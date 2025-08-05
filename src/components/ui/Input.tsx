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
  const baseClasses = 'w-full px-3 py-2 border rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const stateClasses = error 
    ? 'border-danger-500 focus:ring-danger-500 focus:border-danger-500' 
    : 'border-neutral-200 focus:ring-primary-500 focus:border-primary-500'
  
  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed bg-neutral-50' : ''
  
  const classes = [
    baseClasses,
    stateClasses,
    disabledClasses,
    className
  ].filter(Boolean).join(' ')
  
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-neutral-700 mb-1">
          {label}
          {required && <span className="text-danger-500 ml-1">*</span>}
        </label>
      )}
      <motion.input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        className={classes}
        whileFocus={{ scale: 1.01 }}
      />
      {error && (
        <motion.p 
          className="mt-1 text-sm text-danger-500"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {error}
        </motion.p>
      )}
    </div>
  )
}

export default Input 