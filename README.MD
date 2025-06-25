# 🧪 Pollab — Backend

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Build Status](https://img.shields.io/badge/deploy-render-gray.svg?style=flat-square)](https://dashboard.render.com/)
[![Last Commit](https://img.shields.io/github/last-commit/igormahall/pollab-backend?style=flat-square)](https://github.com/igormahall/pollab-backend/commits/main)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=flat-square)](https://www.python.org/)
[![Status: Production](https://img.shields.io/badge/status-production-brightgreen?style=flat-square)](#)

**About Pollab**

**Pollab** (short for *Poll Laboratory*) is a modern, open-source polling platform designed to 
simplify how users collect opinions and make decisions. Built with **Django REST Framework** 
and **PostgreSQL**, it powers both web and mobile clients with a robust API.

Main features include:
- 🧠 Clean and responsive UI 
- ⚙️ Reactive forms with validation
- 🕒 Real-time vote tracking and countdown support
- 📢 Toast notifications for a smooth UX

Whether you're testing ideas, collecting feedback, or running interactive demos — Pollab lets 
you create, vote, and visualize results in seconds.
> **Join. Experiment. Transform.**

[//]: # (## Interface)

[//]: # ()
[//]: # (<p align="center">)

[//]: # (  <img src="readme_assets/mobile_create.png" alt="Splashscreen" width="30%"/>)

[//]: # (  <img src="readme_assets/mobile_polllist.png" alt="Enquetes Abertas" width="30%"/>)

[//]: # (  <img src="readme_assets/mobile_polldetails.png" alt="Detalhe da Enquete" width="30%"/>)

[//]: # (</p>)

---

## ✨ Overview

| Item               | Details                                                                                    |
|--------------------|--------------------------------------------------------------------------------------------|
| **Stack**          | Python · Django · DRF · PostgreSQL                                                         |
| **Identification** | Participants are identified by a custom `id_participante` field in each vote submission.   |
| **Goal**           | Full CRUD for polls, duplicate vote prevention, and real-time result tracking.             |
| **Docs**           | Auto-generated API documentation via `drf-spectacular` (Swagger/ReDoc).                    |


---

## ⚙️ Setup

### 0. Prerequisites

Make sure you have the following installed:

- [Python ≥ 3.9](https://www.python.org/downloads/) (added to `PATH`)
- [PostgreSQL](https://www.postgresql.org/download/) (default user: `postgres`, password: `postgres`)
- [Git](https://git-scm.com/)
- [PyCharm Community](https://www.jetbrains.com/pycharm/download)

### 1. Clone the repository
```bash
git clone https://github.com/igormahall/pollab-backend.git
cd pollab-backend
```
 

### 2. Create and activate the virtual environment
```bash
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS / Linux
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create a `.env` file
- In the project root, create a `.env` file with:
```env
DJANGO_SECRET_KEY=your-secret-key-here
```
- Generate a secure key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Create the PostgreSQL database
```bash
psql -U postgres
```
- When prompted, enter the password: `postgres`
- Inside the PostgreSQL shell:
```sql
CREATE DATABASE enquete;
\q
```

### 6. Apply migrations
```bash
python manage.py migrate
```

### 7. Create a superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to define username, email, and password.

### 8. Start the development server
```bash
python manage.py runserver
```
- Admin panel: **http://127.0.0.1:8000/**
- Interative API docs: **http://127.0.0.1:8000/api/swagger/**


>⚠️ Never commit your real `.env` file!
>
> Make sure `.env` is listed in `.gitignore`.

---

## 🗄️ Data Model

The backend logic is structured around three main models:

### 1. Pool (`Enquete`)

| Field          | Type                | Description                                  |
|----------------|---------------------|----------------------------------------------|
| `id`           | `BigAutoField` (PK) | Primary Key                                  |
| `titulo`       | `CharField`         | The question shown to users                  |
| `data_criacao` | `DateTimeField`     | Poll creation timestamp                      |
| `status`       | `CharField`         | Either `Aberta` (Open) or `Fechada` (Closed) |



### 2. Choice (`Opcao`)

| Field         | Type                       | Description                   |
|---------------|----------------------------|-------------------------------|
| `id`          | `BigAutoField` (PK)        | Primary Key                   |
| `enquete`     | `ForeignKey('Enquete')`    | Linked poll                   |
| `texto_opcao` | `CharField`                | Text displayed as vote option |
| `votos`       | `IntegerField`             | Vote counter                  |

---

### 3. Vote (`Voto`)

| Field             | Type                    | Description                      |
|-------------------|-------------------------|----------------------------------|
| `id`              | `BigAutoField` (PK)     | Primary key                      |
| `id_participante` | `CharField`             | Unique identifier for each voter |
| `enquete`         | `ForeignKey('Enquete')` | Related poll                     |
| `opcao_escolhida` | `ForeignKey('Opcao')`   | Chosen option                    |
| `data_voto`       | `DateTimeField`         | Vote timestamp                   |

**Unique vote restriction**

```python
class Meta:
    unique_together = ("enquete", "id_participante")
```
Enforces **1 vote per participant** per pool.

---

### 🔗 Relationships & Flow

```
Poll ──< Choice ──< Vote
         ^              |
         |--------------|
```

1. A pool (`Enquete`) has many choices (`Opcao`).  
2. Voting creates a `Voto` object linked to the selected choice.  
3. If a participant has already voted, it returns 409 Conflict.  
4. After voting, the selected choice's counter is atomically incremented.

---

## 🔌 REST Endpoints

| Method + Route                   | Action | Description                                             |
|----------------------------------|--------|---------------------------------------------------------|
| `GET /api/enquetes/`             | List   | Returns all polls (open and closed)                     |
| `GET /api/enquetes/{id}/`        | Detail | Returns poll details, including choices                 |
| `POST /api/enquetes/`            | Create | Creates a new poll and nested choices                   |
| `POST /api/enquetes/{id}/votar/` | Vote   | Registers a vote for a specific choice and participant  |

> All responses use `application/json` format with camelCase payloads.

Example — **POST /api/enquetes/1/votar/**
```json
{
  "id_opcao": 2,
  "id_participante": "carlinhos_teste_123"
}
```

Possible responses:

| Status Code         | Meaning                                    |
|---------------------|--------------------------------------------|
| **200** OK          | Vote successfully recorded                 |
| **400** Bad Request | Invalid choice for the given poll          |
| **409** Conflict    | Participant has already voted in this poll |

---

## 🚀 Deployment

This project is production-ready for platforms like Render, Railway, or Heroku. 
All critical settings (`DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`) are 
environment-based to ensure security and scalability.

---

## 🤝 Contributing

We welcome contributions! If you'd like to suggest improvements, report a bug, 
or propose new features, feel free to open an issue or submit a pull request.

---

## 📜 License

Distributed under the **MIT License**.
