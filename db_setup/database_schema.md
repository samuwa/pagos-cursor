# 📘 Database Schema Documentation

## 🧾 Overview

This document provides a comprehensive breakdown of the relational database schema, including tables, columns, primary keys, foreign keys, and their relationships. This format is optimized for readability by both developers and large language models (LLMs).

---

## 🎯 Custom Types

- **`expense_phase`** ENUM: `'Creado'`, `'Aprobado'`, `'Pagado'`, `'Rechazado'`
- **`user_role`** ENUM: `'admin'`, `'payer'`, `'approver'`, `'requester'`, `'viewer'`

---

## 📚 Tables

---

### Table: `users`

**Primary Key:** `id`

| Column           | Type                      | Nullable |
|------------------|---------------------------|----------|
| id               | uuid                      | NO       |
| name             | text                      | NO       |
| email            | text                      | YES      |
| created_at       | timestamp with time zone  | NO       |
| updated_at       | timestamp with time zone  | NO       |
| deleted_at       | timestamp with time zone  | YES      |

---

### Table: `user_roles`

**Primary Key (Composite):** `user_id`, `role`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| user_id     | uuid                      | NO       |
| role        | user_role                 | NO       |
| created_at  | timestamp with time zone  | NO       |

---

### Table: `categories`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| description | varchar(255)              | NO       |
| created_at  | timestamp with time zone  | NO       |
| updated_at  | timestamp with time zone  | NO       |
| deleted_at  | timestamp with time zone  | YES      |

---

### Table: `accounts`

**Primary Key:** `id`

| Column       | Type                      | Nullable |
|--------------|---------------------------|----------|
| id           | bigint                    | NO       |
| category_id  | bigint                    | NO       |
| description  | varchar(255)              | NO       |
| created_at   | timestamp with time zone  | NO       |
| updated_at   | timestamp with time zone  | NO       |
| deleted_at   | timestamp with time zone  | YES      |

---

### Table: `receivers`

**Primary Key:** `id`

| Column       | Type                      | Nullable |
|--------------|---------------------------|----------|
| id           | bigint                    | NO       |
| name         | text                      | NO       |
| email        | text                      | YES      |
| phone        | text                      | YES      |
| role         | varchar(100)              | YES      |
| created_by   | uuid                      | NO       |
| created_date | date                      | NO       |
| created_at   | timestamp with time zone  | NO       |
| updated_at   | timestamp with time zone  | NO       |
| deleted_at   | timestamp with time zone  | YES      |

---

### Table: `expenses`

**Primary Key:** `id`

| Column              | Type                      | Nullable |
|---------------------|---------------------------|----------|
| id                  | bigint                    | NO       |
| amount              | numeric(10,2)             | NO       |
| account_id          | bigint                    | YES      |
| category_id         | bigint                    | NO       |
| requester_id        | uuid                      | NO       |
| approver_id         | uuid                      | YES      |
| payer_id            | uuid                      | YES      |
| approved_quote_id   | bigint                    | YES      |
| description         | text                      | YES      |
| payment_method      | text                      | YES      |
| payment_receipt     | text                      | YES      |
| phase               | expense_phase             | YES      |
| date_created        | timestamp with time zone  | NO       |
| created_at          | timestamp with time zone  | NO       |
| updated_at          | timestamp with time zone  | NO       |
| deleted_at          | timestamp with time zone  | YES      |

---

### Table: `comments`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| created_by  | uuid                      | NO       |
| created_at  | timestamp with time zone  | NO       |
| content     | text                      | NO       |

---

### Table: `logs`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| created_by  | uuid                      | NO       |
| created_at  | timestamp with time zone  | NO       |
| content     | text                      | NO       |

---

### Table: `quotes`

**Primary Key:** `id`

| Column       | Type                      | Nullable |
|--------------|---------------------------|----------|
| id           | bigint                    | NO       |
| expense_id   | bigint                    | NO       |
| receiver_id  | bigint                    | NO       |
| descripcion  | text                      | YES      |
| file_url     | text                      | NO       |
| file_name    | text                      | YES      |
| file_size    | bigint                    | YES      |
| total        | numeric(10,2)             | NO       |
| uploaded_at  | timestamp with time zone  | NO       |
| created_at   | timestamp with time zone  | NO       |
| updated_at   | timestamp with time zone  | NO       |

---

### Table: `people_suppliers`

**Primary Key:** `id`

| Column       | Type                      | Nullable |
|--------------|---------------------------|----------|
| id           | bigint                    | NO       |
| receiver_id  | bigint                    | NO       |
| email        | text                      | YES      |
| phone        | text                      | YES      |
| title        | text                      | YES      |
| created_at   | timestamp with time zone  | NO       |
| updated_at   | timestamp with time zone  | NO       |

---

### Table: `reembolsos`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| receiver_id | bigint                    | NO       |
| created_by  | uuid                      | NO       |
| created_at  | timestamp with time zone  | NO       |

---

### Table: `receiver_accounts`

**Primary Key (Composite):** `receiver_id`, `account_id`

| Column       | Type   | Nullable |
|--------------|--------|----------|
| receiver_id  | bigint | NO       |
| account_id   | bigint | NO       |

---

### Table: `receiver_categories`

**Primary Key (Composite):** `receiver_id`, `category_id`

| Column       | Type   | Nullable |
|--------------|--------|----------|
| receiver_id  | bigint | NO       |
| category_id  | bigint | NO       |

---

## 🔗 Foreign Keys

| Table              | Column           | References Table | References Column |
|--------------------|------------------|------------------|-------------------|
| user_roles         | user_id          | users            | id                |
| accounts           | category_id      | categories       | id                |
| receivers          | created_by       | users            | id                |
| expenses           | account_id       | accounts         | id                |
| expenses           | category_id      | categories       | id                |
| expenses           | requester_id     | users            | id                |
| expenses           | approver_id      | users            | id                |
| expenses           | payer_id         | users            | id                |
| expenses           | approved_quote_id| quotes           | id                |
| comments           | expense_id       | expenses         | id                |
| comments           | created_by       | users            | id                |
| logs               | expense_id       | expenses         | id                |
| logs               | created_by       | users            | id                |
| quotes             | expense_id       | expenses         | id                |
| quotes             | receiver_id      | receivers        | id                |
| people_suppliers   | receiver_id      | receivers        | id                |
| reembolsos         | expense_id       | expenses         | id                |
| reembolsos         | receiver_id      | receivers        | id                |
| reembolsos         | created_by       | users            | id                |
| receiver_accounts  | receiver_id      | receivers        | id                |
| receiver_accounts  | account_id       | accounts         | id                |
| receiver_categories| receiver_id      | receivers        | id                |
| receiver_categories| category_id      | categories       | id                |

---

## ⚠️ Notes

- `pg_stat_statements` and `pg_stat_statements_info` are PostgreSQL system performance views and are not part of the application's business domain.
- Composite primary keys are used for associative (many-to-many) tables like `receiver_accounts` and `receiver_categories`.
- User roles are now normalized in the `user_roles` table instead of boolean flags in the `users` table.
- UUID is used for user IDs to be compatible with Supabase Auth.
- Reimbursements are tracked in the separate `reembolsos` table instead of a boolean flag in expenses.
- All tables include `created_at`, `updated_at`, and `deleted_at` timestamps for audit trails and soft deletes.
- Custom enum types are used for expense phases and user roles.

---
