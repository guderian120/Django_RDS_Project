
# 📘 Django + RDS + AWS Deployment Guide

This project demonstrates how to build and deploy a Django application backed by an RDS MySQL database using Docker for local development and a production-ready setup on AWS EC2 with GitHub Actions for CI/CD.


## 📑 Table of Contents

* [📦 Phase 1: Local Development with Docker Compose](#-phase-1-local-development-with-docker-compose)
* [🧪 Phase 2: RDS Integration Testing (Without Docker)](#-phase-2-rds-integration-testing-without-docker)
* [🚀 Phase 3: Deployment Documentation](#-phase-3-deployment-documentation) 
* [📡 Phase 4:  API APPLICATION DOCUMENTATION](#📡-phase-4--api-application-documentation)


### 🧪 Project  URL (Check the live project out here) 👉 👉 [project url](http://3.254.151.159)


### 🧱 API Docs
![api dasboard](/media/frontend/frontend_video.gif)


## 📦 Phase 1: Local Development with Docker Compose


* Clone the repo:

```bash
git clone https://github.com/guderian120/Django_RDS_Project
cd Django_RDS_Project
```
### 🐳 Docker Compose Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── .env
├── app/
│   ├── manage.py
│   ├── requirements.txt
│   ├── your_project/
```

### 📄 docker-compose.yml

```yaml
vversion: '3.9'

services:
  django:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django_app
    command: >
      sh -c "python manage.py makemigrations && 
      python manage.py migrate && 
      gunicorn lab5_rds.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - .:/app
    expose:
      - "8000"
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      DB_HOST: mysql_db
      DB_NAME: mydb
      DB_USER: myuser
      DB_PASSWORD: mypass
    networks:
      - backend

  mysql:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_DATABASE: mydb
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypass
      MYSQL_ROOT_PASSWORD: rootpass
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - backend
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:latest
    container_name: nginx_proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - django
    networks:
      - backend

networks:
  backend:

volumes:
  mysql_data:
```

### 📄 Dockerfile

```Dockerfile
FROM python:3.12-slim

# Environment variables (corrected format)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip tools
RUN pip install --upgrade pip setuptools wheel

# Install dependencies (using cache-efficient approach)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Runtime command (with proper signal handling)
CMD ["sh", "-c", "python manage.py migrate && exec gunicorn lab5_rds.wsgi:application --bind 0.0.0:8000"]

```

### ▶️ Running the App Locally

```bash
#make sure you are in the Django_RDS_Project direcory
docker-compose up --build
```

### ▶Demo on Docker-Compose
![Dashboard](/media/frontend/dashboard.png)

### Video on Docker-Compose
![Dashboard](/media/compose/docker_compose_video.gif)

---

## 🧪 Phase 2: RDS Integration Testing (Without Docker)

### 🧬 A. Clone the repo and Activate virtual environment 



```bash
git clone https://github.com/guderian120/Django_RDS_Project
cd Django_RDS_Project
```
* Activate virtual environment and Install requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt

#Linux users facing dependency issues with mysql-client install this dependency
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config libssl-dev
pip install -r requirements.txt #install libraries again
```
  Ensure you have already setup a publicly available Amazon RDS instance
 
### ⚙️ B. Create a `.env` File

```env
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=mydb.abcdefghijk.us-west-2.rds.amazonaws.com
DB_PORT=3306
```

Then load it in `manage.py` or via `python-dotenv`.

### 📦 C. Update `settings.py`


```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```


### 🛠️ D. Run Migrations

```bash
python manage.py migrate
```

You are now connected to your AWS RDS instance.
Note for this to be possible when setting up your 
RDS you have to make it publicly availabe: comes with security risk

---

## 🚀 Phase 3: Deployment Documentation

This section provides a complete deployment guide for the Django + MySQL project to a live AWS environment using:

* **Amazon EC2** (Ubuntu 22.04 LTS)
* **Amazon RDS MySQL** (Managed DB)
* **Gunicorn** (WSGI application server)
* **Nginx** (reverse proxy)
* **GitHub Actions** (CI/CD workflow)

### 🗺️ 1. Infrastructure Overview

| Component      | Technology             |
| -------------- | ---------------------- |
| **App Server** | EC2 (Ubuntu 22.04 LTS) |
| **Database**   | RDS MySQL (Free Tier)  |
| **Web Server** | Nginx                  |
| **WSGI App**   | Gunicorn               |
| **CI/CD**      | GitHub Actions         |

### 🛠️ 2. GITHUB ACTIONS DEMO
![GITHUB ACTION](/media/compose/github_action_log.jpg)


#### 📌 A. RDS MySQL

* Use same VPC and security group as EC2.
* Allow port 3306.

#### 📌 B. EC2 Instance

* Allow SSH (22), HTTP (80), HTTPS (443).
* SSH into instance:

```bash
ssh -i "your-key.pem" ubuntu@<EC2_IP>
```
* Clone the repo:
```bash
git clone https://github.com/guderian120/Django_RDS_Project
cd Django_RDS_Project
```
### ⚙️ 3. Django Settings

#### 🧬 A. `settings.py` Example

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```
### ⚙️ B. Create a `.env` File in the settings directory

```env
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=mydb.abcdefghijk.us-west-2.rds.amazonaws.com
DB_PORT=3306
```

#### 🔥 C. Insttall Requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt

#Linux users facing dependency issues with mysql-client install this dependency
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config libssl-dev
pip install -r requirements.txt #install libraries again
```

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Django_RDS_Project
Environment="PATH=/home/ubuntu/Django_RDS_Project/venv/bin"
ExecStart=/home/ubuntu/Django_RDS_Project/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/Django_RDS_Project/gunicorn.sock \
          your_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reexec
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 🌐 4. Nginx Configuration

```bash
sudo apt install nginx
```

Create `/etc/nginx/sites-available/Django_RDS_Project`:

```nginx
server {
    listen 80;
    server_name your-domain.com; # put your EC2 Public DNS or IP here

    location /static/ {
        root /home/ubuntu/Django_RDS_Project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Django_RDS_Project/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/Django_RDS_Project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 🤖 5. GitHub Actions CI/CD

#### 🔐 A. Add Secrets

In GitHub → Settings → Secrets:

* `EC2_IP`, `EC2_USER`, `SSH_PRIVATE_KEY`
* `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

#### ⚙️ B. Workflow

`.github/workflows/deploy.yml`

```yaml
name: Deploy Django to EC2 (No Docker)

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up SSH
      run: |
        echo "${{ secrets.SSH_PRIVATE_KEY }}" > key.pem
        chmod 600 key.pem

    - name: Deploy to EC2
      run: |
        ssh -i key.pem -o StrictHostKeyChecking=no ${{ secrets.EC2_USER }}@${{ secrets.EC2_IP }} << 'EOF'
          cd /home/ubuntu/Django_RDS_Project
          git pull origin master
          source venv/bin/activate
          pip install -r requirements.txt
          python manage.py migrate
          sudo systemctl restart gunicorn
        EOF
```

### ✅ 6. Post-Deployment Checks

```bash
sudo systemctl status gunicorn
sudo tail -f /var/log/nginx/error.log
curl http://localhost
```
You can visit the IP address of your EC2 in a browser and greet the maginificent Views
---




## 📡 Phase 4:  API APPLICATION DOCUMENTATION

This project uses **Django REST Framework** to power a RESTful API backend for managing customers, orders, and analytics. Authentication is not implemented (due to time constraints), but this can be extended in future iterations.

---
### 🧱 API Docs
![api dasboard](/media/api_docs/api_docs.png)


### 🧱 API Docs Video
![api dasboard](/media/api_docs/api_docs.gif)


### 🧱 API App Structure

```bash
rds_app/
├── admin.py               # Admin interface for models
├── apps.py
├── __init__.py
│
├── management/
│   └── commands/
│       ├── customers.py   # Populates DB with lab-provided data
│       └── seed_data.py   # Another option for seeding sample data
│
├── serializers.py         # DRF serializers for data validation
├── tests.py               # Unit tests for the app
├── urls.py                # API route mappings
└── views.py               # Main logic for handling requests
```

---

### 🔗 API Endpoints

> **Note:** All endpoints assume `localhost:8000` as the base URL during development.

---

#### 🔸 Core API Endpoints

| Endpoint                       | Method | Description                                               |
| ------------------------------ | ------ | --------------------------------------------------------- |
| `/api/customers/`              | `GET`  | Retrieve a list of all customers                          |
| `/api/analytics/`              | `GET`  | Returns analytics and advanced queries on customer orders |
| `/api/add-customer/`           | `POST` | Add a new customer with request payload                   |
| `/api/add-order/`              | `POST` | Add a new order for an existing customer                  |
| `/api/orders/<str:user_name>/` | `GET`  | Retrieve all order history for a specific customer        |

---

#### 🔹 API Documentation Endpoints

| Endpoint                  | Method | Description                                        |
| ------------------------- | ------ | -------------------------------------------------- |
| `/api/schema/`            | `GET`  | Downloads the OpenAPI schema in YAML               |
| `/api/schema/swagger-ui/` | `GET`  | Browse and test API interactively using Swagger UI |
| `/api/schema/redoc/`      | `GET`  | Browse structured API documentation using Redoc    |

> ✅ Use **Swagger UI** or **Redoc** to test requests directly from your browser interface.

---

### 🧪 Example: Adding a Customer

**POST** `/api/add-customer/`

```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "location": "Accra"
}
```

---

### 📊 Example: Viewing Customer Orders

**GET** `/api/orders/john-doe/`

Returns all orders for the user `john-doe` including price, status, and timestamp.

---

### 🔍 Example: Analytics Endpoint

**GET** `/api/analytics/`

Returns:

* Most frequent buyers
* Monthly revenue
* Revenue by location
* Product performance (e.g., unsold products)

---

> 📁 **Tip:** All seeding logic is located in `rds_app/management/commands/`. Use:

```bash
visit the endpoint localhost:8000/api/seed_data
```

to populate your database for testing and development.

---

## ✅ You're Done!

You now have a fully operational Django app:

* Locally via Docker
* Connected to AWS RDS
* Deployed on EC2 with GitHub CI/CD

Happy hacking! 🎉


