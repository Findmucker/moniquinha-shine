import { createHash, createHmac, randomBytes } from 'node:crypto';

export const SERVICES = new Set([
  'cleaning', 'deep-cleaning', 'construction', 'movein', 'laundry',
  'closet', 'organization', 'garage', 'holiday', 'staging', 'other'
]);

export const noStore = { 'Cache-Control': 'no-store, max-age=0', 'Content-Type': 'application/json; charset=utf-8' };

export function respond(res, status, data) {
  for (const [key, value] of Object.entries(noStore)) res.setHeader(key, value);
  return res.status(status).json(data);
}

export function configured() {
  return /^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(process.env.SUPABASE_URL || '') &&
    Boolean(process.env.SUPABASE_SECRET_KEY);
}

export async function database(path, options = {}) {
  if (!configured()) throw new Error('Review storage is not configured');
  const response = await fetch(`${process.env.SUPABASE_URL}/rest/v1/${path}`, {
    ...options,
    headers: {
      apikey: process.env.SUPABASE_SECRET_KEY,
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  });
  if (!response.ok) throw new Error(`Review storage error: ${response.status}`);
  const body = await response.text();
  return body ? JSON.parse(body) : null;
}

export const hash = value => createHash('sha256').update(value).digest('hex');
export const token = () => randomBytes(32).toString('base64url');
export const ipHash = ip => createHmac('sha256', process.env.SUPABASE_SECRET_KEY).update(ip).digest('hex');

export function sameOrigin(req) {
  const origin = req.headers.origin;
  return !origin || origin === 'https://www.moniquinhashine.pt' || origin === 'https://moniquinhashine.pt';
}
