import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Save, 
  X, 
  Upload, 
  FileText, 
  DollarSign,
  User,
  Calendar
} from 'lucide-react'
import { supabase } from '../lib/supabase'
import { useAuth } from '../contexts/AuthContext'
import { useRole } from '../contexts/RoleContext'
import Card from './ui/Card'
import Button from './ui/Button'
import Input from './ui/Input'
import StatusChip from './ui/StatusChip'

interface ExpenseFormData {
  amount: number
  description: string
  category_id: number
  account_id: number | null
  payment_method: string
  requester_id: string
  approver_id: string | null
  payer_id: string | null
  phase: 'Creado' | 'Aprobado' | 'Pagado' | 'Rechazado'
}

interface Category {
  id: number
  description: string
}

interface Account {
  id: number
  description: string
  category_id: number
}

interface User {
  id: string
  name: string
  email: string
}

const ExpenseForm: React.FC = () => {
  const navigate = useNavigate()
  const { id } = useParams()
  const { user } = useAuth()
  const { isRequester, isApprover, isPayer, isAdmin } = useRole()
  
  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [accounts, setAccounts] = useState<Account[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [formData, setFormData] = useState<ExpenseFormData>({
    amount: 0,
    description: '',
    category_id: 0,
    account_id: null,
    payment_method: '',
    requester_id: user?.id || '',
    approver_id: null,
    payer_id: null,
    phase: 'Creado'
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const isEditing = !!id

  useEffect(() => {
    fetchInitialData()
    if (isEditing) {
      fetchExpense()
    }
  }, [id])

  const fetchInitialData = async () => {
    try {
      // Fetch categories
      const { data: categoriesData } = await supabase
        .from('categories')
        .select('*')
        .order('description')

      // Fetch accounts
      const { data: accountsData } = await supabase
        .from('accounts')
        .select('*')
        .order('description')

      // Fetch users
      const { data: usersData } = await supabase
        .from('users')
        .select('*')
        .order('name')

      setCategories(categoriesData || [])
      setAccounts(accountsData || [])
      setUsers(usersData || [])
    } catch (error) {
      console.error('Error fetching initial data:', error)
    }
  }

  const fetchExpense = async () => {
    try {
      const { data, error } = await supabase
        .from('expenses')
        .select('*')
        .eq('id', id)
        .single()

      if (error) {
        console.error('Error fetching expense:', error)
        return
      }

      if (data) {
        setFormData({
          amount: data.amount,
          description: data.description || '',
          category_id: data.category_id,
          account_id: data.account_id,
          payment_method: data.payment_method || '',
          requester_id: data.requester_id,
          approver_id: data.approver_id,
          payer_id: data.payer_id,
          phase: data.phase
        })
      }
    } catch (error) {
      console.error('Error fetching expense:', error)
    }
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.amount || formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required'
    }

    if (!formData.category_id) {
      newErrors.category_id = 'Category is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      const expenseData = {
        ...formData,
        date_created: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      if (isEditing) {
        const { error } = await supabase
          .from('expenses')
          .update(expenseData)
          .eq('id', id)

        if (error) throw error
      } else {
        const { error } = await supabase
          .from('expenses')
          .insert(expenseData)

        if (error) throw error
      }

      navigate('/expenses')
    } catch (error) {
      console.error('Error saving expense:', error)
      setErrors({ submit: 'Error saving expense. Please try again.' })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: keyof ExpenseFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  const canEdit = isEditing ? 
    (isRequester && formData.requester_id === user?.id) || isAdmin :
    isRequester

  if (!canEdit) {
    return (
      <div className="max-w-7xl mx-auto py-8 px-6">
        <Card className="p-8 text-center">
          <h2 className="text-xl font-semibold text-neutral-900 mb-4">
            Access Denied
          </h2>
          <p className="text-neutral-600">
            You don't have permission to {isEditing ? 'edit' : 'create'} this expense.
          </p>
        </Card>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto py-8 px-6"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-neutral-900">
          {isEditing ? 'Edit Expense' : 'New Expense'}
        </h1>
        <p className="text-neutral-600 mt-2">
          {isEditing ? 'Update expense details' : 'Create a new expense request'}
        </p>
      </div>

      <Card className="p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Status Display */}
          {isEditing && (
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-neutral-700">Status:</span>
              <StatusChip status={formData.phase} />
            </div>
          )}

          {/* Amount */}
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
              Amount *
            </label>
            <div className="relative">
              <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
              <Input
                type="number"
                value={formData.amount.toString()}
                onChange={(value) => handleInputChange('amount', parseFloat(value) || 0)}
                placeholder="0.00"
                error={errors.amount}
                className="pl-10"
                required
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
              Description *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              placeholder="Describe the expense..."
              className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              rows={3}
              required
            />
            {errors.description && (
              <p className="mt-1 text-sm text-danger-500">{errors.description}</p>
            )}
          </div>

          {/* Category and Account */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">
                Category *
              </label>
              <select
                value={formData.category_id}
                onChange={(e) => handleInputChange('category_id', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                required
              >
                <option value="">Select a category</option>
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.description}
                  </option>
                ))}
              </select>
              {errors.category_id && (
                <p className="mt-1 text-sm text-danger-500">{errors.category_id}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">
                Account
              </label>
              <select
                value={formData.account_id || ''}
                onChange={(e) => handleInputChange('account_id', e.target.value ? parseInt(e.target.value) : null)}
                className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Select an account</option>
                {accounts
                  .filter(account => !formData.category_id || account.category_id === formData.category_id)
                  .map(account => (
                    <option key={account.id} value={account.id}>
                      {account.description}
                    </option>
                  ))}
              </select>
            </div>
          </div>

          {/* Payment Method */}
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
              Payment Method
            </label>
            <Input
              value={formData.payment_method}
              onChange={(value) => handleInputChange('payment_method', value)}
              placeholder="e.g., Credit Card, Bank Transfer, Cash"
            />
          </div>

          {/* Role-specific fields */}
          {isAdmin && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Approver
                </label>
                <select
                  value={formData.approver_id || ''}
                  onChange={(e) => handleInputChange('approver_id', e.target.value || null)}
                  className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="">Select an approver</option>
                  {users
                    .filter(u => u.id !== user?.id)
                    .map(user => (
                      <option key={user.id} value={user.id}>
                        {user.name} ({user.email})
                      </option>
                    ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Payer
                </label>
                <select
                  value={formData.payer_id || ''}
                  onChange={(e) => handleInputChange('payer_id', e.target.value || null)}
                  className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="">Select a payer</option>
                  {users
                    .filter(u => u.id !== user?.id)
                    .map(user => (
                      <option key={user.id} value={user.id}>
                        {user.name} ({user.email})
                      </option>
                    ))}
                </select>
              </div>
            </div>
          )}

          {/* Error Message */}
          {errors.submit && (
            <div className="p-4 bg-danger-50 border border-danger-200 rounded-md">
              <p className="text-danger-700">{errors.submit}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-neutral-200">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/expenses')}
            >
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
            
            <Button
              type="submit"
              loading={loading}
              disabled={loading}
            >
              <Save className="w-4 h-4 mr-2" />
              {isEditing ? 'Update Expense' : 'Create Expense'}
            </Button>
          </div>
        </form>
      </Card>
    </motion.div>
  )
}

export default ExpenseForm 