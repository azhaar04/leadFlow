# 🚀 LeadFlow Backend

LeadFlow is a backend system for managing leads, tasks, and workflow automation.
It allows admins to define automation rules that trigger actions like assigning agents, creating tasks, and sending notifications.

This project is built using Django, Django REST Framework, and PostgreSQL.

---

## 🧠 Project Overview

LeadFlow is designed as a **rule-based automation system**.

Instead of hardcoding logic, admins can define workflows like:

> “When a new lead is created → assign agent → create task → send notification”

The system evaluates conditions and executes actions dynamically.

---

## ✨ Features

### 🔐 Authentication

- Custom user model
- JWT authentication
- Role-based access (admin, agent)

### 👤 Lead Management

- Create, list, update leads
- Assign leads to agents
- Filter leads by role

### 📋 Task Management

- Create and manage tasks
- Assign tasks to agents
- Track task status and due dates

### ⚙️ Workflow Automation

- Define workflows with:
    - Trigger types
    - Conditions
    - Actions

- Supported triggers:
    - `new_lead_created`
    - `lead_status_changed`

- Supported actions:
    - assign agent
    - create task
    - send notification
    - send email

### 🤖 Automation Engine

- Event-driven system
- Condition evaluation
- Action execution in order
- Workflow run tracking
- Action logging

### 🔔 Notifications

- In-app notifications
- Mark as read
- Unread count API

---

## 🏗️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Redis (for Celery - optional)
- Celery (for background tasks - optional)

---

## 📁 Project Structure

```
config/
apps/
    accounts/
    leads/
    tasks/
    workflows/
    automation/
    notifications/
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd leadflow
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Create .env file

```
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=leadflow
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
```

### 5. Apply migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser

```
python manage.py createsuperuser
```

### 7. Run server

```
python manage.py runserver
```

---

## 🔗 API Endpoints (Core)

### Auth

- POST `/api/auth/login/`
- POST `/api/auth/signup/`
- POST `/api/auth/refresh/`
- GET `/api/auth/me/`

### Leads

- GET `/api/leads/`
- POST `/api/leads/`
- POST `/api/leads/{id}/change-status/`

### Workflows

- POST `/api/workflows/`
- GET `/api/workflows/`
- POST `/api/workflows/{id}/conditions/`
- POST `/api/workflows/{id}/actions/`
- POST `/api/workflows/{id}/activate/`

### Notifications

- GET `/api/notifications/`
- POST `/api/notifications/{id}/read/`
- GET `/api/notifications/unread-count/`

---

## 🔄 How Automation Works

1. Event is triggered (e.g., lead created)
2. System finds active workflows
3. Conditions are evaluated
4. If matched → actions are executed in order
5. WorkflowRun and ActionLogs are saved

---

## 📊 Example Workflow

**Trigger:** `lead_status_changed`
**Condition:** status = contacted

**Actions:**

1. Create task → “Send brochure”
2. Send notification to assigned agent

---

## 🚧 Future Improvements

- Celery for async execution
- Advanced condition logic (AND/OR)
- Email templates
- Dashboard analytics
- Role-based dashboards
- WebSocket notifications

---

## 👨‍💻 Author

Built as a learning project to understand backend system design, automation engines, and scalable architecture.

---

## 📌 Notes

This project is designed with a focus on:

- clean architecture
- scalability
- real-world backend patterns

---
