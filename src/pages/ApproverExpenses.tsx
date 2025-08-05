import React from 'react'
import { motion } from 'framer-motion'
import ExpenseList from '../components/ExpenseList'

const ApproverExpenses: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-7xl mx-auto py-8 px-6"
    >
      <ExpenseList
        title="Mis Solicitudes"
        filterBy="my-approvals"
        showCreateButton={false}
      />
    </motion.div>
  )
}

export default ApproverExpenses 