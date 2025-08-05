import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Search, 
  Plus, 
  Eye, 
  Edit, 
  CheckCircle, 
  DollarSign,
  FileText
} from 'lucide-react'
import { supabase } from '../lib/supabase'
import { useRole } from '../contexts/RoleContext'
import { useAuth } from '../contexts/AuthContext'
import Card from './ui/Card'
import Button from './ui/Button'
import StatusChip from './ui/StatusChip'
import Input from './ui/Input'

interface Expense {
  id: number
  amount: number
  description: string | null
  phase: 'Creado' | 'Aprobado' | 'Pagado' | 'Rechazado'
  date_created: string
  requester_id: string
  approver_id: string | null
  payer_id: string | null
  category_id: number
  account_id: number | null
  created_at: string
}

interface ExpenseListProps {
  title: string
  filterBy?: 'my-requests' | 'my-approvals' | 'my-payments' | 'all'
  showCreateButton?: boolean
}

const ExpenseList: React.FC<ExpenseListProps> = ({ 
  title, 
  filterBy = 'all',
  showCreateButton = false 
}) => {
  const { user } = useAuth()
  const { isRequester, isApprover, isPayer, isAdmin } = useRole()
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')

  useEffect(() => {
    fetchExpenses()
  }, [filterBy])

  const fetchExpenses = async () => {
    try {
      setLoading(true)
      let query = supabase
        .from('expenses')
        .select(`
          *,
          categories(description),
          accounts(description),
          users!expenses_requester_id_fkey(name, email)
        `)
        .order('created_at', { ascending: false })

      // Apply role-based filters
      switch (filterBy) {
        case 'my-requests':
          query = query.eq('requester_id', user?.id)
          break
        case 'my-approvals':
          query = query.eq('approver_id', user?.id)
          break
        case 'my-payments':
          query = query.eq('payer_id', user?.id)
          break
        case 'all':
        default:
          // No additional filter
          break
      }

      const { data, error } = await query

      if (error) {
        console.error('Error fetching expenses:', error)
        return
      }

      setExpenses(data || [])
    } catch (error) {
      console.error('Error fetching expenses:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredExpenses = expenses.filter(expense => {
    const matchesSearch = expense.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         expense.amount.toString().includes(searchTerm)
    const matchesStatus = statusFilter === 'all' || expense.phase === statusFilter
    return matchesSearch && matchesStatus
  })

  const getActionButton = (expense: Expense) => {
    const canEdit = expense.phase === 'Creado' && 
                   ((isRequester && expense.requester_id === user?.id) || isAdmin)
    const canApprove = expense.phase === 'Creado' && isApprover && expense.requester_id !== user?.id
    const canPay = expense.phase === 'Aprobado' && isPayer

    if (canEdit) {
      return (
        <Link to={`/expenses/${expense.id}/edit`}>
          <Button size="small" variant="secondary">
            <Edit className="w-4 h-4 mr-1" />
            Edit
          </Button>
        </Link>
      )
    }

    if (canApprove) {
      return (
        <Link to={`/expenses/${expense.id}/approve`}>
          <Button size="small" variant="primary">
            <CheckCircle className="w-4 h-4 mr-1" />
            Approve
          </Button>
        </Link>
      )
    }

    if (canPay) {
      return (
        <Link to={`/expenses/${expense.id}/pay`}>
          <Button size="small" variant="secondary">
            <DollarSign className="w-4 h-4 mr-1" />
            Pay
          </Button>
        </Link>
      )
    }

    return (
      <Link to={`/expenses/${expense.id}`}>
        <Button size="small" variant="secondary">
          <Eye className="w-4 h-4 mr-1" />
          View
        </Button>
      </Link>
    )
  }

  const statusOptions = [
    { value: 'all', label: 'All Status' },
    { value: 'Creado', label: 'Created' },
    { value: 'Aprobado', label: 'Approved' },
    { value: 'Pagado', label: 'Paid' },
    { value: 'Rechazado', label: 'Rejected' }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-neutral-900">{title}</h1>
          <p className="text-neutral-600 mt-1">
            {filteredExpenses.length} expense{filteredExpenses.length !== 1 ? 's' : ''} found
          </p>
        </div>
        
        {showCreateButton && (
          <Link to="/expenses/new">
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              New Expense
            </Button>
          </Link>
        )}
      </div>

      {/* Filters */}
      <Card className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
              <Input
                value={searchTerm}
                onChange={setSearchTerm}
                placeholder="Search expenses..."
                className="pl-10"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
              Status
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-neutral-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              {statusOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      {/* Expense List */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
        </div>
      ) : filteredExpenses.length === 0 ? (
        <Card className="p-12 text-center">
          <div className="text-neutral-500">
            <FileText className="h-12 w-12 mx-auto mb-4 text-neutral-300" />
            <h3 className="text-lg font-medium text-neutral-900 mb-2">No expenses found</h3>
            <p className="text-neutral-600">
              {searchTerm || statusFilter !== 'all' 
                ? 'Try adjusting your filters'
                : 'Get started by creating your first expense'
              }
            </p>
          </div>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredExpenses.map((expense) => (
            <motion.div
              key={expense.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="p-6 hoverable">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4">
                      <div className="flex-shrink-0">
                        <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center">
                          <DollarSign className="h-6 w-6 text-primary-600" />
                        </div>
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="text-lg font-semibold text-neutral-900">
                            ${expense.amount.toLocaleString()}
                          </h3>
                          <StatusChip status={expense.phase} size="small" />
                        </div>
                        
                        <p className="text-neutral-600 text-sm mb-1">
                          {expense.description || 'No description'}
                        </p>
                        
                        <div className="flex items-center space-x-4 text-xs text-neutral-500">
                          <span>Created: {new Date(expense.date_created).toLocaleDateString()}</span>
                          {expense.requester_id && (
                            <span>Requester: {expense.requester_id}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-4">
                    {getActionButton(expense)}
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ExpenseList 