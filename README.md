# 🚀 LeadFlow Backend

LeadFlow is a backend system for managing leads, tasks, and workflow automation.

It enables admins to define automation rules that trigger actions like assigning agents, creating tasks, and sending notifications — all executed asynchronously using Celery.

---

## 🧠 Project Overview

LeadFlow is designed as a **rule-based, event-driven automation system**.

Instead of hardcoding logic, admins can define workflows like:

> “When a new lead is created → assign agent → create task → send notification”

The system listens to events, evaluates conditions, and executes actions dynamically in the background.

---

## ✨ Features

### 🔐 Authentication

* Custom user model
* JWT authentication
* Role-based access (admin, agent)

---

### 👤 Lead Management

* Create, list, update leads
* Assign leads to agents
* Role-based filtering

---

### 📋 Task Management

* Create and manage tasks
* Assign tasks to agents
* Track status and due dates
* Overdue detection

---

### ⚙️ Workflow Automation

* Define workflows with:

  * Trigger types
  * Conditions
  * Actions

#### Supported triggers

* `new_lead_created`
* `lead_status_changed`

#### Supported actions

* assign agent
* create task
* send notification
* send email

---

### 🤖 Automation Engine (Async)

* Event-driven system
* Condition evaluation
* Ordered action execution
* Workflow run tracking
* Action logging
* Executed asynchronously using Celery

---

### 🔔 Notifications

* In-app notifications
* Mark as read
* Unread count API

---

### 📊 Dashboard APIs

#### Admin Dashboard

* Total leads
* Leads by status
* Total active workflows
* Pending tasks
* Overdue tasks
* Recent workflow runs

#### Agent Dashboard

* Assigned leads count
* Pending tasks
* Overdue tasks
* Recent lead updates

---

### 📊 Monitoring & Logs

* Workflow run tracking
* Action logs for each execution
* Debug-friendly logging for async jobs

---

## 🏗️ Tech Stack

* Python 3.x
* Django
* Django REST Framework
* PostgreSQL
* JWT (SimpleJWT)
* Redis (message broker)
* Celery (background task processing)

---

## ⚙️ Setup Instructions

### 1. Clone repository

```bash
git clone <your-repo-url>
cd leadflow
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` file

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=leadflow
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

---

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create superuser

```bash
python manage.py createsuperuser
```

---

### 7. Run Django server

```bash
python manage.py runserver
```

---

### 8. Run Redis server

```bash
docker run -d -p 6379:6379 redis
```

---

### 9. Run Celery worker

```bash
celery -A config worker -P solo -l info
```

---

## 🔗 API Endpoints (Core)

### Auth

* POST `/api/auth/login/`
* POST `/api/auth/signup/`
* POST `/api/auth/refresh/`
* GET `/api/auth/me/`

---

### Leads

* GET `/api/leads/`
* POST `/api/leads/`
* POST `/api/leads/{id}/change-status/`

---

### Workflows

* POST `/api/workflows/`
* GET `/api/workflows/`
* POST `/api/workflows/{id}/conditions/`
* POST `/api/workflows/{id}/actions/`
* POST `/api/workflows/{id}/activate/`

---

### Notifications

* GET `/api/notifications/`
* POST `/api/notifications/{id}/read/`
* GET `/api/notifications/unread-count/`

---

### Dashboard

* GET `/api/dashboard/admin/`
* GET `/api/dashboard/agent/`

---

## 🔄 How Automation Works (Async Flow)

1. Event is triggered (e.g., lead created or status changed)
2. Django saves data
3. Task is queued to Redis
4. Celery worker picks up the task
5. Matching workflows are fetched
6. Conditions are evaluated
7. Actions are executed in order
8. WorkflowRun and ActionLogs are stored

---

## 🧠 Architecture Overview

```
Django API → Redis (Broker) → Celery Worker → Automation Engine
```

---

## 📊 Example Workflow

**Trigger:** `lead_status_changed`
**Condition:** status = contacted

**Actions:**

1. Create task → “Send brochure”
2. Send notification to assigned agent

---

## 🚧 Future Improvements

* Add more supported triggers (e.g., task completed, inactivity, time-based events)
* Add more actions (e.g., webhook calls, SMS, integrations)
* Advanced condition logic (AND/OR support)
* Email templates
* Dashboard analytics (charts & insights)
* WebSocket real-time notifications
* Scheduled workflows (delayed execution)

---

## 👨‍💻 Author

Built as a learning project to understand:

* backend system design
* event-driven architecture
* automation engines
* asynchronous processing with Celery

---

## 📌 Notes

This project focuses on:

* clean architecture
* scalability
* real-world backend patterns
* async job processing

Frontend integration will be added soon to fully visualize workflows and dashboards.

---
