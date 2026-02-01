# BizFlow Architecture & System Design

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        BizFlow Application                       │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────┐     ┌──────────────────────────┐
│   FRONTEND (Next.js 14)        │     │  BACKEND (Flask API)     │
│   http://localhost:3000        │     │  http://localhost:6868   │
├───────────────────────────────┤     ├──────────────────────────┤
│                               │     │                          │
│  Pages:                       │     │  Endpoints:              │
│  ✓ /login                     │────▶│  POST /auth/login        │
│  ✓ /register                  │────▶│  POST /auth/register     │
│  ✓ /dashboard (RBAC)          │     │                          │
│  ✓ /dashboard/pos             │────▶│  GET /products           │
│  ✓ /dashboard/products        │────▶│  POST /products/import   │
│  ✓ /dashboard/customers       │────▶│  GET /customers          │
│  ✓ /dashboard/orders          │────▶│  POST /customers/{id}    │
│  ✓ /dashboard/reports         │────▶│  GET /orders             │
│  ✓ /dashboard/ai              │────▶│  POST /orders            │
│                               │     │  GET /reports/revenue    │
│  Libraries:                   │     │  POST /ai/chat           │
│  • Axios (HTTP Client)        │     │                          │
│  • Tailwind CSS               │     │  Libraries:              │
│  • Lucide React (Icons)       │     │  • SQLAlchemy (ORM)      │
│  • Sonner (Toasts)            │     │  • PyJWT (Auth)          │
│  • React Hooks                │     │  • bcrypt (Hashing)      │
│                               │     │  • Flask-CORS            │
└───────────────────────────────┘     └──────────────────────────┘
         │                                      │
         │   Bearer Token in Header             │
         │   access_token: localStorage         │
         │                                      │
         └──────────────────┬──────────────────┘
                            │
                ┌───────────▼────────────┐
                │   Data Flow Layer      │
                ├───────────────────────┤
                │ • Request Interceptor │
                │ • Response Interceptor│
                │ • Error Handling      │
                │ • 401 Redirect        │
                └───────────────────────┘
```

---

## 🔐 Authentication & Authorization Flow

```
┌─────────────────────────────────────────────────────────────┐
│              AUTHENTICATION & RBAC FLOW                     │
└─────────────────────────────────────────────────────────────┘

[1] USER REGISTRATION
    ┌──────────────────┐
    │ /register page   │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ POST /auth/       │
    │ register          │
    │ {username,        │
    │  password,        │
    │  full_name,       │
    │  role}            │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Backend validates│
    │ & creates user   │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Redirect to      │
    │ /login           │
    └──────────────────┘

[2] USER LOGIN
    ┌──────────────────┐
    │ /login page      │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ POST /auth/login │
    │ {username,       │
    │  password}       │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Backend validates│
    │ generates JWT    │
    │ returns token +  │
    │ user object      │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Frontend stores: │
    │ • access_token   │
    │ • user_info      │
    │ (in localStorage)│
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ SMART REDIRECT   │
    │                  │
    │ if role==OWNER   │
    │  → /dashboard    │
    │                  │
    │ if role==EMPLOYEE│
    │  → /dashboard/pos│
    └──────────────────┘

[3] API REQUEST WITH AUTH
    ┌──────────────────┐
    │ Frontend makes   │
    │ API request      │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Request          │
    │ Interceptor:     │
    │                  │
    │ Get token from   │
    │ localStorage     │
    │                  │
    │ Add header:      │
    │ Authorization:   │
    │ Bearer <token>   │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Backend validates│
    │ JWT              │
    │                  │
    │ ✓ Valid → process│
    │ ✗ Invalid → 401  │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Response         │
    │ Interceptor:     │
    │                  │
    │ if status == 401 │
    │  • Clear token   │
    │  • Clear user    │
    │  • Redirect to   │
    │    /login        │
    │ else             │
    │  • Return data   │
    └──────────────────┘

[4] ROLE-BASED ACCESS CONTROL (RBAC)
    ┌──────────────────────────────────────┐
    │ Dashboard Layout (Protected)          │
    ├──────────────────────────────────────┤
    │                                      │
    │ Check localStorage.access_token      │
    │ ├─ NOT FOUND → Redirect to /login   │
    │ └─ FOUND → Continue                 │
    │                                      │
    │ Parse user_info.role                │
    │ ├─ OWNER:                           │
    │ │  ├─ Show all 7 nav items          │
    │ │  └─ Allow access to all routes    │
    │ │                                   │
    │ └─ EMPLOYEE:                        │
    │    ├─ Show 3 nav items (POS,        │
    │    │  Orders, AI)                   │
    │    └─ Block access to Dashboard,    │
    │       Products, Customers, Reports  │
    │       (Auto-redirect to /pos)       │
    └──────────────────────────────────────┘
```

---

## 📊 Data Model

```
┌─────────────────────────────────────────────────────────┐
│                   DATABASE SCHEMA                       │
│              (MySQL - Docker Container)                │
└─────────────────────────────────────────────────────────┘

┌──────────────────────┐
│      Users           │
├──────────────────────┤
│ id (PK)              │
│ username (UNIQUE)    │
│ password_hash        │
│ full_name            │
│ role (OWNER/EMP)     │
│ created_at           │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│      Orders          │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ customer_id (FK)     │
│ total_amount         │
│ payment_method       │
│ status               │
│ created_at           │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│    OrderItems        │
├──────────────────────┤
│ id (PK)              │
│ order_id (FK)        │
│ product_id (FK)      │
│ quantity             │
│ unit_price           │
└──────────────────────┘
         │
         └──────────────┐
                        │ N:1
                        ▼
    ┌──────────────────────────┐
    │      Products            │
    ├──────────────────────────┤
    │ id (PK)                  │
    │ name                     │
    │ category                 │
    │ selling_price            │
    │ cost_price               │
    │ stock                    │
    │ unit                     │
    │ created_at               │
    └──────────────────────────┘

┌──────────────────────┐
│    Customers         │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ phone                │
│ address              │
│ debt_amount          │
│ created_at           │
└──────────────────────┘
         │
         └─ Referenced by Orders
```

---

## 🔄 Component Communication

```
┌─────────────────────────────────────────────────────┐
│         FRONTEND COMPONENT HIERARCHY                │
└─────────────────────────────────────────────────────┘

App (layout.tsx)
├─ <Toaster /> (Global notifications)
└─ Routes
   ├─ /login (LoginPage)
   │  └─ api.post('/auth/login')
   │
   ├─ /register (RegisterPage)
   │  └─ api.post('/auth/register')
   │
   └─ /dashboard/* (Protected Layout)
      ├─ Sidebar
      │  ├─ Logo & Brand
      │  ├─ Navigation (Filtered by role)
      │  ├─ Role Display
      │  └─ Logout Button
      │
      ├─ Header
      │  ├─ User Greeting
      │  └─ Date Display
      │
      └─ Pages
         ├─ /dashboard
         │  ├─ api.get('/reports/revenue')
         │  └─ 4 Stat Cards
         │
         ├─ /dashboard/pos
         │  ├─ api.get('/products')
         │  ├─ api.get('/customers')
         │  ├─ api.post('/orders')
         │  └─ Cart Logic (useState)
         │
         ├─ /dashboard/products
         │  ├─ api.get('/products')
         │  ├─ api.post('/products/import')
         │  └─ Import Modal
         │
         ├─ /dashboard/customers
         │  ├─ api.get('/customers')
         │  ├─ api.post('/customers/{id}/payment')
         │  └─ Payment Modal
         │
         ├─ /dashboard/orders
         │  └─ api.get('/orders')
         │
         ├─ /dashboard/reports
         │  └─ api.get('/reports/revenue')
         │
         └─ /dashboard/ai
            └─ api.post('/ai/chat')
```

---

## 🌐 Network Communication

```
┌──────────────────────────────────────────────────────┐
│         HTTP REQUEST/RESPONSE CYCLE                  │
└──────────────────────────────────────────────────────┘

[CLIENT SIDE - Browser]
         │
         │ 1. User Action
         │    (Click, Submit Form)
         │
         ▼
    ┌──────────────────┐
    │ React Component  │
    │ State Update     │
    │ api.get/post/put │
    └────────┬─────────┘
             │
             │ 2. Request Interceptor
             │    • Get token from localStorage
             │    • Add Authorization header
             │    • Add Content-Type: application/json
             │
             ▼
    ┌──────────────────────────────────────┐
    │ HTTP Request                         │
    │ GET/POST http://localhost:6868/api/*│
    │ Headers:                             │
    │  Authorization: Bearer <token>       │
    │  Content-Type: application/json      │
    └────────┬─────────────────────────────┘
             │
             │ Network
             │
[SERVER SIDE - Flask]
             │
             ▼
    ┌──────────────────┐
    │ Flask Route      │
    │ @app.route(...)  │
    │ @jwt_required    │
    └────────┬─────────┘
             │
             │ 3. Validate JWT
             │    ├─ Check signature
             │    ├─ Check expiry
             │    └─ Extract user info
             │
             ▼
    ┌──────────────────┐
    │ Route Handler    │
    │ (Controller)     │
    └────────┬─────────┘
             │
             │ 4. Query Database
             │    (SQLAlchemy)
             │
             ▼
    ┌──────────────────┐
    │ Business Logic   │
    │ Processing       │
    └────────┬─────────┘
             │
             │ 5. Build Response
             │    JSON
             │
             ▼
    ┌──────────────────┐
    │ HTTP Response    │
    │ Status: 200/201/ │
    │ 400/401/500      │
    │ Body: JSON       │
    └────────┬─────────┘
             │
             │ Network
             │
[CLIENT SIDE - Browser]
             │
             ▼
    ┌──────────────────┐
    │ Response         │
    │ Interceptor      │
    │                  │
    │ if status == 401 │
    │  • Clear storage │
    │  • Redirect      │
    │ else             │
    │  • Return data   │
    └────────┬─────────┘
             │
             │ 6. Update Component State
             │    (setState)
             │
             ▼
    ┌──────────────────┐
    │ Component        │
    │ Re-render        │
    │ (with new data)  │
    └────────┬─────────┘
             │
             │ 7. Show Toast
             │    (Sonner)
             │
             ▼
    ┌──────────────────┐
    │ UI Update        │
    │ Complete         │
    └──────────────────┘
```

---

## 🔄 Data Flow Example: POS Checkout

```
┌────────────────────────────────────────────────────┐
│      POS SYSTEM - COMPLETE TRANSACTION FLOW        │
└────────────────────────────────────────────────────┘

Step 1: Initial Load
    /dashboard/pos
         │
         ▼
    useEffect → api.get('/products')
         │
         ▼
    [{ id: 1, name: "Cà phê", price: 25000, stock: 100 }]
         │
         ▼
    State: products = [...]
    Render: Product Grid

Step 2: Add to Cart
    User clicks "Cà phê"
         │
         ▼
    onClick → addToCart(product)
         │
         ▼
    cart.push({ id: 1, name: "Cà phê", price: 25000, qty: 1 })
         │
         ▼
    Re-render: Cart shows item

Step 3: Select Customer
    User selects from dropdown
         │
         ▼
    onChange → setSelectedCustomerId(1)
         │
         ▼
    State: selectedCustomerId = 1

Step 4: Choose Payment Method
    User toggles "Ghi nợ"
         │
         ▼
    onClick → setPaymentMethod('DEBT')
         │
         ▼
    State: paymentMethod = 'DEBT'

Step 5: Checkout
    User clicks "Thanh toán"
         │
         ▼
    onClick → handleCheckout()
         │
         │ Build payload:
         │ {
         │   customer_id: 1,
         │   payment_method: 'DEBT',
         │   items: [
         │     { product_id: 1, quantity: 1 }
         │   ]
         │ }
         │
         ▼
    api.post('/orders', payload)
         │
         │ Request Interceptor adds:
         │ Authorization: Bearer <token>
         │
         ▼
    Backend POST /orders
         │
         ├─ Validate JWT ✓
         ├─ Check customer exists ✓
         ├─ Check products exist ✓
         ├─ Create Order record
         ├─ Create OrderItems
         ├─ Update Customers.debt_amount
         └─ Return { id: 123, status: 'success' }
         │
         ▼
    Frontend receives response
         │
         │ 200 OK
         │
         ▼
    handleCheckout catches success:
         ├─ toast.success("Thanh toán thành công")
         ├─ setCart([]) // Clear cart
         └─ setSelectedCustomerId(null)
         │
         ▼
    Re-render: Empty cart, fresh page
```

---

## 🛡️ Security Layers

```
┌─────────────────────────────────────────────────┐
│            SECURITY ARCHITECTURE                │
└─────────────────────────────────────────────────┘

Layer 1: Frontend Validation
    ├─ Form validation (username, password)
    ├─ Required field checks
    ├─ Input sanitization
    └─ Max length limits

Layer 2: HTTP Transport
    ├─ Axios client enforcement
    ├─ HTTPS ready (for production)
    └─ CORS policy (Flask-CORS)

Layer 3: Authentication
    ├─ Password → bcrypt hashing
    ├─ JWT token generation
    ├─ Bearer token in header
    └─ Token expiry validation

Layer 4: Authorization
    ├─ JWT signature verification
    ├─ Route-level @jwt_required
    ├─ Role-based access (OWNER/EMPLOYEE)
    └─ Frontend RBAC guards

Layer 5: Frontend Guards
    ├─ Protected layout checks token
    ├─ Route protection redirects
    ├─ 401 interceptor clears auth
    └─ Sidebar hides unauthorized links

Layer 6: Database
    ├─ Parameterized queries (SQLAlchemy)
    ├─ Foreign key constraints
    ├─ Data validation in models
    └─ Audit timestamps (created_at)
```

---

## 📈 Scalability Roadmap

```
Current State:        Improvement:          Future State:
┌──────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Single User  │────▶│ Add Caching  │────▶│ Distributed     │
│ Local MySQL  │     │ (Redis)      │     │ Architecture    │
│ Dev Server   │     │              │     │                 │
└──────────────┘     └──────────────┘     ├─ Load Balancer  │
                                           ├─ Multiple Flask │
                                           │  Instances      │
                                           ├─ RDS MySQL      │
                                           ├─ S3 for files   │
                                           ├─ CloudFront CDN │
                                           └─ Monitoring     │
```

---

## 🎯 Component State Management

```
┌────────────────────────────────────────────────┐
│       STATE MANAGEMENT BY PAGE                 │
└────────────────────────────────────────────────┘

/login
├─ formData: { username, password }
├─ loading: boolean
└─ error: string

/register
├─ formData: { username, password, full_name, role }
├─ loading: boolean
└─ success message (toast)

/dashboard
├─ stats: { revenue, orders, customers, avg }
└─ isLoading: boolean

/dashboard/pos
├─ products: Product[]
├─ customers: Customer[]
├─ cart: CartItem[]
├─ selectedCustomerId: number | null
├─ paymentMethod: 'CASH' | 'DEBT'
└─ isSubmitting: boolean

/dashboard/products
├─ products: Product[]
├─ isLoading: boolean
├─ role: 'OWNER' | 'EMPLOYEE'
├─ importModalOpen: boolean
├─ selectedProductId: number | null
├─ importQuantity: string
├─ importCost: string
└─ isSubmitting: boolean

/dashboard/customers
├─ customers: Customer[]
├─ isLoading: boolean
├─ role: 'OWNER' | 'EMPLOYEE'
├─ isModalOpen: boolean
├─ selectedCustomer: Customer | null
├─ paymentAmount: string
└─ isSubmitting: boolean
```

---

This architectural overview provides a complete picture of how BizFlow is structured,
how data flows through the system, and how security is maintained across all layers.
