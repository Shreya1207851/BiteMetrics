# 🍔 BiteMetrics — Food Delivery Analytics Dashboard

BiteMetrics is a food delivery analytics dashboard built using **Flask, MySQL, SQL, HTML, CSS and JavaScript**.

The project analyzes food delivery data to provide insights into **orders, revenue, customers, restaurants, cities and delivery performance**.

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
```

🚀 How to Run Locally
1. Clone the repository
```
git clone https://github.com/Shreya1207851/BiteMetrics.git
```
2. Open the project
 ```
cd BiteMetrics
```
5. Create and activate a virtual environment
```
python -m venv .venv
```
Activate it on Windows:
```
.venv\Scripts\activate
```
4. Install Dependencies
```
pip install -r requirements.txt
```
5. Configure MySQL
```
database.sql
```
Create a ```.env``` file in the project root:
```
MYSQLHOST=localhost
MYSQLPORT=3306
MYSQLUSER=root
MYSQLPASSWORD=your_mysql_password
MYSQLDATABASE=food_delivery
```
6. Run the Flask application
```
python app.py
```

🔐 Security
- Database credentials are stored in environment variables.
- Sensitive configuration is stored in ```.env```.
- The ```.env``` file is excluded from Git using ```.gitignore```.

🎯 Project Purpose

The main purpose of BiteMetrics is to practice SQL and relational database concepts through a practical food delivery analytics application.

It combines SQL-based data analysis with a Flask web dashboard to turn raw food delivery data into useful business insights.

🔮 Future Improvements
- Date-range analytics
- Real-time data
- Restaurant comparison
- Customer segmentation
- Predictive analytics
- Automated reports
- Advanced role-based access

## 👩‍💻 Author

**Shreya Kaushal**

GitHub: [Shreya1207851](https://github.com/Shreya1207851)

