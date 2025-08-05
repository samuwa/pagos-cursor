# 🏦 Pagos - Expense Management System

A modern expense management application built with React, TypeScript, and Supabase.

## 🚀 Features

- **Email OTP Authentication** - Secure login without passwords
- **Role-Based Access Control** - Admin, Requester, Approver, Payer, Viewer roles
- **Expense Management** - Create, track, and approve expenses
- **Real-time Updates** - Live notifications and status changes
- **File Upload** - Attach quotes and receipts
- **Responsive Design** - Works on desktop and mobile

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS + Headless UI
- **Backend**: Supabase (Database + Auth + Storage)
- **Deployment**: Heroku
- **Version Control**: GitHub

## 📋 Prerequisites

- Node.js 18+ 
- npm or yarn
- Supabase account
- Heroku account

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/samuwa/pagos-cursor.git
cd pagos-cursor
```

### 2. Install dependencies
```bash
npm install
```

### 3. Set up environment variables
Create a `.env.local` file in the root directory:
```env
VITE_SUPABASE_URL=https://xidfcnlzvcydevjtqfkz.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. Start development server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 🗄️ Database Setup

The database schema is located in `db_setup/`:

- `database_schema.md` - Complete schema documentation
- `database_schema.sql` - SQL to create all tables and relationships

To set up the database:
1. Go to your Supabase Dashboard
2. Navigate to SQL Editor
3. Copy and paste the contents of `database_schema.sql`
4. Execute the SQL

## 🔐 Authentication

The app uses Supabase Auth with Email OTP:

1. **Login Flow**: User enters email → Receives OTP → Enters code → Logged in
2. **Protected Routes**: All dashboard pages require authentication
3. **Role-Based Access**: Different features based on user roles

## 📁 Project Structure

```
src/
├── components/          # React components
│   └── Login.tsx       # Authentication component
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication state management
├── lib/                # Utility libraries
│   └── supabase.ts     # Supabase client configuration
└── App.tsx            # Main application component
```

## 🚀 Deployment

### Heroku Deployment
The app is configured for Heroku deployment:

1. **Environment Variables**: Already set in Heroku
2. **Build Command**: `npm run build`
3. **Start Command**: `npm start`

### Manual Deployment
```bash
# Build the app
npm run build

# Deploy to Heroku
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Features

1. **Components**: Add to `src/components/`
2. **Pages**: Add to `src/pages/` (create if needed)
3. **Types**: Add to `src/lib/supabase.ts`
4. **Contexts**: Add to `src/contexts/`

## 📊 Database Schema

The application uses the following main tables:

- **users** - User accounts and profiles
- **user_roles** - Role assignments
- **expenses** - Expense records
- **categories** - Expense categories
- **accounts** - Financial accounts
- **receivers** - Suppliers/vendors
- **quotes** - Quote documents
- **comments** - User comments
- **logs** - System audit logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using React, TypeScript, and Supabase**
