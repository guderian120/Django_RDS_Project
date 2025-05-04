
## 🐳 Quick Start with Docker Compose

1. [📦 Prerequisites](#-prerequisites)

   * [Install Docker](#install-docker)
   * [Install Docker Compose](#install-docker-compose)
2. [🚀 Running the Application](#-running-the-application)

   * [Clone the Repository](#clone-the-repository)
   * [Navigate to Project Directory](#navigate-to-project-directory)
   * [Build and Start Containers](#build-and-start-containers)
   * [Access the Application](#access-the-application)
   * [Container Status](#container-status)
3. [🖼️ Docker Build Screenshot](#️docker-build-screenshot)

---

## 🎨 Frontend Documentation

4. [📁 Frontend App Overview](#-frontend-app-overview)

   * [Creating the Frontend App](#creating-the-frontend-app)
   * [Directory Structure](#directory-structure)
5. [🗂️ Static Files and Templates](#️static-files-and-templates)

   * [JavaScript and Styles](#javascript-and-styles)
   * [HTML Templates](#html-templates)
6. [📊 Dashboard Features](#-dashboard-features)

   * [Add New Customer](#add-new-customer)
   * [Add New Order](#add-new-order)
   * [Customer Orders Section](#customer-orders-section)
   * [Real-Time Charts and Graphs](#real-time-charts-and-graphs)
   * [Summary Cards](#summary-cards)
   * [Dashboard Navigation](#dashboard-navigation)
   * [Dashboard Screenshot](#dashboard-screenshot)
7. [📄 View Orders Page](#-view-orders-page)

   * [Filter and Sort Orders](#filter-and-sort-orders)
   * [Top Customers](#top-customers)
   * [Monthly Sales Report](#monthly-sales-report)
   * [Unsold Products](#unsold-products)
   * [Average Order by Location](#average-order-by-location)
   * [Frequent Buyers](#frequent-buyers)
   * [Orders Page Screenshot](#orders-page-screenshot)




# 🚀 Django RDS Project

Welcome to the **Django RDS Project** – a minimal but functional full-stack application with real-time dashboard features, a connected MySQL RDS backend, and Dockerized deployment. This README helps you get started immediately and provides in-depth frontend documentation.

---

## 🐳 Quick Start with Docker Compose

### 📦 Prerequisites

Before running the application, make sure the following tools are installed:

#### ✅ Docker

* Follow the [Docker installation guide](https://docs.docker.com/get-docker/) for your OS.
* After installation, verify Docker is working:

  ```bash
  docker --version
  ```

#### ✅ Docker Compose

* Install Docker Compose (usually comes with Docker Desktop).
* Confirm with:

  ```bash
  docker-compose --version
  ```

---

### 🚀 Running the Application

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Django_RDS_Project.git
```

#### 2. Navigate to Project Directory

```bash
cd Django_RDS_Project
```

Ensure you're in the same directory as `docker-compose.yml`.

#### 3. Build and Start Containers

```bash
docker-compose up --build
```

> 🕓 **Note:** The images are large, so allow some time for everything to build and initialize.

#### 4. Access the Application

Once all services are up, visit:

```
http://127.0.0.1
```

#### 5. Check Docker Containers

You can confirm the containers are running using:

```bash
docker ps
```

---

### 🖼️ Docker Build Screenshot

![docker-compose-up](path/to/docker-compose-screenshot.png)

---

## 🎨 Frontend Documentation

### 📁 Frontend App Overview

We created a minimal frontend using Django templates and static files:

```bash
python manage.py startapp frontend
```

#### 📂 Directory Structure

```
frontend/
├── static/
│   ├── js/
│   └── styles/
├── templates/
│   └── frontend/
│       ├── dashboard.html
│       └── order_data.html
├── urls.py
└── views.py
```

This app mainly serves static assets and dashboard templates.

---

### 🗂️ Static Files and Templates

#### JavaScript and Styles

All frontend interactivity and visuals are handled through JS/CSS inside the `static/` directory.

#### HTML Templates

* `dashboard.html` – Real-time interactive dashboard.
* `order_data.html` – Tabular summary of orders and customers.

---

### 📊 Dashboard Features

Preview:
![Dashboard](path/to/Dashboard.png)

#### 1. Add New Customer

* Add customers directly to the RDS backend.
* See new entries reflected instantly in UI.

#### 2. Add New Order

* Add new orders to customers in real time.

#### 3. Customer Orders Section

* Select a customer and view their transaction history.
* Includes a **View Orders** button to fetch detailed history.

#### 4. Real-Time Charts and Graphs

* **Line Chart**: Tracks customer spending over time.
* **Donut Chart**: Visualizes order distribution.
* Fully interactive: Add data and watch charts update instantly.

#### 5. Summary Cards

Top section contains 4 responsive cards showing:

* Total Customers
* Total Orders
* Total Revenue
* Average Order Value

#### 6. Dashboard Navigation

Top-right corner provides navigation links:

* Dashboard
* View Orders

---

### 📄 View Orders Page

Preview:
![View Orders](path/to/ViewOrders.png)

#### 1. Filter and Sort Orders

Sort based on:

* Completed Orders
* Pending Orders
* Cancelled Orders

#### 2. Top Customers

View your top five customers by revenue.

#### 3. Monthly Sales Report

Track monthly completed orders and totals.

#### 4. Unsold Products

See products in your catalog that were **never sold**.

> *(Note: Product table is placeholder for future expansion.)*

#### 5. Average Order by Location

Get geographic insights into customer spending.

#### 6. Frequent Buyers

Identify repeat customers based on order frequency.



