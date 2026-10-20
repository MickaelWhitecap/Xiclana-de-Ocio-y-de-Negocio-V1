-- Xiclana: almacenamiento de cambios manuales y fichas nuevas.
-- 1) Crea un proyecto Supabase y un usuario de administrador.
-- 2) Desactiva el registro público de usuarios en Authentication > Settings.
-- 3) Sustituye ADMIN_EMAIL_HERE por el correo exacto de tu cuenta de administrador.
-- 4) Ejecuta este archivo en SQL Editor.
-- No se usa ni se debe publicar la clave service_role.

create table if not exists public.listing_overrides (
  listing_id text primary key,
  fields jsonb not null default '{}'::jsonb,
  is_new boolean not null default false,
  verified_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  updated_by uuid references auth.users(id) on delete set null
);

alter table public.listing_overrides enable row level security;

drop policy if exists "Public can read listing overrides" on public.listing_overrides;
create policy "Public can read listing overrides"
  on public.listing_overrides for select
  to anon, authenticated
  using (true);

drop policy if exists "Only Xiclana admin can insert overrides" on public.listing_overrides;
create policy "Only Xiclana admin can insert overrides"
  on public.listing_overrides for insert
  to authenticated
  with check (
    (auth.jwt() ->> 'email') = 'ADMIN_EMAIL_HERE'
    and updated_by = auth.uid()
  );

drop policy if exists "Only Xiclana admin can update overrides" on public.listing_overrides;
create policy "Only Xiclana admin can update overrides"
  on public.listing_overrides for update
  to authenticated
  using ((auth.jwt() ->> 'email') = 'ADMIN_EMAIL_HERE')
  with check (
    (auth.jwt() ->> 'email') = 'ADMIN_EMAIL_HERE'
    and updated_by = auth.uid()
  );

drop policy if exists "Only Xiclana admin can delete overrides" on public.listing_overrides;
create policy "Only Xiclana admin can delete overrides"
  on public.listing_overrides for delete
  to authenticated
  using ((auth.jwt() ->> 'email') = 'ADMIN_EMAIL_HERE');

create index if not exists listing_overrides_updated_at_idx
  on public.listing_overrides (updated_at desc);
