import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Login from './components/Login'
import Card from './components/ui/Card'

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) {
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

// Dashboard Component (placeholder)
const Dashboard: React.FC = () => {
  const { user, signOut } = useAuth()

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white shadow-medium border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center">
                <div className="h-8 w-8 bg-primary-500 rounded-lg flex items-center justify-center mr-3">
                  <span className="text-white font-bold text-lg">P</span>
                </div>
                <h1 className="text-xl font-bold text-neutral-900">Pagos</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-primary-600 font-medium text-sm">
                    {user?.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <span className="text-neutral-700 text-sm font-medium">{user?.email}</span>
              </div>
              <button
                onClick={signOut}
                className="bg-danger-500 hover:bg-danger-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

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
            <button className="flex items-center justify-center p-4 border-2 border-dashed border-neutral-300 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors duration-200">
              <span className="text-primary-600 font-medium">+ New Expense</span>
            </button>
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

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
