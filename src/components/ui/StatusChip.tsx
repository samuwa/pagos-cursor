import React from 'react'
import { motion } from 'framer-motion'

interface StatusChipProps {
  status: 'Creado' | 'Aprobado' | 'Pagado' | 'Rechazado' | string
  size?: 'small' | 'medium' | 'large'
  className?: string
}

const StatusChip: React.FC<StatusChipProps> = ({
  status,
  size = 'medium',
  className = '',
}) => {
  const statusConfig = {
    'Creado': {
      color: 'bg-neutral-100 text-neutral-700 border-neutral-200',
      icon: '📝'
    },
    'Aprobado': {
      color: 'bg-secondary-100 text-secondary-700 border-secondary-200',
      icon: '✅'
    },
    'Pagado': {
      color: 'bg-primary-100 text-primary-700 border-primary-200',
      icon: '💰'
    },
    'Rechazado': {
      color: 'bg-danger-100 text-danger-700 border-danger-200',
      icon: '❌'
    }
  }
  
  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig['Creado']
  
  const sizeClasses = {
    small: 'px-2 py-0.5 text-xs',
    medium: 'px-3 py-1 text-sm',
    large: 'px-4 py-2 text-base'
  }
  
  const baseClasses = 'inline-flex items-center font-medium rounded-full border'
  
  const classes = [
    baseClasses,
    config.color,
    sizeClasses[size],
    className
  ].join(' ')
  
  return (
    <motion.span
      className={classes}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05 }}
    >
      <span className="mr-1">{config.icon}</span>
      {status}
    </motion.span>
  )
}

export default StatusChip 