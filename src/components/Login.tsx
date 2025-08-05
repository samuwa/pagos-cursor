import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Mail, Lock, CheckCircle, AlertCircle } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import Input from './ui/Input'
import Button from './ui/Button'
import Card from './ui/Card'

const Login: React.FC = () => {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const { signIn } = useAuth()

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Clear previous messages
    setMessage('')
    setError('')

    // Validate email
    if (!email.trim()) {
      setError('Email is required')
      return
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address')
      return
    }

    setLoading(true)

    try {
      await signIn(email)
      setMessage('Check your email for the login link!')
      setEmail('') // Clear email field after successful submission
    } catch (error) {
      setError('Error sending login link. Please try again.')
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEmailChange = (value: string) => {
    setEmail(value)
    // Clear error when user starts typing
    if (error) {
      setError('')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-50 to-neutral-100 py-8 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="w-full max-w-md"
      >
        <Card className="p-8 shadow-medium border-0">
          <motion.div 
            className="text-center mb-8"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="mx-auto h-16 w-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex items-center justify-center mb-6 shadow-soft">
              <Lock className="h-8 w-8 text-primary-600" />
            </div>
            <h2 className="text-3xl font-bold text-neutral-900 mb-3">
              Welcome to Pagos
            </h2>
            <p className="text-neutral-600 text-base leading-relaxed">
              Enter your email to receive a secure login link
            </p>
          </motion.div>

          <motion.form 
            onSubmit={handleSubmit} 
            className="space-y-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <div className="space-y-2">
              <Input
                label="Email Address"
                type="email"
                value={email}
                onChange={handleEmailChange}
                placeholder="Enter your email address"
                required
                error={error}
                disabled={loading}
                className="text-base"
              />
            </div>

            <Button
              type="submit"
              loading={loading}
              disabled={loading || !email.trim()}
              className="w-full h-12 text-base font-semibold"
              size="large"
            >
              <Mail className="w-5 h-5 mr-2" />
              Send Login Link
            </Button>

            {message && (
              <motion.div
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.3 }}
                className="flex items-center justify-center p-4 rounded-lg bg-secondary-50 text-secondary-700 border border-secondary-200"
              >
                <CheckCircle className="w-5 h-5 mr-2 text-secondary-600" />
                <span className="text-sm font-medium">{message}</span>
              </motion.div>
            )}

            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.3 }}
                className="flex items-center justify-center p-4 rounded-lg bg-danger-50 text-danger-700 border border-danger-200"
              >
                <AlertCircle className="w-5 h-5 mr-2 text-danger-600" />
                <span className="text-sm font-medium">{error}</span>
              </motion.div>
            )}
          </motion.form>

          <motion.div 
            className="mt-8 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            <p className="text-xs text-neutral-500">
              Secure email-based authentication powered by Supabase
            </p>
          </motion.div>
        </Card>
      </motion.div>
    </div>
  )
}

export default Login 