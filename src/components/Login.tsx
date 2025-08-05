import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Mail, Lock } from 'lucide-react'
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    try {
      await signIn(email)
      setMessage('Check your email for the login link!')
    } catch (error) {
      setError('Error sending login link. Please try again.')
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full"
      >
        <Card className="p-8">
          <div className="text-center mb-8">
            <div className="mx-auto h-12 w-12 bg-primary-100 rounded-full flex items-center justify-center mb-4">
              <Lock className="h-6 w-6 text-primary-600" />
            </div>
            <h2 className="text-3xl font-bold text-neutral-900 mb-2">
              Welcome to Pagos
            </h2>
            <p className="text-neutral-600">
              Enter your email to receive a secure login link
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Email Address"
              type="email"
              value={email}
              onChange={setEmail}
              placeholder="Enter your email address"
              required
              error={error}
            />

            <Button
              type="submit"
              loading={loading}
              disabled={loading}
              className="w-full"
              size="large"
            >
              <Mail className="w-4 h-4 mr-2" />
              Send Login Link
            </Button>

            {message && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`text-sm text-center p-3 rounded-md ${
                  message.includes('Error') 
                    ? 'bg-danger-50 text-danger-700 border border-danger-200' 
                    : 'bg-secondary-50 text-secondary-700 border border-secondary-200'
                }`}
              >
                {message}
              </motion.div>
            )}
          </form>
        </Card>
      </motion.div>
    </div>
  )
}

export default Login 