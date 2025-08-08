-- Add support for multiple categories and accounts per expense
-- This migration adds junction tables to support many-to-many relationships

-- Create expense_categories junction table
CREATE TABLE expense_categories (
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    category_id BIGINT REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (expense_id, category_id)
);

-- Create expense_accounts junction table
CREATE TABLE expense_accounts (
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    account_id BIGINT REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (expense_id, account_id)
);

-- Add indexes for better performance
CREATE INDEX idx_expense_categories_expense_id ON expense_categories(expense_id);
CREATE INDEX idx_expense_categories_category_id ON expense_categories(category_id);
CREATE INDEX idx_expense_accounts_expense_id ON expense_accounts(expense_id);
CREATE INDEX idx_expense_accounts_account_id ON expense_accounts(account_id);

-- Enable RLS on new tables
ALTER TABLE expense_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE expense_accounts ENABLE ROW LEVEL SECURITY;

-- Add RLS policies for the new tables
CREATE POLICY "Users can view expense categories they're involved with" ON expense_categories
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = expense_categories.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

CREATE POLICY "Users can view expense accounts they're involved with" ON expense_accounts
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM expenses e 
            WHERE e.id = expense_accounts.expense_id 
            AND (e.requester_id = auth.uid() OR e.approver_id = auth.uid() OR e.payer_id = auth.uid())
        )
    );

-- Note: The original category_id and account_id fields in expenses table can be kept for backward compatibility
-- or removed in a future migration if not needed
