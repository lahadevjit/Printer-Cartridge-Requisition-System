# Printer-Cartridge-Requisition-System
A role-based Django web application for managing cartridge and ink requisition requests within an organization.

## 📌 Introduction

This project is a role-based web application developed using Django to manage cartridge and ink requisitions within an organization. The system digitizes the process of requesting, approving, issuing, and reporting printer cartridge usage. It supports multiple roles — **Employee**, **HOD**, and **Admin** — each with distinct access and functionality.

The platform ensures transparency, efficient tracking, and accountability in consumable resource management while reducing paperwork and manual errors. It supports dynamic field population, validation, email notifications, and a clean user interface for streamlined operations.

---

## 🛠 Technologies Used

### 🔸 Frontend
- **HTML5**, **CSS3** for layout and design
- **JavaScript** and **AJAX** for interactivity and live validations
- **Bootstrap** for responsive UI components

### 🔸 Backend
- **Django** (Python) as the primary backend framework
- **Django ORM** for secure and scalable database interaction

### 🔸 Database
- **SQLite3** for local development and testing
- Supports upgrade to **PostgreSQL** or **MySQL** for production

### 🔸 Security
- Django’s built-in **authentication system**
- **CSRF protection**, **role-based access control**, and **server-side validation**

---

## 🔧 Installation & Run Locally

### ✅ Step 1: Install dependencies

```bash
pip install django

✅ Step 2: Clone the repository
git clone https://github.com/your-username/cartridge-requisition-system.git

✅ Step 3: Run the application
cd cartridge-requisition-system
python manage.py runserver


cartridge-requisition-system/
│
├── templates/
│   ├── request_form.html
│   ├── status_page.html
│   ├── approve_page.html
│   ├── issue_page.html
│   └── report_page.html
│
├── requisition/           
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── db.sqlite3
├── manage.py
└── README.md

