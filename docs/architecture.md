## Django Architecture & Components

This section describes the high-level architecture and components of the Email Verifier project.

### **Recommended Stack**
- **Django (>=4.x) + Django Rest Framework (DRF)** — core web framework and API handling  
- **PostgreSQL** — primary relational database  
- **Redis** — used as broker/cache for background tasks  
- **Celery** — background job processing (or Django-Q / RQ if preferred)  
- **Gunicorn + Nginx** — production server setup (or Uvicorn if using ASGI)  
- **Docker + docker-compose** — containerization for development and deployment  
- **Optional:** Celery Flower for monitoring background tasks  
- **Storage:** Local file system for CSV uploads (use S3 or object store for production)  
- **Optional:** Rate limiting with DRF throttling + Redis  
- **Logging:** Sentry or simple file logging  
- **Tests:** pytest + pytest-django or Django Test framework  

---

### **Key Components**
- **`verifier.engine`** — Core verification functions; pure Python module, fully unit-testable  
- **`jobs.tasks`** — Celery tasks to process CSV rows in batches  
- **`api.views`** — DRF endpoints for:  
  - Job creation  
  - Job status  
  - Single email check  
  - User profile  
- **`ui.views`** — Django templates for dashboard, CSV upload pages (if not building SPA)  
- **`utils.parsers`** — CSV parser that streams rows for memory efficiency  
- **`rate_limiter`** — Decorator/middleware to prevent abuse of endpoints  

---

### **Security Considerations**
- Throttle API endpoints to prevent abuse  
- Sanitize CSV uploads and enforce file size limits  
- Use timeouts and exponential backoff for SMTP checks  
- Respect MX providers; avoid spamming  
- Use HTTPS in production for secure communication  
