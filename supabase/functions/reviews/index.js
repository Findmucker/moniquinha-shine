// Public endpoint for submissions and approved reviews. Private actions require
// the random token sent only to the owner by email; no privileged key reaches a browser.
const services = new Set([
  'cleaning', 'deep-cleaning', 'construction', 'movein', 'laundry', 'closet',
  'organization', 'garage', 'holiday', 'staging', 'other'
]);
const serviceNames = {
  cleaning: 'Limpeza regular', 'deep-cleaning': 'Limpeza profunda',
  construction: 'Limpeza pós-obra', movein: 'Limpeza de entrada/saída',
  laundry: 'Lavandaria e engomadoria', closet: 'Organização de armários',
  organization: 'Organização da casa', garage: 'Organização de garagem',
  holiday: 'Decoração festiva', staging: 'Home staging', other: 'Outro'
};
const origins = new Set([
  'https://www.moniquinhashine.pt', 'https://moniquinhashine.pt',
  'http://localhost:3000', 'http://127.0.0.1:3000',
  'http://localhost:8000', 'http://127.0.0.1:8000'
]);
const encode = value => new TextEncoder().encode(value);

async function digest(value) {
  const bytes = new Uint8Array(await crypto.subtle.digest('SHA-256', encode(value)));
  return [...bytes].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function ipDigest(ip, key) {
  const secret = await crypto.subtle.importKey('raw', encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const bytes = new Uint8Array(await crypto.subtle.sign('HMAC', secret, encode(ip)));
  return [...bytes].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

function randomToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export async function handleReviewRequest(req, dependencies = {}) {
  const fetcher = dependencies.fetch || fetch;
  const env = dependencies.env || (name => Deno.env.get(name));
  const origin = req.headers.get('origin');
  const allowed = !origin || origins.has(origin);
  const headers = {
    'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store, max-age=0',
    Vary: 'Origin',
    ...(origin && allowed ? { 'Access-Control-Allow-Origin': origin } : {})
  };
  const reply = (code, data) => new Response(JSON.stringify(data), { status: code, headers });
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: allowed ? 204 : 403, headers: {
      ...headers, 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'content-type, apikey, authorization, x-client-info'
    } });
  }
  if (!allowed) return reply(403, { error: 'Invalid origin' });
  if (!['GET', 'POST'].includes(req.method)) return reply(405, { error: 'Method not allowed' });

  let key;
  try { key = JSON.parse(env('SUPABASE_SECRET_KEYS') || '{}').default || env('SUPABASE_SERVICE_ROLE_KEY'); }
  catch { key = env('SUPABASE_SERVICE_ROLE_KEY'); }
  const url = env('SUPABASE_URL');
  if (!key || !/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(url || '')) return reply(503, { error: 'Reviews unavailable' });
  const database = async (path, options = {}) => {
    const response = await fetcher(`${url}/rest/v1/${path}`, {
      ...options, headers: { apikey: key, 'Content-Type': 'application/json', ...(options.headers || {}) }
    });
    if (!response.ok) throw new Error(`Database status ${response.status}`);
    const text = await response.text();
    return text ? JSON.parse(text) : null;
  };

  try {
    if (req.method === 'GET') {
      const reviews = await database('reviews?status=eq.approved&select=id,display_name,rating,service,comment,created_at&order=approved_at.desc&limit=60');
      return reply(200, { reviews });
    }

    const raw = await req.text();
    if (raw.length > 10000) return reply(413, { error: 'Request too large' });
    let body;
    try { body = JSON.parse(raw); } catch { return reply(400, { error: 'Invalid JSON' }); }
    if (!body || typeof body !== 'object') return reply(400, { error: 'Invalid request' });

    if (body.action) {
      const { id, token, action } = body;
      if (!/^[0-9a-f-]{36}$/i.test(id || '') || !/^[a-zA-Z0-9_-]{43}$/.test(token || '') ||
          !['view', 'approve', 'delete'].includes(action)) return reply(400, { error: 'Invalid request' });
      const conditions = `id=eq.${id}&moderation_hash=eq.${await digest(token)}`;
      const rows = await database(`reviews?${conditions}&select=id,display_name,rating,service,comment,contact,status,created_at&limit=1`);
      if (!rows.length) return reply(404, { error: 'Review not found' });
      const review = rows[0];
      if (action === 'view') return reply(200, { review });
      if (action === 'approve') {
        if (review.status !== 'pending') return reply(409, { error: 'Review already processed' });
        const updated = await database(`reviews?${conditions}&status=eq.pending`, {
          method: 'PATCH', headers: { Prefer: 'return=representation' },
          body: JSON.stringify({ status: 'approved', approved_at: new Date().toISOString() })
        });
        return updated?.length ? reply(200, { status: 'approved' }) : reply(409, { error: 'Review already processed' });
      }
      await database(`reviews?${conditions}`, { method: 'DELETE' });
      return reply(200, { status: 'deleted' });
    }

    if (body.website) return reply(202, { ok: true });
    const name = String(body.name || '').trim();
    const contact = String(body.contact || '').trim();
    const comment = String(body.comment || '').trim();
    const service = String(body.service || '');
    const rating = Number(body.rating);
    const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact);
    const phone = /^\+?[\d\s().-]+$/.test(contact) &&
      contact.replace(/\D/g, '').length >= 9 && contact.replace(/\D/g, '').length <= 15;
    if (name.length < 2 || name.length > 40 || /[\r\n\x00-\x1f]/.test(name) ||
        contact.length > 120 || (!email && !phone) || comment.length < 20 || comment.length > 600 ||
        !services.has(service) || !Number.isInteger(rating) || rating < 1 || rating > 5 || body.consent !== true) {
      return reply(400, { error: 'Invalid review' });
    }

    const clientIp = String(req.headers.get('x-forwarded-for') || 'unknown').split(',')[0].trim();
    const identifier = await ipDigest(clientIp, key);
    const since = new Date(Date.now() - 86400000).toISOString();
    const recent = await database(`reviews?ip_hash=eq.${identifier}&created_at=gte.${encodeURIComponent(since)}&select=id&limit=3`);
    if (recent.length >= 3) return reply(429, { error: 'Too many reviews' });

    const secret = randomToken();
    const id = crypto.randomUUID();
    await database('reviews', {
      method: 'POST', body: JSON.stringify({ id, display_name: name, contact, comment, service, rating,
        moderation_hash: await digest(secret), ip_hash: identifier, status: 'pending' })
    });
    const approvalLink = `https://www.moniquinhashine.pt/aprovar-testemunho#id=${id}&token=${secret}`;
    const message = [
      'NOVO TESTEMUNHO PARA APROVAÇÃO', `Nome a mostrar: ${name}`, `Classificação: ${rating}/5`,
      `Serviço: ${serviceNames[service]}`, `Contacto privado: ${contact}`,
      'Autorização de publicação: sim', '', 'Comentário:', comment,
      '', 'Para rever e decidir, abra esta ligação privada:', approvalLink,
      'A ligação também permite retirar o testemunho depois de publicado. Não a partilhe.'
    ].join('\n');
    try {
      const mail = await fetcher('https://api.emailjs.com/api/v1.0/email/send', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service_id: 'service_0o7hvd3', template_id: 'template_m24yjpo',
          user_id: 'IOvvpHPz0DZRqJlmz',
          template_params: { from_name: name, from_email: email ? contact : 'Não indicado',
            from_phone: phone ? contact : 'Não indicado', address: 'Testemunho — não aplicável',
            address_map_url: '', service: `TESTEMUNHO • ${serviceNames[service]}`,
            home_type: 'Não aplicável', date: 'Não aplicável', time: 'Não aplicável',
            period: 'Não aplicável', message, approval_url: approvalLink }
        })
      });
      if (!mail.ok) throw new Error(`Email status ${mail.status}`);
    } catch (error) {
      try { await database(`reviews?id=eq.${id}`, { method: 'DELETE' }); } catch { /* recover manually if storage failed */ }
      throw error;
    }
    return reply(202, { ok: true });
  } catch (error) {
    console.error('Review request failed:', error.message);
    return reply(503, { error: 'Reviews unavailable' });
  }
}

if (typeof Deno !== 'undefined') Deno.serve(handleReviewRequest);
