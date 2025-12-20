# 💸 Smart Expense Splitter (Django)

A simple, clean, and practical Django web application to split group expenses fairly and calculate who owes whom.  
Inspired by real-world tools like Splitwise, this project focuses on clear backend logic and a minimalist UI.

---

## 🚀 Features

- User authentication (Sign up / Login / Logout)
- Create and manage expense groups
- Add members using names only
- Add, edit, and delete expenses
- Automatic equal expense splitting
- Smart settlement calculation (who pays whom)
- Clean, modern, minimalist UI
- Refactored business logic for maintainability

---

## 🛠 Tech Stack

- Backend: Python, Django  
- Database: SQLite  
- Frontend: HTML, CSS  
- Authentication: Django Auth  
- Version Control: Git, GitHub  

---

## 📂 Project Structure

expense_project/
├── manage.py
├── expense_project/
│ ├── settings.py
│ └── urls.py
├── splitter/
│ ├── models.py
│ ├── views.py
│ ├── services.py
│ ├── urls.py
│ └── templates/
├── templates/
│ ├── base.html
│ └── auth/
├── static/
│ └── css/
│ └── styles.css



---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/naveenk2932/expense-splitter.git
cd smart-expense-splitter
pip install django
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
