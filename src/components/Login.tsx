import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Mail, Lock, CheckCircle, AlertCircle, Shield } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { BootstrapInput as Input, BootstrapButton as Button, BootstrapCard as Card, BootstrapAlert as Alert } from './ui/BootstrapComponents'

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
    <div className="min-h-screen d-flex align-items-center justify-content-center bg-gradient-to-br from-neutral-50 to-neutral-100 py-8 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="w-100"
        style={{ maxWidth: '420px' }}
      >
        <Card className="border-0 shadow-lg" shadow="lg">
          <div className="card-body p-5">
            <motion.div 
              className="text-center mb-5"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              <div className="mx-auto mb-4 d-flex align-items-center justify-content-center" style={{ width: '80px', height: '80px' }}>
                <div className="bg-gradient-to-br from-primary-100 to-primary-200 rounded-circle d-flex align-items-center justify-content-center shadow-soft" style={{ width: '100%', height: '100%' }}>
                  <Shield className="text-primary-600" size={32} />
                </div>
              </div>
              
              <h2 className="h3 fw-bold text-neutral-900 mb-3">
                Welcome to Pagos
              </h2>
              <p className="text-neutral-600 mb-0">
                Enter your email to receive a secure login link
              </p>
            </motion.div>

            <motion.form 
              onSubmit={handleSubmit} 
              className="space-y-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              <Input
                label="Email Address"
                type="email"
                value={email}
                onChange={handleEmailChange}
                placeholder="Enter your email address"
                required
                error={error}
                disabled={loading}
                size="lg"
                className="mb-4"
              />

              <Button
                type="submit"
                loading={loading}
                disabled={loading || !email.trim()}
                variant="primary"
                size="lg"
                block
                className="mb-4"
              >
                <Mail className="me-2" size={20} />
                Send Login Link
              </Button>

              {message && (
                <Alert variant="success" className="mb-0">
                  <div className="d-flex align-items-center">
                    <CheckCircle className="me-2" size={18} />
                    <span className="fw-medium">{message}</span>
                  </div>
                </Alert>
              )}

              {error && (
                <Alert variant="danger" className="mb-0">
                  <div className="d-flex align-items-center">
                    <AlertCircle className="me-2" size={18} />
                    <span className="fw-medium">{error}</span>
                  </div>
                </Alert>
              )}
            </motion.form>

            <motion.div 
              className="mt-5 text-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.5 }}
            >
              <div className="d-flex align-items-center justify-content-center text-neutral-500">
                <Lock className="me-2" size={14} />
                <small className="fw-medium">Secure email-based authentication powered by Supabase</small>
              </div>
            </motion.div>
          </div>
        </Card>
      </motion.div>
    </div>
  )
}

export default Login 