

# Job Listing Backend API

This is a RESTful backend service built with **Django** and **Django REST Framework (DRF)** for the MuLearn Tech Intern role. It features a complete role-based access control system for managing job listings.

## 🚀 Features

* **Role-Based Access Control (RBAC):** Custom permissions for Admins, Companies, and Public users.
* **JWT Authentication:** Secure token-based login using `SimpleJWT`.
* **Job Management:** Comprehensive CRUD operations for job listings.
* **Advanced Filtering & Search:** Search by title/description and filter by job type, location, skills, and status.
* **API Documentation:** Fully documented OpenAPI 3.0 schema using `drf-spectacular`.
* **API Versioning:** Future-proofed with `/api/v1/` routing.
* **Soft Delete:** Data safety via `is_deleted` flags instead of hard deletion.
* **Rate Limiting:** Throttling implemented on public endpoints to prevent abuse.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** Django & Django REST Framework
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Auth:** SimpleJWT (JSON Web Tokens)
* **Filtering:** django-filter
* **Documentation:** drf-spectacular (Swagger UI)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://www.github.com/UmarAlMukhtar/mulearn-backend-intern-task.git
cd backend

```

### 2. Set up Virtual Environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

### 5. Create Admin (Superuser)

```bash
python manage.py createsuperuser

```

### 6. Run the Server

```bash
python manage.py runserver

```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔐 Authentication Flow

1. **Register:** Create an account at `/api/v1/accounts/register/` choosing role `admin` or `company`.
2. **Login:** Post credentials to `/api/v1/accounts/login/` to receive `access` and `refresh` tokens.
3. **Authorize:** Use the `access` token in the header for protected routes:
`Authorization: Bearer <your_access_token>`

---

## 👥 User Roles & Permissions

| Role | Permissions |
| --- | --- |
| **Public** | View only **Verified** jobs. Subject to rate limiting (10 req/min). |
| **Company** | Create jobs. Manage (Update/Soft Delete) **only their own** listings. |
| **Admin** | View all jobs (including drafts). **Verify/Reject** any job post. |

---

## 📖 API Documentation

Interactive API documentation is available at:

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
* **Redoc:** `http://127.0.0.1:8000/api/schema/redoc/`

---

## 📝 Assumptions & Logic

* **Soft Delete:** When a job is deleted, `is_deleted` is set to `True`. The record remains in the DB for auditing but is excluded from all API querysets.
* **Verification Logic:** Companies cannot set their own job status to `Verified`. This must be done via the `/verify/` action by an Admin.
* **Throttling:** Anonymous users are throttled to 10 requests per minute to ensure service stability.