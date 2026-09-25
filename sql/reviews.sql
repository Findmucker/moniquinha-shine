-- Run only in a dedicated Supabase project for Moniquinha Shine.
create table if not exists public.reviews (
  id uuid primary key,
  display_name text not null check (char_length(display_name) between 2 and 40),
  contact text not null check (char_length(contact) <= 120),
  rating smallint not null check (rating between 1 and 5),
  service text not null check (service in ('cleaning','deep-cleaning','construction','movein','laundry','closet','organization','garage','holiday','staging','other')),
  comment text not null check (char_length(comment) between 20 and 600),
  status text not null default 'pending' check (status in ('pending','approved')),
  moderation_hash text not null unique check (char_length(moderation_hash) = 64),
  ip_hash text not null check (char_length(ip_hash) = 64),
  created_at timestamptz not null default now(),
  approved_at timestamptz
);

create index if not exists reviews_published_idx on public.reviews (approved_at desc) where status = 'approved';
create index if not exists reviews_rate_idx on public.reviews (ip_hash, created_at desc);

alter table public.reviews enable row level security;
revoke all on public.reviews from anon, authenticated;
grant select, insert, update, delete on public.reviews to service_role;
