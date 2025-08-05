import React from 'react'
import { motion } from 'framer-motion'

interface CardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  hoverable = false,
}) => {
  const baseClasses = 'bg-white rounded-lg border border-neutral-200 shadow-soft p-4'
  const hoverClasses = hoverable ? 'cursor-pointer hover:shadow-medium hover:border-neutral-300' : ''
  
  const classes = [
    baseClasses,
    hoverClasses,
    className
  ].filter(Boolean).join(' ')
  
  const Component = onClick || hoverable ? motion.div : 'div'
  const motionProps = onClick || hoverable ? {
    whileHover: { y: -2 },
    whileTap: { scale: 0.98 },
    onClick
  } : {}
  
  return (
    <Component className={classes} {...motionProps}>
      {children}
    </Component>
  )
}

export default Card 