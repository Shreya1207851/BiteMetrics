# 🍔 BiteMetrics — Food Delivery Analytics Dashboard

BiteMetrics is a food delivery analytics dashboard built using Flask, MySQL, SQL, HTML, CSS and JavaScript.

The project analyzes food delivery data to provide insights into orders, revenue, customers, restaurants, cities and delivery performance.

## 📊 Dashboard Features

- Total Orders
- Total Customers
- Total Restaurants
- Total Revenue
- Restaurant-wise Performance
- Customer Spending Analysis
- City-wise Analysis
- Order Status Overview
- Delivery Success Rate
- Average Order Value
- Popular Restaurant Analysis
- Monthly Revenue Trend
- Search and Filters
- Dark / Light Mode
- User Login and Registration
- Profile Section

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Analytics:** SQL
- **Version Control:** Git & GitHub

## 🧮 SQL Concepts Used

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- COUNT()
- SUM()
- AVG()
- JOIN
- HAVING
- CASE

## 📁 Project Structure

```text
BiteMetrics/
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── login.css
│   ├── edit_profile.css
│   ├── saved.css
│   ├── feedback.css
│   ├── about.css
│   └── settings.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── profile/
│
├── app.py
├── database.sql
├── requirements.txt
└── .gitignore

How to Run Locally
1. Clone the repository
git clone https://github.com/Shreya1207851/BiteMetrics.git
2. Open the project
cd BiteMetrics
3. Create and activate a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Configure MySQL
