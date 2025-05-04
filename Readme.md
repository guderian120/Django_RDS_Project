
# 📘 Django + RDS + AWS Deployment Guide

This project demonstrates how to build and deploy a Django application backed by an RDS MySQL database using Docker for local development and a production-ready setup on AWS EC2 with GitHub Actions for CI/CD.

---

## 📑 Table of Contents

* [📦 Phase 1: Local Development with Docker Compose](#-phase-1-local-development-with-docker-compose)
* [🧪 Phase 2: RDS Integration Testing (Without Docker)](#-phase-2-rds-integration-testing-without-docker)
* [🚀 Phase 3: Deployment Documentation](#-phase-3-deployment-documentation)

---

## 📦 Phase 1: Local Development with Docker Compose

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
version: '3.9'
services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  web:
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_NAME=mydb
      - DB_USER=user
      - DB_PASSWORD=password
      - DB_HOST=db

volumes:
  db_data:
```

### 📄 Dockerfile

```Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

### ▶️ Running the App Locally

```bash
docker-compose up --build
```

---

## 🧪 Phase 2: RDS Integration Testing (Without Docker)

### 🧬 A. Update `settings.py`

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

### ⚙️ B. Create a `.env` File

```env
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=mydb.abcdefghijk.us-west-2.rds.amazonaws.com
DB_PORT=3306
```

Then load it in `manage.py` or via `python-dotenv`.

### 📦 C. Install MySQL Client

```bash
pip install mysqlclient
sudo apt-get install libmysqlclient-dev  # Linux
```

### 🛠️ D. Run Migrations

```bash
python manage.py migrate
```

You are now connected to your AWS RDS instance.

---

## 🚀 Phase 3: Deployment Documentation

This section provides a complete deployment guide for your Django + MySQL project to a live AWS environment using:

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

### 🛠️ 2. AWS Setup

#### 📌 A. RDS MySQL

* Use same VPC and security group as EC2.
* Allow port 3306.

#### 📌 B. EC2 Instance

* Allow SSH (22), HTTP (80), HTTPS (443).
* SSH into instance:

```bash
ssh -i "your-key.pem" ubuntu@<EC2_IP>
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

#### 🔥 B. Gunicorn Setup

```bash
pip install gunicorn
```

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/your-project
Environment="PATH=/home/ubuntu/your-project/venv/bin"
ExecStart=/home/ubuntu/your-project/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/your-project/gunicorn.sock \
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

Create `/etc/nginx/sites-available/your-project`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        root /home/ubuntu/your-project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/your-project/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/your-project /etc/nginx/sites-enabled
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

---

## ✅ You're Done!

You now have a fully operational Django app:

* Locally via Docker
* Connected to AWS RDS
* Deployed on EC2 with GitHub CI/CD

Happy hacking! 🎉


