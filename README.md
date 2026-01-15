# Job/Internship Listing Backend API

This is a RESTful backend service built with **Django** and **Django REST Framework (DRF)** for the MuLearn Tech Intern role. It features a complete role-based access control system for managing job listings.

## 🚀 Features

* **Role-Based Access Control (RBAC):** Separate permissions for Admins, Companies, and Public users.
* **JWT Authentication:** Secure login using `djangorestframework-simplejwt`.
* **Job Management:** Companies can create/edit listings; Admins verify them.
* **Advanced Filtering:** Filter by job type, location, skills, and status.
* **API Documentation:** Interactive Swagger UI documentation.
* **API Versioning:** Clean `/api/v1/` structure.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** Django & Django REST Framework
* **Database:** PostgreSQL (or SQLite)
* **Auth:** SimpleJWT (JSON Web Tokens)
* **Documentation:** drf-spectacular (OpenAPI 3.0)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://www.github.com/UmarAlMukhtar/mulearn-intern-backend.git
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

1. **Register:** Create a user account at `/api/v1/accounts/register/` and select a role (`admin` or `company`).
2. **Login:** Submit credentials to `/api/v1/accounts/login/` to receive an `access` and `refresh` token.
3. **Authorize:** Use the `access` token in the header for protected routes:
`Authorization: Bearer <your_access_token>`

---

## 👥 User Roles & Permissions

| Role | Permissions |
| --- | --- |
| **Public** | Can view only **Verified** job listings. |
| **Company** | Can create jobs and manage (edit/delete) **only their own** listings. |
| **Admin** | Can view all listings and **Verify/Reject** any job post. |

---

## 📖 API Documentation

Interactive API documentation is available at:

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`

---

## 📝 Assumptions

* A user must specify their role during registration.
* Newly created jobs are set to `draft` status by default.
* Skills must be created via the Django Admin or by an Admin user before being assigned to jobs.