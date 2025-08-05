import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Home, 
  FileText, 
  CheckCircle, 
  DollarSign, 
  Users, 
  Settings, 
  LogOut,
  Menu,
  X
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useRole } from '../contexts/RoleContext'
import Button from './ui/Button'

const Navigation: React.FC = () => {
  const { user, signOut } = useAuth()
  const { isAdmin, isRequester, isApprover, isPayer, isViewer } = useRole()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigationItems = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: Home,
      show: true
    },
    {
      name: 'Mis Solicitudes',
      href: '/expenses',
      icon: FileText,
      show: isRequester || isApprover || isPayer
    },
    {
      name: 'Solicitudes Pagadas',
      href: '/paid-expenses',
      icon: CheckCircle,
      show: isViewer || isPayer
    },
    {
      name: 'Pagos',
      href: '/payments',
      icon: DollarSign,
      show: isPayer
    },
    {
      name: 'Usuarios',
      href: '/users',
      icon: Users,
      show: isAdmin
    },
    {
      name: 'Configuración',
      href: '/settings',
      icon: Settings,
      show: isAdmin
    }
  ].filter(item => item.show)

  const handleSignOut = async () => {
    try {
      await signOut()
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }

  return (
    <nav className="bg-white shadow-medium border-b border-neutral-200">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center">
              <div className="h-8 w-8 bg-primary-500 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-lg">P</span>
              </div>
              <h1 className="text-xl font-bold text-neutral-900">Pagos</h1>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigationItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.href
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2">
              <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 font-medium text-sm">
                  {user?.email?.charAt(0).toUpperCase()}
                </span>
              </div>
              <span className="text-neutral-700 text-sm font-medium">{user?.email}</span>
            </div>
            
            <Button
              variant="danger"
              size="small"
              onClick={handleSignOut}
              className="hidden md:flex"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-md text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden border-t border-neutral-200 bg-white"
        >
          <div className="px-4 py-4 space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.href
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
            
            <div className="pt-4 border-t border-neutral-200">
              <div className="flex items-center space-x-3 px-3 py-2">
                <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-primary-600 font-medium text-sm">
                    {user?.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <span className="text-neutral-700 text-sm font-medium">{user?.email}</span>
              </div>
              
              <Button
                variant="danger"
                size="small"
                onClick={handleSignOut}
                className="w-full mt-2"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </div>
        </motion.div>
      )}
    </nav>
  )
}

export default Navigation 