-- Xiclana V1: categorías creadas desde el panel de administración.
-- Ejecuta este archivo una sola vez en Supabase > SQL Editor.
-- Mantiene lectura pública y restringe escrituras a la cuenta administradora.

create table if not exists public.listing_categories (
  slug text primary key,
  name text not null,
  type text not null default 'negocio' check (type in ('ocio','negocio')),
  created_at timestamptz not null default now(),
  created_by uuid references auth.users(id) on delete set null
);

alter table public.listing_categories enable row level security;

drop policy if exists "Public can read listing categories" on public.listing_categories;
create policy "Public can read listing categories"
  on public.listing_categories for select
  to anon, authenticated
  using (true);

drop policy if exists "Only Xiclana admin can insert listing categories" on public.listing_categories;
create policy "Only Xiclana admin can insert listing categories"
  on public.listing_categories for insert
  to authenticated
  with check (
    (auth.jwt() ->> 'email') = 'surferomc@gmail.com'
    and created_by = auth.uid()
  );

drop policy if exists "Only Xiclana admin can update listing categories" on public.listing_categories;
create policy "Only Xiclana admin can update listing categories"
  on public.listing_categories for update
  to authenticated
  using ((auth.jwt() ->> 'email') = 'surferomc@gmail.com')
  with check (
    (auth.jwt() ->> 'email') = 'surferomc@gmail.com'
    and created_by = auth.uid()
  );

drop policy if exists "Only Xiclana admin can delete listing categories" on public.listing_categories;
create policy "Only Xiclana admin can delete listing categories"
  on public.listing_categories for delete
  to authenticated
  using ((auth.jwt() ->> 'email') = 'surferomc@gmail.com');

create index if not exists listing_categories_name_idx
  on public.listing_categories (name);
