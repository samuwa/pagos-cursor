# 📘 Database Setup Documentation

## 🎯 Overview

This folder contains the database schema and setup files for the **Pagos** expense management system.

## 📁 Files

- **`database_schema.md`** - Original database schema documentation with table definitions and relationships
- **`database_schema.sql`** - Enhanced SQL schema with all improvements and optimizations
- **`README.md`** - This documentation file

## 🗄️ Database Structure

### Core Tables
- **`users`** - User management with UUID primary keys
- **`user_roles`** - Normalized user roles (admin, payer, approver, requester, viewer)
- **`categories`** - Expense categories
- **`accounts`** - Financial accounts linked to categories
- **`receivers`** - Suppliers/vendors/receivers
- **`expenses`** - Main expense records with phases (Creado, Aprobado, Pagado, Rechazado)
- **`comments`** - User comments on expenses
- **`logs`** - System logs for audit trail
- **`quotes`** - Quote documents with file metadata
- **`people_suppliers`** - People associated with receivers
- **`reembolsos`** - Reimbursement records

### Association Tables
- **`receiver_accounts`** - Many-to-many relationship between receivers and accounts
- **`receiver_categories`** - Many-to-many relationship between receivers and categories

## 🔧 Key Features

### ✅ Implemented Improvements
- **UUID for user IDs** (compatible with Supabase Auth)
- **Custom enum types** for expense phases and user roles
- **Row Level Security (RLS)** enabled on all tables
- **Foreign key constraints** properly configured
- **Indexes** for performance optimization
- **Triggers** for automatic `updated_at` timestamps
- **Soft delete support** with `deleted_at` columns
- **File metadata** in quotes table for Supabase Storage integration

### 🎯 Database Status
- ✅ **Created successfully** in Supabase project: `xidfcnlzvcydevjtqfkz`
- ✅ **All tables** with proper relationships and constraints
- ✅ **Security policies** in place
- ✅ **Ready for application development**

## 🚀 Next Steps

1. **Initial Data**: Insert sample categories and accounts
2. **Application Development**: Start building the frontend/backend
3. **Authentication**: Integrate with Supabase Auth
4. **File Storage**: Set up Supabase Storage for quote files

## 📋 Usage

To recreate the database structure:

1. Go to your Supabase Dashboard
2. Navigate to SQL Editor
3. Copy and paste the contents of `database_schema.sql`
4. Execute the SQL

## 🔐 Security

- Row Level Security (RLS) is enabled on all tables
- User authentication will be handled through Supabase Auth
- File uploads will use Supabase Storage with proper access controls

---

**Created**: August 5, 2025  
**Status**: ✅ Complete and Ready for Development 