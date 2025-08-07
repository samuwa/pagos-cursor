-- Migration: Remove stytch_user_id column from users table
-- This migration removes the unused stytch_user_id column

-- Remove the stytch_user_id column from the users table
ALTER TABLE users DROP COLUMN IF EXISTS stytch_user_id;

-- Verify the column was removed
-- You can run this query to confirm: SELECT column_name FROM information_schema.columns WHERE table_name = 'users';
