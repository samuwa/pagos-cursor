-- 📘 Enhanced Database Schema for Pagos Expense Management System
-- This schema includes all recommended improvements and optimizations

-- 🎯 Create custom enum types
CREATE TYPE expense_phase AS ENUM ('Creado', 'Aprobado', 'Pagado', 'Rechazado');
CREATE TYPE user_role AS ENUM ('admin', 'payer', 'approver', 'requester', 'viewer');

-- 👥 Users table (simplified without boolean flags)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    stytch_user_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 🔐 User roles table (normalized)
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role user_role NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (user_id, role)
);

-- 📂 Categories table
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 💰 Accounts table
CREATE TABLE accounts (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT REFERENCES categories(id) ON DELETE RESTRICT,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 👤 Receivers table
CREATE TABLE receivers (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    role VARCHAR(100),
    created_by UUID REFERENCES users(id) ON DELETE RESTRICT,
    created_date DATE DEFAULT CURRENT_DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 💸 Expenses table (enhanced)
CREATE TABLE expenses (
    id BIGSERIAL PRIMARY KEY,
    amount NUMERIC(10,2) NOT NULL,
    account_id BIGINT REFERENCES accounts(id) ON DELETE SET NULL,
    category_id BIGINT REFERENCES categories(id) ON DELETE RESTRICT,
    requester_id UUID REFERENCES users(id) ON DELETE RESTRICT,
    approver_id UUID REFERENCES users(id) ON DELETE SET NULL,
    payer_id UUID REFERENCES users(id) ON DELETE SET NULL,
    approved_quote_id BIGINT, -- Will reference quotes table
    description TEXT,
    payment_method TEXT,
    payment_receipt TEXT,
    phase expense_phase DEFAULT 'Creado',
    date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT positive_amount CHECK (amount > 0),
    CONSTRAINT valid_phase CHECK (phase IN ('Creado', 'Aprobado', 'Pagado', 'Rechazado'))
);

-- 💬 Comments table
CREATE TABLE comments (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    created_by UUID REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    content TEXT NOT NULL
);

-- 📝 Logs table
CREATE TABLE logs (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    created_by UUID REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    content TEXT NOT NULL
);

-- 📄 Quotes table (enhanced with file metadata)
CREATE TABLE quotes (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    receiver_id BIGINT REFERENCES receivers(id) ON DELETE RESTRICT,
    descripcion TEXT,
    file_url TEXT NOT NULL, -- Supabase storage URL
    file_name TEXT, -- Original filename
    file_size BIGINT, -- File size in bytes
    total NUMERIC(10,2) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    
    CONSTRAINT positive_quote_total CHECK (total > 0)
);

-- 🔗 People/Suppliers table
CREATE TABLE people_suppliers (
    id BIGSERIAL PRIMARY KEY,
    receiver_id BIGINT REFERENCES receivers(id) ON DELETE CASCADE,
    email TEXT,
    phone TEXT,
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 💰 Reimbursements table
CREATE TABLE reembolsos (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    receiver_id BIGINT REFERENCES receivers(id) ON DELETE RESTRICT,
    created_by UUID REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 🔗 Receiver-Accounts association table
CREATE TABLE receiver_accounts (
    receiver_id BIGINT REFERENCES receivers(id) ON DELETE CASCADE,
    account_id BIGINT REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (receiver_id, account_id)
);

-- 🔗 Receiver-Categories association table
CREATE TABLE receiver_categories (
    receiver_id BIGINT REFERENCES receivers(id) ON DELETE CASCADE,
    category_id BIGINT REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (receiver_id, category_id)
);

-- 🔗 Add foreign key constraint for approved_quote_id
ALTER TABLE expenses 
ADD CONSTRAINT fk_expenses_approved_quote 
FOREIGN KEY (approved_quote_id) REFERENCES quotes(id) ON DELETE SET NULL;

-- 📊 Create indexes for better performance
CREATE INDEX idx_expenses_requester_id ON expenses(requester_id);
CREATE INDEX idx_expenses_phase ON expenses(phase);
CREATE INDEX idx_expenses_date_created ON expenses(date_created);
CREATE INDEX idx_expenses_category_id ON expenses(category_id);
CREATE INDEX idx_comments_expense_id ON comments(expense_id);
CREATE INDEX idx_logs_expense_id ON logs(expense_id);
CREATE INDEX idx_quotes_expense_id ON quotes(expense_id);
CREATE INDEX idx_quotes_receiver_id ON quotes(receiver_id);
CREATE INDEX idx_reembolsos_expense_id ON reembolsos(expense_id);
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role);

-- 🔄 Create updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_receivers_updated_at BEFORE UPDATE ON receivers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_expenses_updated_at BEFORE UPDATE ON expenses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quotes_updated_at BEFORE UPDATE ON quotes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_people_suppliers_updated_at BEFORE UPDATE ON people_suppliers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 🎯 Insert some initial data for testing
INSERT INTO categories (description) VALUES 
('Office Supplies'),
('Travel'),
('Equipment'),
('Software'),
('Marketing');

-- Insert sample accounts
INSERT INTO accounts (category_id, description) VALUES 
(1, 'Office Supplies Account'),
(2, 'Travel Expenses Account'),
(3, 'Equipment Purchase Account'),
(4, 'Software Licenses Account'),
(5, 'Marketing Budget Account');

-- 🔐 Create RLS (Row Level Security) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE receivers ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE people_suppliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE reembolsos ENABLE ROW LEVEL SECURITY;
ALTER TABLE receiver_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE receiver_categories ENABLE ROW LEVEL SECURITY;

-- 📋 Grant necessary permissions (adjust based on your auth setup)
-- These policies should be customized based on your specific authentication and authorization requirements

-- Example policy for expenses (users can see expenses they're involved with)
CREATE POLICY "Users can view expenses they're involved with" ON expenses
    FOR SELECT USING (
        auth.uid() = requester_id OR 
        auth.uid() = approver_id OR 
        auth.uid() = payer_id
    );

-- Example policy for users (users can view their own profile)
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- 🎉 Database schema creation complete!
-- The database is now ready for the Pagos expense management system 