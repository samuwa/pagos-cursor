import React, { createContext, useContext, useEffect, useState } from 'react'
import { useAuth } from './AuthContext'
import { supabase } from '../lib/supabase'

interface UserRole {
  user_id: string
  role: 'admin' | 'requester' | 'approver' | 'payer' | 'viewer'
  created_at: string
}

interface RoleContextType {
  roles: UserRole[]
  loading: boolean
  hasRole: (role: string) => boolean
  isAdmin: boolean
  isRequester: boolean
  isApprover: boolean
  isPayer: boolean
  isViewer: boolean
}

const RoleContext = createContext<RoleContextType | undefined>(undefined)

export const useRole = () => {
  const context = useContext(RoleContext)
  if (context === undefined) {
    throw new Error('useRole must be used within a RoleProvider')
  }
  return context
}

interface RoleProviderProps {
  children: React.ReactNode
}

export const RoleProvider: React.FC<RoleProviderProps> = ({ children }) => {
  const { user } = useAuth()
  const [roles, setRoles] = useState<UserRole[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchUserRoles()
    } else {
      setRoles([])
      setLoading(false)
    }
  }, [user])

  const fetchUserRoles = async () => {
    try {
      const { data, error } = await supabase
        .from('user_roles')
        .select('*')
        .eq('user_id', user?.id)

      if (error) {
        console.error('Error fetching roles:', error)
        return
      }

      setRoles(data || [])
    } catch (error) {
      console.error('Error fetching roles:', error)
    } finally {
      setLoading(false)
    }
  }

  const hasRole = (role: string) => {
    return roles.some(r => r.role === role)
  }

  const isAdmin = hasRole('admin')
  const isRequester = hasRole('requester')
  const isApprover = hasRole('approver')
  const isPayer = hasRole('payer')
  const isViewer = hasRole('viewer')

  const value = {
    roles,
    loading,
    hasRole,
    isAdmin,
    isRequester,
    isApprover,
    isPayer,
    isViewer,
  }

  return <RoleContext.Provider value={value}>{children}</RoleContext.Provider>
} 