-- Fix RLS policies for user_roles table
-- This allows users to read their own roles from the user_roles table

-- Policy for users to read their own roles
CREATE POLICY "Users can read their own roles" ON user_roles
    FOR SELECT USING (
        auth.uid()::text = user_id::text
    );

-- Policy for admins to read all roles (optional)
CREATE POLICY "Admins can read all roles" ON user_roles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM user_roles ur 
            WHERE ur.user_id = auth.uid() 
            AND ur.role = 'admin'
        )
    );

-- Policy for inserting roles (for admin functionality)
CREATE POLICY "Admins can insert roles" ON user_roles
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM user_roles ur 
            WHERE ur.user_id = auth.uid() 
            AND ur.role = 'admin'
        )
    );

-- Policy for updating roles (for admin functionality)
CREATE POLICY "Admins can update roles" ON user_roles
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM user_roles ur 
            WHERE ur.user_id = auth.uid() 
            AND ur.role = 'admin'
        )
    );

-- Policy for deleting roles (for admin functionality)
CREATE POLICY "Admins can delete roles" ON user_roles
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM user_roles ur 
            WHERE ur.user_id = auth.uid() 
            AND ur.role = 'admin'
        )
    );
