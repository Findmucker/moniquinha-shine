import test from 'node:test';
import assert from 'node:assert/strict';
import submit from '../api/reviews.js';
import moderate from '../api/reviews-moderate.js';

test('a review stays private until approved, appears publicly, then is deleted', async () => {
  process.env.SUPABASE_URL = 'https://example.supabase.co';
  process.env.SUPABASE_SECRET_KEY = 'sb_secret_test_only';
  const rows = [];
  let sentEmail = '';
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, options = {}) => {
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
      const matching = rows.filter(filter).map(row => selection
        ? Object.fromEntries(selection.map(key => [key, row[key]])) : row);
      return Response.json(matching);
    }
    if (options.method === 'POST') {
      rows.push({ ...JSON.parse(options.body), created_at: new Date().toISOString() });
      return new Response('', { status: 201 });
    }
    if (options.method === 'PATCH') {
      const matched = rows.filter(filter);
      for (const row of matched) Object.assign(row, JSON.parse(options.body));
      return Response.json(matched);
    }
    if (options.method === 'DELETE') {
      for (const row of rows.filter(filter)) rows.splice(rows.indexOf(row), 1);
      return new Response(null, { status: 204 });
    }
    throw new Error('Unexpected request');
  };
  const call = async (handler, method, body) => {
    const response = { status(code) { this.code = code; return this; }, json(value) { this.body = value; return this; }, setHeader() {} };
    await handler({ method, body, headers: { origin: 'https://www.moniquinhashine.pt', 'x-forwarded-for': '192.0.2.1' } }, response);
    return response;
  };
  try {
    const payload = { name: 'Cliente Real', contact: 'teste@example.com', comment: 'A casa ficou impecável e gostei muito do cuidado com os detalhes.', service: 'cleaning', rating: 5, consent: true };
    assert.equal((await call(submit, 'POST', payload)).code, 202);
    assert.equal(rows[0].status, 'pending');
    assert.ok(rows[0].moderation_hash);
    assert.equal((await call(submit, 'GET')).body.reviews.length, 0);
    assert.ok(!JSON.stringify(await call(submit, 'GET')).includes(payload.contact));
    const [, id, token] = sentEmail.match(/#id=([0-9a-f-]+)&token=([\w-]+)/);
    assert.equal((await call(moderate, 'POST', { id, token: 'x'.repeat(43), action: 'approve' })).code, 404);
    assert.equal((await call(moderate, 'POST', { id, token, action: 'view' })).body.review.contact, payload.contact);
    assert.equal((await call(moderate, 'POST', { id, token, action: 'approve' })).body.status, 'approved');
    const list = (await call(submit, 'GET')).body.reviews;
    assert.equal(list.length, 1);
    assert.equal(list[0].comment, payload.comment);
    assert.equal((await call(moderate, 'POST', { id, token, action: 'delete' })).body.status, 'deleted');
    assert.equal(rows.length, 0);
    assert.equal((await call(submit, 'GET')).body.reviews.length, 0);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
