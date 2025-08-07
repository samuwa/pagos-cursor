import streamlit as st
import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Initialize Supabase client (reuse from f_cud.py)
@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and cache Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("❌ Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
        return None
    return create_client(url, key)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        response = supabase.table('users').select('*').eq('email', email).single().execute()
        return response.data if response.data else None
    except Exception as e:
        st.error(f"❌ Error getting user: {str(e)}")
        return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        response = supabase.table('users').select('*').eq('id', user_id).single().execute()
        return response.data if response.data else None
    except Exception as e:
        st.error(f"❌ Error getting user: {str(e)}")
        return None

def get_all_users() -> List[Dict[str, Any]]:
    """Get all users"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('users').select('*').is_('deleted_at', 'null').execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting users: {str(e)}")
        return []

def get_expense_by_id(expense_id: str) -> Optional[Dict[str, Any]]:
    """Get expense by ID"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        response = supabase.table('expenses').select('*').eq('id', expense_id).is_('deleted_at', 'null').single().execute()
        return response.data if response.data else None
    except Exception as e:
        st.error(f"❌ Error getting expense: {str(e)}")
        return None

def get_expenses_by_user(user_id: str) -> List[Dict[str, Any]]:
    """Get all expenses for a specific user"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('user_id', user_id).is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting user expenses: {str(e)}")
        return []

def get_pending_expenses() -> List[Dict[str, Any]]:
    """Get all pending expenses"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('status', 'pending').is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting pending expenses: {str(e)}")
        return []

def get_approved_expenses() -> List[Dict[str, Any]]:
    """Get all approved expenses"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('status', 'approved').is_('deleted_at', 'null').order('approved_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting approved expenses: {str(e)}")
        return []

def get_rejected_expenses() -> List[Dict[str, Any]]:
    """Get all rejected expenses"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('status', 'rejected').is_('deleted_at', 'null').order('approved_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting rejected expenses: {str(e)}")
        return []

def get_paid_expenses() -> List[Dict[str, Any]]:
    """Get all paid expenses"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('status', 'paid').is_('deleted_at', 'null').order('paid_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting paid expenses: {str(e)}")
        return []

def get_all_expenses() -> List[Dict[str, Any]]:
    """Get all expenses (for admin)"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting all expenses: {str(e)}")
        return []

def get_expenses_by_status(status: str) -> List[Dict[str, Any]]:
    """Get expenses by status"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').eq('status', status).is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting expenses by status: {str(e)}")
        return []

def get_expenses_by_date_range(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Get expenses within a date range"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').gte('created_at', start_date).lte('created_at', end_date).is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting expenses by date range: {str(e)}")
        return []

def get_expenses_by_amount_range(min_amount: float, max_amount: float) -> List[Dict[str, Any]]:
    """Get expenses within an amount range"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').gte('amount', min_amount).lte('amount', max_amount).is_('deleted_at', 'null').order('amount', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting expenses by amount range: {str(e)}")
        return []

def get_user_roles(user_id: str) -> List[str]:
    """Get roles for a specific user"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('user_roles').select('role').eq('user_id', user_id).execute()
        return [role['role'] for role in response.data]
    except Exception as e:
        st.error(f"❌ Error getting user roles: {str(e)}")
        return []

def get_users_by_role(role: str) -> List[Dict[str, Any]]:
    """Get all users with a specific role"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        # Join users and user_roles tables
        response = supabase.table('users').select('*, user_roles!inner(*)').eq('user_roles.role', role).is_('deleted_at', 'null').execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting users by role: {str(e)}")
        return []

def get_expense_statistics() -> Dict[str, Any]:
    """Get expense statistics for dashboard"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return {}
            
        # Get total expenses
        total_response = supabase.table('expenses').select('amount', count='exact').is_('deleted_at', 'null').execute()
        total_expenses = len(total_response.data) if total_response.data else 0
        
        # Get total amount
        amount_response = supabase.table('expenses').select('amount').is_('deleted_at', 'null').execute()
        total_amount = sum(expense['amount'] for expense in amount_response.data) if amount_response.data else 0
        
        # Get expenses by status
        pending_count = len(get_expenses_by_status('pending'))
        approved_count = len(get_expenses_by_status('approved'))
        rejected_count = len(get_expenses_by_status('rejected'))
        paid_count = len(get_expenses_by_status('paid'))
        
        return {
            'total_expenses': total_expenses,
            'total_amount': total_amount,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'paid_count': paid_count
        }
    except Exception as e:
        st.error(f"❌ Error getting expense statistics: {str(e)}")
        return {}

def get_recent_expenses(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent expenses"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        response = supabase.table('expenses').select('*').is_('deleted_at', 'null').order('created_at', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error getting recent expenses: {str(e)}")
        return []

def search_expenses(query: str) -> List[Dict[str, Any]]:
    """Search expenses by description or category"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []
            
        # Search in description and category fields
        response = supabase.table('expenses').select('*').or_(f'description.ilike.%{query}%,category.ilike.%{query}%').is_('deleted_at', 'null').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error searching expenses: {str(e)}")
        return [] 