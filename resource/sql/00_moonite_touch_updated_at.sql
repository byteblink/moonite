-- PostgreSQL 18 — shared trigger function for updated_at
-- Run this file before any table DDL that attaches moonite_touch_updated_at.

CREATE OR REPLACE FUNCTION public.moonite_touch_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.moonite_touch_updated_at() IS 'BEFORE UPDATE 触发器用：将 NEW.updated_at 设为当前时间';
