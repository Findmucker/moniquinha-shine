import test from 'node:test';
import assert from 'node:assert/strict';
import { handleReviewRequest } from '../supabase/functions/reviews/index.js';

test('a review stays private until approved, appears publicly, then is deleted', async () => {
  const rows = [];
  let sentEmail = '';
  const fetcher = async (url, options = {}) => {
    if (url.startsWith('https://api.emailjs.com/')) {
      sentEmail = JSON.parse(options.body).template_params.message;
      return new Response('OK');
    }
    const parsed = new URL(url);
    assert.equal(parsed.origin, 'https://example.supabase.co');
    assert.equal(options.headers.apikey, 'sb_secret_test_only');
    const filter = row => [...parsed.searchParams].every(([key, value]) => {
      if (['select', 'order', 'limit'].includes(key)) return true;
      if (key === 'created_at') return row.created_at >= value.slice(4);
      return row[key] === value.slice(3);
    });
    if (!options.method || options.method === 'GET') {
      const selection = parsed.searchParams.get('select')?.split(',');
      const matches = rows.filter(filter).map(row => selection
        ? Object.fromEntries(selection.map(key => [key, row[key]])) : row);
      return Response.json(matches);
    }
    if (options.method === 'POST') {
      rows.push({ ...JSON.parse(options.body), created_at: new Date().toISOString() });
      return new Response('', { status: 201 });
    }
    if (options.method === 'PATCH') {
      const matches = rows.filter(filter);
      for (const row of matches) Object.assign(row, JSON.parse(options.body));
      return Response.json(matches);
    }
    if (options.method === 'DELETE') {
      for (const row of rows.filter(filter)) rows.splice(rows.indexOf(row), 1);
      return new Response(null, { status: 204 });
    }
    throw new Error('Unexpected request');
  };
  const env = key => ({ SUPABASE_URL: 'https://example.supabase.co',
    SUPABASE_SECRET_KEYS: JSON.stringify({ default: 'sb_secret_test_only' }) })[key];
  const call = async (method, body, origin = 'https://www.moniquinhashine.pt') => {
    const req = new Request('https://example.supabase.co/functions/v1/reviews', {
      method, headers: { origin, 'x-forwarded-for': '192.0.2.1' },
      ...(body ? { body: JSON.stringify(body) } : {})
    });
    const response = await handleReviewRequest(req, { fetch: fetcher, env });
    return { status: response.status, data: await response.json() };
  };

  const payload = { name: 'Cliente Real', contact: 'teste@example.com',
    comment: 'A casa ficou impecável e gostei muito do cuidado com os detalhes.',
    service: 'cleaning', rating: 5, consent: true };
  assert.equal((await call('POST', payload)).status, 202);
  assert.equal(rows[0].status, 'pending');
  assert.ok(rows[0].moderation_hash);
  assert.equal((await call('GET')).data.reviews.length, 0);
  assert.ok(!JSON.stringify(await call('GET')).includes(payload.contact));
  const [, id, token] = sentEmail.match(/#id=([0-9a-f-]+)&token=([\w-]+)/);
  assert.equal((await call('POST', { id, token: 'x'.repeat(43), action: 'approve' })).status, 404);
  assert.equal((await call('POST', { id, token, action: 'view' })).data.review.contact, payload.contact);
  assert.equal((await call('POST', { id, token, action: 'approve' })).data.status, 'approved');
  const list = (await call('GET')).data.reviews;
  assert.equal(list.length, 1);
  assert.equal(list[0].comment, payload.comment);
  assert.equal('contact' in list[0], false);
  assert.equal((await call('POST', { id, token, action: 'delete' })).data.status, 'deleted');
  assert.equal(rows.length, 0);
  assert.equal((await call('GET')).data.reviews.length, 0);
  assert.equal((await call('POST', payload, 'https://other.example')).status, 403);
});
