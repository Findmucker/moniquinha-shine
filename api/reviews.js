import { randomUUID } from 'node:crypto';
import { configured, database, hash, ipHash, respond, sameOrigin, SERVICES, token } from '../lib/reviews.js';

const serviceNames = {
  cleaning: 'Limpeza regular', 'deep-cleaning': 'Limpeza profunda',
  construction: 'Limpeza pós-obra', movein: 'Limpeza de entrada/saída',
  laundry: 'Lavandaria e engomadoria', closet: 'Organização de armários',
  organization: 'Organização da casa', garage: 'Organização de garagem',
  holiday: 'Decoração festiva', staging: 'Home staging', other: 'Outro'
};

export default async function handler(req, res) {
  if (req.method === 'GET') {
    if (!configured()) return respond(res, 503, { error: 'Reviews unavailable' });
    try {
      const reviews = await database('reviews?status=eq.approved&select=id,display_name,rating,service,comment,created_at&order=approved_at.desc&limit=60');
      return respond(res, 200, { reviews });
    } catch {
      return respond(res, 503, { error: 'Reviews unavailable' });
    }
  }
  if (req.method !== 'POST') return respond(res, 405, { error: 'Method not allowed' });
  if (!sameOrigin(req)) return respond(res, 403, { error: 'Invalid origin' });
  if (!configured()) return respond(res, 503, { error: 'Reviews unavailable' });
  if (Number(req.headers['content-length']) > 10000) return respond(res, 413, { error: 'Request too large' });
  const body = req.body || {};
  if (body.website) return respond(res, 202, { ok: true });

  const name = String(body.name || '').trim();
  const contact = String(body.contact || '').trim();
  const comment = String(body.comment || '').trim();
  const service = String(body.service || '');
  const rating = Number(body.rating);
  const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact);
  const phone = /^\+?[\d\s().-]+$/.test(contact) && contact.replace(/\D/g, '').length >= 9 && contact.replace(/\D/g, '').length <= 15;
  if (name.length < 2 || name.length > 40 || /[\r\n\x00-\x1f]/.test(name) ||
      contact.length > 120 || (!email && !phone) || comment.length < 20 || comment.length > 600 ||
      !SERVICES.has(service) || !Number.isInteger(rating) || rating < 1 || rating > 5 || body.consent !== true) {
    return respond(res, 400, { error: 'Invalid review' });
  }

  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
  const identifier = ipHash(ip);
  let reviewId;
  try {
    const since = new Date(Date.now() - 86400000).toISOString();
    const recent = await database(`reviews?ip_hash=eq.${identifier}&created_at=gte.${encodeURIComponent(since)}&select=id&limit=3`);
    if (recent.length >= 3) return respond(res, 429, { error: 'Too many reviews' });

    const secret = token();
    const id = randomUUID();
    reviewId = id;
    await database('reviews', {
      method: 'POST',
      body: JSON.stringify({ id, display_name: name, contact, comment, service, rating,
        moderation_hash: hash(secret), ip_hash: identifier, status: 'pending' })
    });

    // The link token is created on the server. It is never returned to the visitor.
    const approvalLink = `https://www.moniquinhashine.pt/aprovar-testemunho.html#id=${id}&token=${secret}`;
    const message = [
      'NOVO TESTEMUNHO PARA APROVAÇÃO',
      `Nome a mostrar: ${name}`,
      `Classificação: ${rating}/5`,
      `Serviço: ${serviceNames[service]}`,
      `Contacto privado: ${contact}`,
      'Autorização de publicação: sim',
      '', 'Comentário:', comment,
      '', 'Para rever e decidir, abra esta ligação privada:', approvalLink,
      'A ligação também permite retirar o testemunho depois de publicado. Não a partilhe.'
    ].join('\n');
    const mail = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ service_id: 'service_0o7hvd3', template_id: 'template_m24yjpo',
        user_id: 'IOvvpHPz0DZRqJlmz',
        template_params: {
          from_name: name, from_email: email ? contact : 'Não indicado',
          from_phone: phone ? contact : 'Não indicado', address: 'Testemunho — não aplicável',
          address_map_url: '', service: `TESTEMUNHO • ${serviceNames[service]}`,
          home_type: 'Não aplicável', date: 'Não aplicável', time: 'Não aplicável',
          period: 'Não aplicável', message, approval_url: approvalLink
        }
      })
    });
    if (!mail.ok) throw new Error(`Mail error: ${mail.status}`);
    return respond(res, 202, { ok: true });
  } catch (error) {
    // A failed notification must never leave a review awaiting an email that was not sent.
    if (reviewId) {
      try { await database(`reviews?id=eq.${reviewId}`, { method: 'DELETE' }); } catch { /* Retained pending for manual recovery. */ }
    }
    console.error('Review submission failed:', error.message);
    return respond(res, 503, { error: 'Review unavailable' });
  }
}
