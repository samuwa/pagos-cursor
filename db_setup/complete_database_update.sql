-- 🔄 Complete Database Update Migration
-- This file brings the database up to date with all missing tables and columns
-- that the application functions expect to exist.

-- ========================================
-- 1. ADD MISSING COLUMNS TO EXISTING TABLES
-- ========================================

-- Add receiver_id column to expenses table (if not already exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'expenses' AND column_name = 'receiver_id'
    ) THEN
        ALTER TABLE expenses ADD COLUMN receiver_id BIGINT REFERENCES receivers(id) ON DELETE SET NULL;
        CREATE INDEX idx_expenses_receiver_id ON expenses(receiver_id);
        COMMENT ON COLUMN expenses.receiver_id IS 'Reference to the receiver/supplier for this expense';
    END IF;
END $$;

-- ========================================
-- 2. CREATE MISSING JUNCTION TABLES
-- ========================================

-- Create expense_categories junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS expense_categories (
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    category_id BIGINT REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (expense_id, category_id)
);

-- Create expense_accounts junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS expense_accounts (
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    account_id BIGINT REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (expense_id, account_id)
);

-- ========================================
-- 3. CREATE PAYMENT RECEIPTS TABLE
-- ========================================

-- Create payment_receipts table for storing payment receipt files
CREATE TABLE IF NOT EXISTS payment_receipts (
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

-- ========================================
-- 4. CREATE INDEXES FOR PERFORMANCE
-- ========================================

-- Indexes for junction tables
CREATE INDEX IF NOT EXISTS idx_expense_categories_expense_id ON expense_categories(expense_id);
CREATE INDEX IF NOT EXISTS idx_expense_categories_category_id ON expense_categories(category_id);
CREATE INDEX IF NOT EXISTS idx_expense_accounts_expense_id ON expense_accounts(expense_id);
CREATE INDEX IF NOT EXISTS idx_expense_accounts_account_id ON expense_accounts(account_id);

-- Indexes for payment_receipts table
CREATE INDEX IF NOT EXISTS idx_payment_receipts_expense_id ON payment_receipts(expense_id);
CREATE INDEX IF NOT EXISTS idx_payment_receipts_payer_id ON payment_receipts(payer_id);
CREATE INDEX IF NOT EXISTS idx_payment_receipts_uploaded_at ON payment_receipts(uploaded_at);

-- ========================================
-- 5. ENABLE ROW LEVEL SECURITY (RLS)
-- ========================================

-- Enable RLS on new tables
ALTER TABLE expense_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE expense_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_receipts ENABLE ROW LEVEL SECURITY;

-- ========================================
-- 6. CREATE RLS POLICIES
-- ========================================

-- RLS policies for expense_categories
DROP POLICY IF EXISTS "Users can view expense categories they're involved with" ON expense_categories;
CREATE POLICY "Users can view expense categories they're involved with" ON expense_categories
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = expense_categories.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

-- RLS policies for expense_accounts
DROP POLICY IF EXISTS "Users can view expense accounts they're involved with" ON expense_accounts;
CREATE POLICY "Users can view expense accounts they're involved with" ON expense_accounts
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = expense_accounts.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

-- RLS policies for payment_receipts
DROP POLICY IF EXISTS "Users can view payment receipts they're involved with" ON payment_receipts;
CREATE POLICY "Users can view payment receipts they're involved with" ON payment_receipts
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = payment_receipts.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

DROP POLICY IF EXISTS "Payers can insert payment receipts" ON payment_receipts;
CREATE POLICY "Payers can insert payment receipts" ON payment_receipts
    FOR INSERT WITH CHECK (
        auth.uid() = payer_id
    );

-- ========================================
-- 7. CREATE UPDATED_AT TRIGGERS
-- ========================================

-- Create updated_at trigger function if it doesn't exist
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to payment_receipts
DROP TRIGGER IF EXISTS update_payment_receipts_updated_at ON payment_receipts;
CREATE TRIGGER update_payment_receipts_updated_at 
    BEFORE UPDATE ON payment_receipts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 8. DATA MIGRATION (OPTIONAL)
-- ========================================

-- If you want to migrate existing single category/account relationships to the new junction tables
-- Uncomment the following section if you have existing data to migrate:

/*
-- Migrate existing category relationships
INSERT INTO expense_categories (expense_id, category_id)
SELECT id, category_id 
FROM expenses 
WHERE category_id IS NOT NULL 
AND id NOT IN (SELECT expense_id FROM expense_categories);

-- Migrate existing account relationships  
INSERT INTO expense_accounts (expense_id, account_id)
SELECT id, account_id 
FROM expenses 
WHERE account_id IS NOT NULL 
AND id NOT IN (SELECT expense_id FROM expense_accounts);
*/

-- ========================================
-- 9. VERIFICATION QUERIES
-- ========================================

-- Verify all tables exist
DO $$
DECLARE
    missing_tables TEXT[] := ARRAY[]::TEXT[];
    tbl_name TEXT;
BEGIN
    -- Check for required tables
    FOR tbl_name IN 
        SELECT unnest(ARRAY['expense_categories', 'expense_accounts', 'payment_receipts'])
    LOOP
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = tbl_name
        ) THEN
            missing_tables := array_append(missing_tables, tbl_name);
        END IF;
    END LOOP;
    
    -- Check for required columns
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'expenses' AND column_name = 'receiver_id'
    ) THEN
        missing_tables := array_append(missing_tables, 'expenses.receiver_id');
    END IF;
    
    -- Report results
    IF array_length(missing_tables, 1) > 0 THEN
        RAISE NOTICE '❌ Missing elements: %', array_to_string(missing_tables, ', ');
    ELSE
        RAISE NOTICE '✅ All required tables and columns are present!';
    END IF;
END $$;

-- ========================================
-- 10. FINAL STATUS REPORT
-- ========================================

-- Show final table count
SELECT 
    'Database Update Complete' as status,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public') as total_tables,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'public') as total_columns;

-- Show new tables created
SELECT 
    table_name,
    'New Table' as type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('expense_categories', 'expense_accounts', 'payment_receipts')
ORDER BY table_name;

-- 🎉 Migration Complete!
-- The database is now fully compatible with the application functions.
