import { configured, database, hash, respond, sameOrigin } from '../lib/reviews.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return respond(res, 405, { error: 'Method not allowed' });
  if (!sameOrigin(req)) return respond(res, 403, { error: 'Invalid origin' });
  if (!configured()) return respond(res, 503, { error: 'Reviews unavailable' });
  const { id, token, action } = req.body || {};
  if (!/^[0-9a-f-]{36}$/i.test(id || '') || !/^[a-zA-Z0-9_-]{43}$/.test(token || '') ||
      !['view', 'approve', 'delete'].includes(action)) return respond(res, 400, { error: 'Invalid request' });
  const conditions = `id=eq.${id}&moderation_hash=eq.${hash(token)}`;
  try {
    const rows = await database(`reviews?${conditions}&select=id,display_name,rating,service,comment,contact,status,created_at&limit=1`);
    if (!rows.length) return respond(res, 404, { error: 'Review not found' });
    const review = rows[0];
    if (action === 'view') return respond(res, 200, { review });
    if (action === 'approve') {
      if (review.status !== 'pending') return respond(res, 409, { error: 'Review already processed' });
      await database(`reviews?${conditions}&status=eq.pending`, {
        method: 'PATCH', headers: { Prefer: 'return=representation' },
        body: JSON.stringify({ status: 'approved', approved_at: new Date().toISOString() })
      }).then(rows => {
        if (!rows.length) throw new Error('Review already processed');
      });
      return respond(res, 200, { status: 'approved' });
    }
    // Delete also works after approval, so the same private link can remove a test review.
    await database(`reviews?${conditions}`, { method: 'DELETE' });
    return respond(res, 200, { status: 'deleted' });
  } catch (error) {
    console.error('Review moderation failed:', error.message);
    return respond(res, 503, { error: 'Review unavailable' });
  }
}
