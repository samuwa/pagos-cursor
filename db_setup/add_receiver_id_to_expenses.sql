-- Migration: Add receiver_id column to expenses table
-- This migration adds a receiver_id column to link expenses to receivers

-- Add receiver_id column to expenses table
ALTER TABLE expenses 
ADD COLUMN receiver_id BIGINT REFERENCES receivers(id) ON DELETE SET NULL;

-- Create index for better performance
CREATE INDEX idx_expenses_receiver_id ON expenses(receiver_id);

-- Add comment to document the change
COMMENT ON COLUMN expenses.receiver_id IS 'Reference to the receiver/supplier for this expense';
