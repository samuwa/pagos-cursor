import React from 'react'
import { motion } from 'framer-motion'

interface InputProps {
  label?: string
  placeholder?: string
  value: string
  onChange: (value: string) => void
  type?: 'text' | 'email' | 'password' | 'number'
  error?: string
  disabled?: boolean
  required?: boolean
  className?: string
}

const Input: React.FC<InputProps> = ({
  label,
  placeholder,
  value,
  onChange,
  type = 'text',
  error,
  disabled = false,
  required = false,
  className = '',
}) => {
  const baseClasses = 'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 text-base'
  
  const stateClasses = error 
    ? 'border-danger-500 focus:ring-danger-500 focus:border-danger-500 bg-danger-50' 
    : 'border-neutral-200 focus:ring-primary-500 focus:border-primary-500 bg-white hover:border-neutral-300'
  
  const disabledClasses = disabled ? 'opacity-60 cursor-not-allowed bg-neutral-50 border-neutral-200' : ''
  
  const classes = [
    baseClasses,
    stateClasses,
    disabledClasses,
    className
  ].filter(Boolean).join(' ')
  
  return (
    <div className="w-full">
      {label && (
        <motion.label 
          className="block text-sm font-semibold text-neutral-700 mb-2"
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {label}
          {required && <span className="text-danger-500 ml-1">*</span>}
        </motion.label>
      )}
      <motion.input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        className={classes}
        whileFocus={!disabled ? { scale: 1.01 } : {}}
        whileHover={!disabled ? { scale: 1.005 } : {}}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      />
      {error && (
        <motion.p 
          className="mt-2 text-sm text-danger-600 font-medium"
          initial={{ opacity: 0, y: -5, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.2 }}
        >
          {error}
        </motion.p>
      )}
    </div>
  )
}

export default Input 