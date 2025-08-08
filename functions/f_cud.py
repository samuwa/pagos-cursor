import streamlit as st
import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import time

# Initialize Supabase client
@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and cache Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
        return None
    return create_client(url, key)

def send_otp_email(email: str) -> bool:
    """Send OTP email to user"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
            
        # Send OTP email using Supabase Auth
        response = supabase.auth.sign_in_with_otp({
            "email": email
        })
        
        return True
    except Exception as e:
        st.error(f"Error sending OTP: {str(e)}")
        return False

def verify_otp(email: str, otp: str) -> Optional[Dict[str, Any]]:
    """Verify OTP and authenticate user"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        # Verify OTP
        response = supabase.auth.verify_otp({
            "email": email,
            "token": otp,
            "type": "email"
        })
        
        if response.user:
            # Get user details from our users table
            user_data = supabase.table('users').select('*').eq('email', email).single().execute()
            if user_data.data:
                return {
                    'id': user_data.data['id'],
                    'name': user_data.data['name'],
                    'email': user_data.data['email']
                }
        return None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Legacy function - kept for compatibility but not used"""
    return None

def get_user_roles(user_id: str) -> List[str]:
    """Get user roles from the user_roles table"""
    try:
        # Use service role key to bypass RLS for role queries
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot fetch user roles.")
            return []
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        response = supabase_admin.table('user_roles').select('role').eq('user_id', user_id).execute()
        return [role['role'] for role in response.data]
    except Exception as e:
        st.error(f"Error getting user roles: {str(e)}")
        return []

def create_expense(expense_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new expense with multiple categories and accounts"""
    try:
        # Use service role key to bypass RLS for expense creation
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot create expense.")
            return None
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        
        # Extract category and account IDs for junction tables
        category_ids = expense_data.pop('category_ids', [])
        account_ids = expense_data.pop('account_ids', [])
        
        # Create the expense first
        expense_response = supabase_admin.table('expenses').insert(expense_data).execute()
        if not expense_response.data:
            st.error("Failed to create expense")
            return None
            
        expense = expense_response.data[0]
        expense_id = expense['id']
        
        # Add category relationships
        if category_ids:
            category_relations = [{'expense_id': expense_id, 'category_id': cat_id} for cat_id in category_ids]
            supabase_admin.table('expense_categories').insert(category_relations).execute()
        
        # Add account relationships
        if account_ids:
            account_relations = [{'expense_id': expense_id, 'account_id': acc_id} for acc_id in account_ids]
            supabase_admin.table('expense_accounts').insert(account_relations).execute()
        
        return expense
    except Exception as e:
        st.error(f"Error creating expense: {str(e)}")
        return None

def update_expense(expense_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update an existing expense"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        response = supabase.table('expenses').update(update_data).eq('id', expense_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error updating expense: {str(e)}")
        return None

def delete_expense(expense_id: str) -> bool:
    """Delete an expense (soft delete)"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
            
        response = supabase.table('expenses').update({'deleted_at': 'now()'}).eq('id', expense_id).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error deleting expense: {str(e)}")
        return False

def approve_expense(expense_id: str, approver_id: str, comments: str = None) -> bool:
    """Approve an expense"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
            
        update_data = {
            'phase': 'Aprobado',
            'approver_id': approver_id,
            'updated_at': 'now()'
        }
        
        if comments:
            update_data['description'] = comments
        
        response = supabase.table('expenses').update(update_data).eq('id', expense_id).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error approving expense: {str(e)}")
        return False

def reject_expense(expense_id: str, approver_id: str, comments: str = None) -> bool:
    """Reject an expense"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
            
        update_data = {
            'phase': 'Rechazado',
            'approver_id': approver_id,
            'updated_at': 'now()'
        }
        
        if comments:
            update_data['description'] = comments
        
        response = supabase.table('expenses').update(update_data).eq('id', expense_id).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error rejecting expense: {str(e)}")
        return False

def mark_expense_as_paid(expense_id: str, payer_id: str, payment_date: str = None) -> bool:
    """Mark an expense as paid"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
            
        update_data = {
            'phase': 'Pagado',
            'payer_id': payer_id,
            'updated_at': 'now()'
        }
        
        response = supabase.table('expenses').update(update_data).eq('id', expense_id).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error marking expense as paid: {str(e)}")
        return False

def create_user(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new user"""
    try:
        # Use service role key to bypass RLS for admin operations
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot create user.")
            return None
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        
        response = supabase_admin.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error creating user: {str(e)}")
        return None

def update_user(user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update an existing user"""
    try:
        # Use service role key to bypass RLS for admin operations
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot update user.")
            return None
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        
        response = supabase_admin.table('users').update(update_data).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error updating user: {str(e)}")
        return None

def assign_role_to_user(user_id: str, role: str) -> bool:
    """Assign a role to a user"""
    try:
        # Use service role key to bypass RLS for role management
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot assign role.")
            return False
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        
        role_data = {
            'user_id': user_id,
            'role': role
        }
        
        response = supabase_admin.table('user_roles').insert(role_data).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error assigning role: {str(e)}")
        return False

def remove_role_from_user(user_id: str, role: str) -> bool:
    """Remove a role from a user"""
    try:
        # Use service role key to bypass RLS for role management
        url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not service_key:
            st.error("Missing Supabase service role key. Cannot remove role.")
            return False
            
        # Create client with service role key to bypass RLS
        supabase_admin = create_client(url, service_key)
        
        response = supabase_admin.table('user_roles').delete().eq('user_id', user_id).eq('role', role).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error removing role: {str(e)}")
        return False 