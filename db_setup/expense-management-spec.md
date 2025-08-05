
# 🧾 Expense Management App — System Specification

---

## 📌 Overview

A platform to manage expense requests (solicitudes), allowing users to create, review, approve, reject, pay, and track expenses. The system supports role-based access and logging for auditing and accountability.

---

## 🧱 Expense Structure

### Expense (Solicitud)
- **Requester** (creator)
- **Categories** (multi)
- **Accounts** (multi, must belong to selected categories)
- **Quotes** (multiple)
  - Each quote includes:
    - Receiver
    - Amount
    - Notes (optional)
    - File (PDF, optional; stored in Supabase)
- **Selected Receiver** (chosen from one of the quotes during approval)
- **is_received** (boolean, editable any time)
  - Optional proof image/file
- **Status**: created → approved → paid (or declined)

---

## 🗂️ Supabase File Storage

- Files are uploaded to Supabase and stored under:
  ```
  /quotes/{quote_id}/{filename}.pdf
  ```
- Linked to `quotes` table via `file_path`

---

## 📋 Logging and Comments

### Logs (auto-generated)
- `Solicitud creada`
- `Nueva cotización de proveedor {receiver_name} agregada`
- `Solicitud aprobada`
- `Solicitud rechazada`
- `Solicitud regresada de rechazada a creada`
- `Solicitud marcada como recibida`

### Comments (user-generated)
- Any user can add comments to an expense
- Stored with `expense_id`, `user_id`, timestamp

---

## 👥 User Roles & Permissions

### 🔧 Admin
- Manage users
- Create/edit categories & accounts
- Create/edit receivers
- Set restricted history access (categories/accounts) for requesters

### ✍️ Requester
- Create new expenses
- View history of:
  - Receivers (only if `proveedor`)
  - Categories/accounts (based on admin restrictions)
- Edit `is_received` anytime (with optional file proof)
- View logs and comments

### ✅ Approver
- View and approve expenses in status `creado`
- Must select the approved quote
- Cannot approve own requests (if implemented)
- View history (with admin-controlled permissions)

### 💰 Payer
- View approved expenses
- Mark expenses as paid
  - Upload **payment confirmation**
  - Upload **payment receipt**
- View full receiver payment history

### 📊 Viewer (Accountant)
- Read-only access
- View all paid expenses
- Filter by time frame, category, receiver, account

---

## 🖼️ Views & Forms by Role

### ✅ Approver

#### ▸ **Mis Solicitudes View**
- Grouped by phase: creado, aprobado, rechazado, pagado
- Filter by requester, date range, etc.

#### ▸ **Detalles y Actualizar Form**
- Only editable if status = `creado`
  - Approve/decline
  - Select quote
- Otherwise: view-only

#### ▸ **Historial Dashboard**
- Access to receivers, categories, accounts
- Limited by admin configuration

---

### ✍️ Requester

#### ▸ **Solicitudes View**
- Filter by:
  - Status
  - **“Approved by me”**

#### ▸ **Detalles y Actualizar Form**
- Full edit access (if status = `creado`)
- `is_received` is always editable (with optional file upload)

#### ▸ **Historial Dashboard**
- Full access, no restrictions

---

### 💰 Payer

#### ▸ **Solicitudes View**
- Filter by:
  - Status
  - **“Paid by me”**

#### ▸ **Detalles y Actualizar Form**
- Upload:
  - Payment Confirmation
  - Payment Receipt

#### ▸ **Historial Dashboard**
- Full access to all histories (receivers, payments, etc.)

---

### 📊 Viewer

#### ▸ **Solicitudes Pagadas View**
- Filter by time frame, category, receiver, account

#### ▸ **Detalles View**
- Read-only view of all paid expenses

#### ▸ **Historial Dashboard**
- Full historical access

---

## 🗃️ Database Tables (Simplified)

### `expenses`
| Field          | Type       |
|----------------|------------|
| id             | UUID       |
| requester_id   | FK (users) |
| status         | ENUM       |
| is_received    | BOOLEAN    |
| created_at     | TIMESTAMP  |
| updated_at     | TIMESTAMP  |

### `quotes`
| Field        | Type       |
|--------------|------------|
| id           | UUID       |
| expense_id   | FK         |
| receiver_id  | FK         |
| amount       | DECIMAL    |
| notes        | TEXT       |
| file_path    | TEXT (Supabase) |

### `comments`
| Field        | Type       |
|--------------|------------|
| id           | UUID       |
| expense_id   | FK         |
| user_id      | FK         |
| content      | TEXT       |
| created_at   | TIMESTAMP  |

### `logs`
| Field        | Type       |
|--------------|------------|
| id           | UUID       |
| expense_id   | FK         |
| user_id      | FK (nullable) |
| action       | TEXT       |
| created_at   | TIMESTAMP  |

---

## 🔁 Workflows Summary

### Expense Creation
- User creates expense
- Logs: `Solicitud creada`, plus one per quote

### Approval
- Approver selects one quote, approves or declines
- Logs: `Solicitud aprobada` or `Solicitud rechazada`

### Reopening Declined
- Resets status
- Log: `Solicitud regresada de rechazada a creada`

### Payment
- Payer marks as paid
- Uploads:
  - Confirmation
  - Receipt
- Log: `Solicitud pagada`

### Mark as Received
- Requester toggles `is_received`
- Upload optional file
- Log: `Solicitud marcada como recibida`

---

## 📌 Future Considerations

- Notification system (email or in-app)
- API endpoint spec per role
- Full schema validation
- Audit trails for sensitive actions
- Localization (Spanish/English toggle)
- Role delegation (e.g., backups for payers)
