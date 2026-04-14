# 🚀 LeadFlow Backend

LeadFlow is a backend system for managing leads, tasks, and workflow automation.

It allows admins to define automation rules that trigger actions like assigning agents, creating tasks, sending notifications, and emails — all executed asynchronously using Celery.

---

## 🧠 Project Overview

LeadFlow is designed as a **rule-based, event-driven automation system**.

Instead of hardcoding logic, admins can define workflows like:

> “When a new lead is created → assign agent → create task → send notification”

The system listens to events, evaluates conditions, and executes actions dynamically.

---

## ✨ Features

### 🔐 Authentication

- Custom user model
- JWT authentication (SimpleJWT)
- Role-based access (`admin`, `agent`)

### 👤 Lead Management

- Create, list, update leads
- Assign leads to agents
- Role-based filtering

### 📋 Task Management

- Create and manage tasks
- Assign tasks to agents
- Track status and due dates

### ⚙️ Workflow Automation

- Admin-defined workflows with:
    - trigger types
    - conditions
    - actions

#### Supported Triggers (MVP)

- `new_lead_created`
- `lead_status_changed`

#### Supported Actions (MVP)

- assign agent
- create task
- send notification
- send email

---

## 🤖 Automation Engine

- Event-driven architecture
- Condition evaluation engine
- Ordered action execution
- WorkflowRun tracking
- Action logging

---

## ⚡ Async Processing (Celery + Redis)

Automation execution runs asynchronously using:

- **Celery** → task queue system
- **Redis** → message broker

### Flow

1. Lead event is triggered (e.g., created or status changed)
2. Django emits event
3. Celery picks up task via Redis
4. Workflow engine processes:
    - condition evaluation
    - action execution

5. Logs stored in database

---

## 🔔 Notifications

- In-app notifications
- Mark as read
- Unread count API

---

## 📊 Dashboard APIs

### Admin Dashboard

- total leads
- leads by status
- active workflows
- pending & overdue tasks
- recent workflow runs

### Agent Dashboard

- assigned leads
- pending tasks
- overdue tasks
- recent activity

---

## 🏗️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Redis
- Celery
- Docker & Docker Compose

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

## 🐳 Docker Setup

### 1. Clone repository

```
git clone <your-repo-url>
cd leadflow
```

---

### 2. Create `.env`

```
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=leadflow
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=leadflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword

REDIS_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

---

### 3. Build & run containers

```
docker compose up --build
```

---

### 4. Run migrations (if needed)

```
docker compose exec web python manage.py migrate
```

---

### 5. Create superuser

```
docker compose exec web python manage.py createsuperuser
```

---

### 6. Access app

- API → http://localhost:8000
- Admin → http://localhost:8000/admin/

---

## 🔗 Core API Endpoints

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

### Dashboard

- GET `/api/dashboard/admin/`
- GET `/api/dashboard/agent/`

---

## 🔄 How Automation Works

1. Event is triggered (lead created / status changed)
2. Celery task is queued
3. Worker processes workflows
4. Conditions evaluated
5. Actions executed in order
6. WorkflowRun + ActionLogs stored

---

## 📊 Example Workflow

**Trigger:** `lead_status_changed`
**Condition:** status = contacted

**Actions:**

1. Create task → "Send brochure"
2. Send notification to assigned agent

---

## 🚧 Future Improvements

- More triggers & actions (event-driven expansion)
- Advanced condition logic (AND/OR groups)
- Email templates
- WebSocket real-time notifications
- Role-based UI dashboards
- Celery Beat (scheduled workflows)
- Production deployment (Gunicorn + Nginx)

---

## 👨‍💻 Author

Built as a learning project to understand:

- backend architecture
- event-driven systems
- async processing
- scalable design patterns

---

## 📌 Notes

This project focuses on:

- clean architecture
- modular design
- real-world backend patterns
- scalability & extensibility

---
