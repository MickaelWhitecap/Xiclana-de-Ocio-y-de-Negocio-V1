-- Xiclana V1: fichas provisionales pendientes de revisión
-- Ejecutar una sola vez en Supabase > SQL Editor > New query.
-- Las propuestas NO se publican: la web pública no consulta esta tabla.

create table if not exists public.listing_proposals (
  id uuid primary key default gen_random_uuid(),
  fields jsonb not null default '{}'::jsonb,
  source_name text,
  source_url text,
  source_checked_at date,
  notes text,
  status text not null default 'pending'
    check (status in ('pending','approved','rejected')),
  created_at timestamptz not null default now(),
  created_by uuid references auth.users(id) on delete set null,
  reviewed_at timestamptz,
  reviewed_by uuid references auth.users(id) on delete set null,
  review_notes text
);

create index if not exists listing_proposals_status_created_idx
  on public.listing_proposals (status, created_at desc);

alter table public.listing_proposals enable row level security;

-- Propuestas privadas: únicamente la cuenta administradora autorizada puede leer o modificarlas.
drop policy if exists "Xiclana admin can read proposals" on public.listing_proposals;
create policy "Xiclana admin can read proposals"
  on public.listing_proposals for select to authenticated
  using ((auth.jwt() ->> 'email') = 'surferomc@gmail.com');

drop policy if exists "Xiclana admin can insert proposals" on public.listing_proposals;
create policy "Xiclana admin can insert proposals"
  on public.listing_proposals for insert to authenticated
  with check ((auth.jwt() ->> 'email') = 'surferomc@gmail.com');

drop policy if exists "Xiclana admin can update proposals" on public.listing_proposals;
create policy "Xiclana admin can update proposals"
  on public.listing_proposals for update to authenticated
  using ((auth.jwt() ->> 'email') = 'surferomc@gmail.com')
  with check ((auth.jwt() ->> 'email') = 'surferomc@gmail.com');

drop policy if exists "Xiclana admin can delete proposals" on public.listing_proposals;
create policy "Xiclana admin can delete proposals"
  on public.listing_proposals for delete to authenticated
  using ((auth.jwt() ->> 'email') = 'surferomc@gmail.com');

-- No crear políticas para anon ni para otros usuarios.
