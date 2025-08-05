# 📘 Database Schema Documentation

## 🧾 Overview

This document provides a comprehensive breakdown of the relational database schema, including tables, columns, primary keys, foreign keys, and their relationships. This format is optimized for readability by both developers and large language models (LLMs).

---

## 📚 Tables

---

### Table: `users`

**Primary Key:** `id`

| Column           | Type                      | Nullable |
|------------------|---------------------------|----------|
| id               | bigint                    | NO       |
| name             | text                      | NO       |
| email            | text                      | YES      |
| is_admin         | boolean                   | NO       |
| is_payer         | boolean                   | NO       |
| is_approver      | boolean                   | NO       |
| is_requester     | boolean                   | NO       |
| is_viewer        | boolean                   | NO       |
| stytch_user_id   | text                      | NO       |
| created_at       | timestamp with time zone  | NO       |

---

### Table: `categories`

**Primary Key:** `id`

| Column      | Type         | Nullable |
|-------------|--------------|----------|
| id          | bigint       | NO       |
| description | USER-DEFINED | NO       |

---

### Table: `accounts`

**Primary Key:** `id`

| Column       | Type         | Nullable |
|--------------|--------------|----------|
| id           | bigint       | NO       |
| category_id  | bigint       | NO       |
| description  | USER-DEFINED | NO       |

---

### Table: `receivers`

**Primary Key:** `id`

| Column       | Type              | Nullable |
|--------------|-------------------|----------|
| id           | bigint            | NO       |
| name         | text              | NO       |
| email        | text              | YES      |
| phone        | text              | YES      |
| role         | character varying | YES      |
| created_by   | bigint            | NO       |
| created_date | date              | NO       |

---

### Table: `expenses`

**Primary Key:** `id`

| Column              | Type                      | Nullable |
|---------------------|---------------------------|----------|
| id                  | bigint                    | NO       |
| amount              | numeric                   | NO       |
| account_id          | bigint                    | YES      |
| category_id         | bigint                    | NO       |
| requester_id        | bigint                    | NO       |
| approver_id         | bigint                    | YES      |
| payer_id            | bigint                    | YES      |
| approved_quote_id   | bigint                    | YES      |
| is_reembolso        | boolean                   | NO       |
| description         | text                      | YES      |
| payment_method      | text                      | YES      |
| payment_receipt     | text                      | YES      |
| phase               | character varying         | YES      |
| date_created        | timestamp with time zone  | NO       |

---

### Table: `comments`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| created_by  | bigint                    | NO       |
| created_at  | timestamp with time zone  | NO       |
| content     | text                      | NO       |

---

### Table: `logs`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| created_by  | bigint                    | NO       |
| created_at  | timestamp with time zone  | NO       |
| content     | text                      | NO       |

---

### Table: `quotes`

**Primary Key:** `id`

| Column       | Type     | Nullable |
|--------------|----------|----------|
| id           | bigint   | NO       |
| expense_id   | bigint   | NO       |
| receiver_id  | bigint   | NO       |
| descripcion  | text     | YES      |
| file_path    | text     | NO       |
| total        | numeric  | NO       |

---

### Table: `people_suppliers`

**Primary Key:** `id`

| Column       | Type   | Nullable |
|--------------|--------|----------|
| id           | bigint | NO       |
| receiver_id  | bigint | NO       |
| email        | text   | YES      |
| phone        | text   | YES      |
| title        | text   | YES      |

---

### Table: `reembolsos`

**Primary Key:** `id`

| Column      | Type                      | Nullable |
|-------------|---------------------------|----------|
| id          | bigint                    | NO       |
| expense_id  | bigint                    | NO       |
| receiver_id | bigint                    | NO       |
| created_by  | bigint                    | NO       |
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
| receiver_accounts  | receiver_id      | receivers        | id                |
| receiver_accounts  | account_id       | accounts         | id                |
| receiver_categories| receiver_id      | receivers        | id                |
| receiver_categories| category_id      | categories       | id                |
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

---

## ⚠️ Notes

- `pg_stat_statements` and `pg_stat_statements_info` are PostgreSQL system performance views and are not part of the application's business domain.
- Composite primary keys are used for associative (many-to-many) tables like `receiver_accounts` and `receiver_categories`.

---
