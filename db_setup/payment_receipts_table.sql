-- Create payment_receipts table for storing payment receipt files
CREATE TABLE payment_receipts (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    payer_id UUID REFERENCES users(id) ON DELETE RESTRICT,
    file_url TEXT NOT NULL, -- Supabase storage URL
    file_name TEXT, -- Original filename
    file_size BIGINT, -- File size in bytes
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Add indexes for better performance
CREATE INDEX idx_payment_receipts_expense_id ON payment_receipts(expense_id);
CREATE INDEX idx_payment_receipts_payer_id ON payment_receipts(payer_id);
CREATE INDEX idx_payment_receipts_uploaded_at ON payment_receipts(uploaded_at);

-- Enable RLS on the new table
ALTER TABLE payment_receipts ENABLE ROW LEVEL SECURITY;

-- Add RLS policies for payment_receipts
CREATE POLICY "Users can view payment receipts they're involved with" ON payment_receipts
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = payment_receipts.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

CREATE POLICY "Payers can insert payment receipts" ON payment_receipts
    FOR INSERT WITH CHECK (
        auth.uid() = payer_id
    );

-- Apply updated_at trigger
CREATE TRIGGER update_payment_receipts_updated_at 
    BEFORE UPDATE ON payment_receipts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
