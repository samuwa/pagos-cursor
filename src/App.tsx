import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { RoleProvider, useRole } from './contexts/RoleContext'
import Login from './components/Login'
import Navigation from './components/Navigation'
import Card from './components/ui/Card'
import ExpenseForm from './components/ExpenseForm'
import RequesterExpenses from './pages/RequesterExpenses'
import ApproverExpenses from './pages/ApproverExpenses'
import PayerExpenses from './pages/PayerExpenses'
import PaidExpenses from './pages/PaidExpenses'

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth()
  const { loading: roleLoading } = useRole()

  if (loading || roleLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

// Dashboard Component
const Dashboard: React.FC = () => {
  const { isRequester } = useRole()

  return (
    <div className="min-h-screen bg-neutral-50">
      <Navigation />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-6">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-neutral-900 mb-2">Dashboard</h2>
          <p className="text-neutral-600">Welcome to your expense management dashboard!</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mr-4">
                <span className="text-primary-600 text-xl">💰</span>
              </div>
              <div>
                <p className="text-sm font-medium text-neutral-600">Total Expenses</p>
                <p className="text-2xl font-bold text-neutral-900">$0</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-warning-100 rounded-lg flex items-center justify-center mr-4">
                <span className="text-warning-600 text-xl">⏳</span>
              </div>
              <div>
                <p className="text-sm font-medium text-neutral-600">Pending Approval</p>
                <p className="text-2xl font-bold text-neutral-900">0</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-secondary-100 rounded-lg flex items-center justify-center mr-4">
                <span className="text-secondary-600 text-xl">✅</span>
              </div>
              <div>
                <p className="text-sm font-medium text-neutral-600">Approved This Month</p>
                <p className="text-2xl font-bold text-neutral-900">$0</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="p-6">
          <h3 className="text-xl font-semibold text-neutral-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {isRequester && (
              <button className="flex items-center justify-center p-4 border-2 border-dashed border-neutral-300 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors duration-200">
                <span className="text-primary-600 font-medium">+ New Expense</span>
              </button>
            )}
            <button className="flex items-center justify-center p-4 border-2 border-dashed border-neutral-300 rounded-lg hover:border-secondary-300 hover:bg-secondary-50 transition-colors duration-200">
              <span className="text-secondary-600 font-medium">+ New Category</span>
            </button>
          </div>
        </Card>
      </main>
    </div>
  )
}

// Auth Callback Component
const AuthCallback: React.FC = () => {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Processing authentication...</div>
      </div>
    )
  }

  if (user) {
    return <Navigate to="/dashboard" replace />
  }

  return <Navigate to="/login" replace />
}

// Layout wrapper for all protected pages
const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-neutral-50">
      <Navigation />
      {children}
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <RoleProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/auth/callback" element={<AuthCallback />} />
            
            {/* Protected Routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            
            {/* Expense Routes */}
            <Route
              path="/expenses"
              element={
                <ProtectedRoute>
                  <Layout>
                    <RequesterExpenses />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/expenses/new"
              element={
                <ProtectedRoute>
                  <Layout>
                    <ExpenseForm />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/expenses/:id/edit"
              element={
                <ProtectedRoute>
                  <Layout>
                    <ExpenseForm />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            {/* Approver Routes */}
            <Route
              path="/approvals"
              element={
                <ProtectedRoute>
                  <Layout>
                    <ApproverExpenses />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            {/* Payer Routes */}
            <Route
              path="/payments"
              element={
                <ProtectedRoute>
                  <Layout>
                    <PayerExpenses />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            {/* Viewer Routes */}
            <Route
              path="/paid-expenses"
              element={
                <ProtectedRoute>
                  <Layout>
                    <PaidExpenses />
                  </Layout>
                </ProtectedRoute>
              }
            />
            
            {/* Default Route */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Router>
      </RoleProvider>
    </AuthProvider>
  )
}

export default App
