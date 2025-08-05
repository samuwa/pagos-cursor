import React from 'react'
import { motion } from 'framer-motion'

// Bootstrap-like Button Component
interface BootstrapButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark' | 'link'
  size?: 'sm' | 'md' | 'lg'
  outline?: boolean
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
  block?: boolean
}

export const BootstrapButton: React.FC<BootstrapButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  outline = false,
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className = '',
  block = false,
}) => {
  const baseClasses = 'btn font-weight-bold border-0 rounded-pill transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 d-inline-flex align-items-center justify-content-center'
  
  const variantClasses = {
    primary: outline ? 'btn-outline-primary' : 'btn-primary',
    secondary: outline ? 'btn-outline-secondary' : 'btn-secondary',
    success: outline ? 'btn-outline-success' : 'btn-success',
    danger: outline ? 'btn-outline-danger' : 'btn-danger',
    warning: outline ? 'btn-outline-warning' : 'btn-warning',
    info: outline ? 'btn-outline-info' : 'btn-info',
    light: outline ? 'btn-outline-light' : 'btn-light',
    dark: outline ? 'btn-outline-dark' : 'btn-dark',
    link: 'btn-link',
  }
  
  const sizeClasses = {
    sm: 'btn-sm px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'btn-lg px-6 py-3 text-lg',
  }
  
  const blockClass = block ? 'w-100' : ''
  const disabledClass = disabled || loading ? 'disabled opacity-60 cursor-not-allowed' : ''
  
  const classes = [
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    blockClass,
    disabledClass,
    className
  ].filter(Boolean).join(' ')
  
  return (
    <motion.button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
      whileHover={!disabled && !loading ? { scale: 1.02, y: -1 } : {}}
      whileTap={!disabled && !loading ? { scale: 0.98 } : {}}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {loading ? (
        <div className="d-flex align-items-center">
          <div className="spinner-border spinner-border-sm me-2" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </motion.button>
  )
}

// Bootstrap-like Card Component
interface BootstrapCardProps {
  children: React.ReactNode
  className?: string
  shadow?: 'sm' | 'md' | 'lg' | 'xl' | 'none'
  border?: boolean
  hoverable?: boolean
}

export const BootstrapCard: React.FC<BootstrapCardProps> = ({
  children,
  className = '',
  shadow = 'md',
  border = true,
  hoverable = false,
}) => {
  const shadowClass = shadow !== 'none' ? `shadow-${shadow}` : ''
  const borderClass = border ? 'border' : 'border-0'
  const hoverClass = hoverable ? 'cursor-pointer hover:shadow-lg transition-shadow duration-200' : ''
  
  const classes = [
    'card',
    shadowClass,
    borderClass,
    hoverClass,
    className
  ].filter(Boolean).join(' ')
  
  const Component = hoverable ? motion.div : 'div'
  const motionProps = hoverable ? { whileHover: { y: -2 }, whileTap: { scale: 0.98 } } : {}
  
  return (
    <Component className={classes} {...motionProps}>
      {children}
    </Component>
  )
}

// Bootstrap-like Input Component
interface BootstrapInputProps {
  label?: string
  placeholder?: string
  value: string
  onChange: (value: string) => void
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url'
  error?: string
  disabled?: boolean
  required?: boolean
  className?: string
  size?: 'sm' | 'md' | 'lg'
  floating?: boolean
}

export const BootstrapInput: React.FC<BootstrapInputProps> = ({
  label,
  placeholder,
  value,
  onChange,
  type = 'text',
  error,
  disabled = false,
  required = false,
  className = '',
  size = 'md',
  floating = false,
}) => {
  const baseClasses = 'form-control border-0 rounded-pill transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const sizeClasses = {
    sm: 'form-control-sm px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'form-control-lg px-5 py-3 text-lg',
  }
  
  const stateClasses = error 
    ? 'border-danger bg-danger-50 focus:ring-danger-500' 
    : 'border-neutral-200 bg-white hover:border-neutral-300 focus:ring-primary-500'
  
  const disabledClass = disabled ? 'opacity-60 cursor-not-allowed bg-neutral-50' : ''
  
  const classes = [
    baseClasses,
    sizeClasses[size],
    stateClasses,
    disabledClass,
    className
  ].filter(Boolean).join(' ')
  
  return (
    <div className="form-group mb-3">
      {label && !floating && (
        <motion.label 
          className="form-label fw-semibold text-neutral-700 mb-2 d-block"
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {label}
          {required && <span className="text-danger ms-1">*</span>}
        </motion.label>
      )}
      
      <div className="position-relative">
        <motion.input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={floating ? ' ' : placeholder}
          disabled={disabled}
          required={required}
          className={classes}
          whileFocus={!disabled ? { scale: 1.01 } : {}}
          whileHover={!disabled ? { scale: 1.005 } : {}}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        />
        
        {floating && label && (
          <motion.label 
            className={`form-floating-label position-absolute ${value ? 'active' : ''}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {label}
            {required && <span className="text-danger ms-1">*</span>}
          </motion.label>
        )}
      </div>
      
      {error && (
        <motion.div 
          className="invalid-feedback d-block mt-2"
          initial={{ opacity: 0, y: -5, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.2 }}
        >
          {error}
        </motion.div>
      )}
    </div>
  )
}

// Bootstrap-like Alert Component
interface BootstrapAlertProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
  dismissible?: boolean
  onDismiss?: () => void
  className?: string
}

export const BootstrapAlert: React.FC<BootstrapAlertProps> = ({
  children,
  variant = 'primary',
  dismissible = false,
  onDismiss,
  className = '',
}) => {
  const classes = [
    'alert',
    `alert-${variant}`,
    dismissible ? 'alert-dismissible' : '',
    className
  ].filter(Boolean).join(' ')
  
  return (
    <motion.div 
      className={classes}
      initial={{ opacity: 0, y: -10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.95 }}
      transition={{ duration: 0.3 }}
    >
      {children}
      {dismissible && (
        <button
          type="button"
          className="btn-close"
          onClick={onDismiss}
          aria-label="Close"
        />
      )}
    </motion.div>
  )
}

// Bootstrap-like Badge Component
interface BootstrapBadgeProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark'
  size?: 'sm' | 'md' | 'lg'
  pill?: boolean
  className?: string
}

export const BootstrapBadge: React.FC<BootstrapBadgeProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  pill = false,
  className = '',
}) => {
  const sizeClasses = {
    sm: 'badge-sm px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'badge-lg px-3 py-1.5 text-base',
  }
  
  const pillClass = pill ? 'rounded-pill' : 'rounded'
  
  const classes = [
    'badge',
    `badge-${variant}`,
    sizeClasses[size],
    pillClass,
    className
  ].filter(Boolean).join(' ')
  
  return (
    <motion.span
      className={classes}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.span>
  )
}

// Bootstrap-like Spinner Component
interface BootstrapSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark'
  className?: string
}

export const BootstrapSpinner: React.FC<BootstrapSpinnerProps> = ({
  size = 'md',
  variant = 'primary',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'spinner-border-sm',
    md: '',
    lg: 'spinner-border-lg',
  }
  
  const classes = [
    'spinner-border',
    `text-${variant}`,
    sizeClasses[size],
    className
  ].filter(Boolean).join(' ')
  
  return (
    <div className={classes} role="status">
      <span className="visually-hidden">Loading...</span>
    </div>
  )
}

// Bootstrap-like Progress Component
interface BootstrapProgressProps {
  value: number
  max?: number
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
  striped?: boolean
  animated?: boolean
  height?: string
  className?: string
}

export const BootstrapProgress: React.FC<BootstrapProgressProps> = ({
  value,
  max = 100,
  variant = 'primary',
  striped = false,
  animated = false,
  height = '1rem',
  className = '',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const classes = [
    'progress',
    className
  ].filter(Boolean).join(' ')
  
  const barClasses = [
    'progress-bar',
    `bg-${variant}`,
    striped ? 'progress-bar-striped' : '',
    animated ? 'progress-bar-animated' : '',
  ].filter(Boolean).join(' ')
  
  return (
    <div className={classes} style={{ height }}>
      <motion.div
        className={barClasses}
        style={{ width: `${percentage}%` }}
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        {percentage > 10 && `${Math.round(percentage)}%`}
      </motion.div>
    </div>
  )
}

// Export all components
export {
  BootstrapButton as Button,
  BootstrapCard as Card,
  BootstrapInput as Input,
  BootstrapAlert as Alert,
  BootstrapBadge as Badge,
  BootstrapSpinner as Spinner,
  BootstrapProgress as Progress,
} 