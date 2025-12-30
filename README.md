# Email Verifier SaaS

A professional full-stack **Email Verification Platform** built with **Django**, **HTML**, and **Tailwind CSS**. Designed to help businesses and developers ensure their email lists are clean and deliverable. The application verifies email addresses for validity, deliverability, and quality while enforcing a **credit-based usage system** with daily and monthly limits.


## 🚀 Features Overview

### ✅ Email Verification Engine
The system validates emails using multiple industry-standard checks:

- **Syntax Validation** – Ensures email follows proper RFC format  
- **MX Record Check** – Verifies mail server availability  
- **Disposable Email Detection** – Checks temporary email services  
- **Role-Based Email Detection** – Detects generic accounts (admin@, info@, support@, etc.)  
- **Deliverability Check** – Predicts if an email can receive messages  

---

### 🎯 Credit-Based Usage System

- **Free Plan**
  - Monthly credit reset
  - Daily usage limit
- **Paid Plans**
  - Higher credit allocation
  - Optional daily limits
  - Monthly usage tracking
- **Automatic Credit Deduction**
- **Plan Expiry Handling**
- **Admin-controlled Plan Upgrades**

---

### 👤 User Authentication (Django Built-in)

- User registration & login
- Secure session-based authentication
- Login-required protected routes
- Automatic free plan assignment on signup

---

### 🧾 Plan & Subscription System

- Multiple plans supported (Free, Basic, Pro and Premium.)
- Admin-manageable pricing and limits
- Credits auto-reset on plan change
- Monthly and daily usage reset logic
- Expiry date handling for paid plans

---

### 📊 Usage Tracking

- Daily email usage
- Monthly usage tracking
- Email verification history stored per user
- Pagination for verification results

---

### 🎨 Frontend & UI

- **HTML templates**
- **Tailwind CSS (compiled for production)**
- Responsive and modern UI
- Clean reusable base and layout templates

---

### 📁 CSV Upload Support

- Upload email lists via CSV
- Bulk email verification
- Credit usage calculated automatically

---

## 🧩 Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Django (Python) |
| Authentication | Django Built-in Auth |
| Frontend | HTML, Tailwind CSS |
| Database | SQLite / PostgreSQL (production ready) |
| Styling | Tailwind CSS (compiled) |
| Deployment | Docker / VPS compatible |

---

## 🗂 Project Structure
backend/
├── core/
│ ├── settings.py
│ ├── urls.py
│
├── accounts/
├── verifier/
├── dashboard/
├── pages/
│
├── templates/
│ ├── base.html
│ ├── layout.html
│
├── static/
│ └── css/
│ └── dist/
│ └── styles.css
│
├── staticfiles/ # collectstatic output
├── manage.py

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

### 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

### 5️⃣ Create superuser
python manage.py createsuperuser

### 6️⃣ Collect static files
python manage.py collectstatic

### 7️⃣ Run server
python manage.py runserver

## 🔐 Admin Panel
- Manage users
- Create & edit plans
- Upgrade/downgrade user plans
- Monitor credit usage
- Control pricing & limits

## 🧠 Email Verification Logic
### Each email passes through the following pipeline:
- Normalize email
- Syntax validation
- MX record lookup
- Disposable email check
- Role account detection
- Deliverability evaluation
- Result stored in database

## 🔄 Credit Reset Logic
- **Daily reset** → resets daily usage counters
- **Monthly reset** → resets monthly usage / credits
- **Plan change** → credits automatically reassigned
- **Expiry handling** → blocks usage after plan expiry

## 🚢 Production Notes
- Tailwind CSS compiled (no live reload in production)
- DEBUG = False
- Static files served via collectstatic
- VPS-ready (Ubuntu recommended)
- Docker compatible

## 📌 Future Improvements
- Payment gateway integration (Stripe / Razorpay)
- API access for developers
- Webhook support
- Team plans
- Usage analytics dashboard

## 📄 License
- **This project is proprietary**.
- **All rights reserved**.

## Purpose
- MVP for product monetization (micro-SaaS)
- Showcase project for recruiters
- Can be sold or deployed for recurring revenue

## 👨‍💻 Author
**Aijaz Ahmed**
Python Developer | Backend Engineer
