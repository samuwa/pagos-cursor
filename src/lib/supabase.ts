import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://xidfcnlzvcydevjtqfkz.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhpZGZjbmx6dmN5ZGV2anRxZmt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0MTU3ODcsImV4cCI6MjA2OTk5MTc4N30.fva0K84NLzHUfI--xb2s7dHisvlHEJwvXXUmeoHIkf0'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types based on our schema
export interface User {
  id: string
  name: string
  email: string | null
  stytch_user_id: string
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export interface UserRole {
  user_id: string
  role: 'admin' | 'payer' | 'approver' | 'requester' | 'viewer'
  created_at: string
}

export interface Expense {
  id: number
  amount: number
  account_id: number | null
  category_id: number
  requester_id: string
  approver_id: string | null
  payer_id: string | null
  approved_quote_id: number | null
  description: string | null
  payment_method: string | null
  payment_receipt: string | null
  phase: 'Creado' | 'Aprobado' | 'Pagado' | 'Rechazado'
  date_created: string
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export interface Category {
  id: number
  description: string
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export interface Account {
  id: number
  category_id: number
  description: string
  created_at: string
  updated_at: string
  deleted_at: string | null
}

export interface Receiver {
  id: number
  name: string
  email: string | null
  phone: string | null
  role: string | null
  created_by: string
  created_date: string
  created_at: string
  updated_at: string
  deleted_at: string | null
} 