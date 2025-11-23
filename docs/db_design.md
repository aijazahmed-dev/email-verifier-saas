## Database Design (PostgreSQL) — Models & Fields

The Email Verifier project uses **PostgreSQL** with Django ORM. Below is a concise overview of the main models and fields.

### **1. User**
- Base: Django default `User` or `CustomUser`
- Fields:
  - `id`
  - `email`
  - `password`
  - `first_name`, `last_name`
  - `is_active`, `is_staff`
  - `plan` (free/pro)
  - `credits_remaining` (int)
  - `created_at`

### **2. Profile**
- One-to-one relation with `User`
- Fields:
  - `user` (OneToOne)
  - `company`
  - `phone`
  - `created_at`

### **3. VerificationJob**
- Represents a bulk or single verification job
- Fields:
  - `id` (UUID)
  - `user` (FK)
  - `name`
  - `status` (`queued`, `in_progress`, `done`, `failed`)
  - `total_emails` (int)
  - `processed` (int)
  - `created_at`, `started_at`, `finished_at`
  - `callback_url` (optional)
  - `is_private` (bool)

### **4. VerificationRecord**
- Stores verification results for each email
- Fields:
  - `id`
  - `job` (FK)
  - `email` (text)
  - `status` (`valid`, `invalid`, `risky`, `unknown`)
  - `reason` (text) — e.g., `syntax_error`, `no_mx`, `smtp_reject`, `disposable`, `role`
  - `mx_records` (JSONB)
  - `smtp_response` (text)
  - `is_disposable` (bool)
  - `is_role` (bool)
  - `is_catch_all` (bool)
  - `processed_at`

### **5. DisposableDomain**
- Stores known temporary/disposable domains
- Fields:
  - `domain` (text, primary key)
  - `source` (text)
  - `last_checked` (datetime)

### **6. DomainReputation (Optional)**
- Tracks reputation scores for domains
- Fields:
  - `domain`
  - `last_checked`
  - `reputation_score`
  - `notes`

### **7. APIAccessKey (Paid API)**
- Manage customer API keys and rate limits
- Fields:
  - `key`
  - `user` (FK)
  - `rate_limit`
  - `created_at`

### **8. AdminLog / Audit (Optional)**
- Logs admin actions or system events
- Fields:
  - `event_type`
  - `payload`
  - `user`
  - `created_at`

---

### **Indexes**
- `VerificationRecord.email` — for fast lookup
- `VerificationJob.user` & `VerificationJob.status` — for filtering jobs
- JSONB used for storing MX records and SMTP responses efficiently
