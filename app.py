from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = "food-analytics-secret-key"


# =========================
# MYSQL CONNECTION
# =========================

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST", "localhost"),
    port=int(os.getenv("MYSQLPORT", "3306")),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQLDATABASE", "food_delivery")
)


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = %s
            AND password = %s
        """, (email, password))

        user = cursor.fetchone()

        cursor.close()

        if user:

            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("home"))

        else:
            error = "Invalid email or password."

    return render_template(
        "login.html",
        error=error
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                error="Password must be at least 6 characters."
            )

        cursor = db.cursor(dictionary=True)

        # Check email

        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_email = cursor.fetchone()

        if existing_email:

            cursor.close()

            return render_template(
                "register.html",
                error="Email is already registered."
            )

        # Check username

        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s",
            (username,)
        )

        existing_username = cursor.fetchone()

        if existing_username:

            cursor.close()

            return render_template(
                "register.html",
                error="Username already exists."
            )

        # Insert new user

        cursor.execute("""
            INSERT INTO users
            (username, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (
            username,
            email,
            password,
            "Analyst"
        ))

        db.commit()

        cursor.close()

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        error=error
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "profile/about.html"
    )


# =========================
# EDIT PROFILE
# =========================

@app.route("/edit-profile")
def edit_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "profile/edit_profile.html",
        username=session.get("username", "")
    )


# =========================
# SAVED
# =========================

@app.route("/saved")
def saved():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "profile/saved.html"
    )


# =========================
# FEEDBACK
# =========================

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        feedback_text = request.form.get("feedback")

        print("Feedback received:")
        print("Name:", name)
        print("Email:", email)
        print("Feedback:", feedback_text)

        return render_template(
            "profile/feedback.html"
        )

    return render_template(
        "profile/feedback.html"
    )


# =========================
# SETTINGS
# =========================

@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "profile/settings.html"
    )


# =========================
# DASHBOARD
# =========================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get filters from header

    search = request.args.get("search", "").strip()
    city_filter = request.args.get("city", "").strip()
    status_filter = request.args.get("status", "").strip()

    cursor = db.cursor(dictionary=True)


    # =========================
    # COMMON FILTER
    # =========================

    filter_query = ""
    filter_params = []

    if search:

        filter_query += """
            AND (
                c.customer_name LIKE %s
                OR r.restaurant_name LIKE %s
            )
        """

        search_value = "%" + search + "%"

        filter_params.extend([
            search_value,
            search_value
        ])

    if city_filter:

        filter_query += """
            AND c.city = %s
        """

        filter_params.append(city_filter)

    if status_filter:

        filter_query += """
            AND o.status = %s
        """

        filter_params.append(status_filter)


    # =========================
    # TOTAL ORDERS
    # =========================

    cursor.execute(
        """
        SELECT COUNT(*) AS total_orders
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query,
        filter_params
    )

    total_orders = cursor.fetchone()["total_orders"]


    # =========================
    # TOTAL CUSTOMERS
    # =========================

    cursor.execute(
        """
        SELECT COUNT(DISTINCT c.customer_id) AS total_customers
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query,
        filter_params
    )

    total_customers = cursor.fetchone()["total_customers"]


    # =========================
    # TOTAL RESTAURANTS
    # =========================

    cursor.execute(
        """
        SELECT COUNT(DISTINCT r.restaurant_id) AS total_restaurants
        FROM restaurants r
        JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        JOIN customers c
            ON c.customer_id = o.customer_id
        WHERE 1 = 1
        """ + filter_query,
        filter_params
    )

    total_restaurants = cursor.fetchone()["total_restaurants"]


    # =========================
    # TOTAL REVENUE
    # Delivered orders only
    # =========================

    cursor.execute(
        """
        SELECT COALESCE(SUM(o.amount), 0) AS total_revenue
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Delivered'
        """ + filter_query,
        filter_params
    )

    total_revenue = cursor.fetchone()["total_revenue"]


    # =========================
    # CANCELLED ORDERS
    # =========================

    cursor.execute(
        """
        SELECT COUNT(*) AS cancelled_orders
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Cancelled'
        """ + filter_query,
        filter_params
    )

    cancelled_orders = cursor.fetchone()["cancelled_orders"]


    # =========================
    # AVERAGE ORDER VALUE
    # =========================

    cursor.execute(
        """
        SELECT ROUND(
            COALESCE(AVG(o.amount), 0),
            2
        ) AS average_order_value
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Delivered'
        """ + filter_query,
        filter_params
    )

    average_order_value = cursor.fetchone()["average_order_value"]


    # =========================
    # STATUS DATA
    # =========================

    cursor.execute(
        """
        SELECT
            o.status,
            COUNT(*) AS total_orders
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY o.status
        ORDER BY total_orders DESC
        """,
        filter_params
    )

    status_data = cursor.fetchall()


    # =========================
    # DELIVERY SUCCESS RATE
    # =========================

    cursor.execute(
        """
        SELECT ROUND(
            (
                SUM(
                    CASE
                        WHEN o.status = 'Delivered'
                        THEN 1
                        ELSE 0
                    END
                ) / NULLIF(COUNT(*), 0)
            ) * 100,
            1
        ) AS delivery_success_rate
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query,
        filter_params
    )

    result = cursor.fetchone()

    delivery_success_rate = result["delivery_success_rate"]

    if delivery_success_rate is None:
        delivery_success_rate = 0


    # =========================
    # ALL CITIES
    # =========================

    cursor.execute("""
        SELECT DISTINCT city
        FROM customers
        ORDER BY city
    """)

    all_cities = cursor.fetchall()


    # =========================
    # RESTAURANT DATA
    # =========================

    cursor.execute(
        """
        SELECT
            r.restaurant_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.amount) AS total_revenue
        FROM restaurants r
        JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        JOIN customers c
            ON c.customer_id = o.customer_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY r.restaurant_name
        ORDER BY total_revenue DESC
        """,
        filter_params
    )

    restaurant_data = cursor.fetchall()


    # =========================
    # CUSTOMER DATA
    # =========================

    cursor.execute(
        """
        SELECT
            c.customer_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.amount) AS total_spent
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY c.customer_name
        ORDER BY total_spent DESC
        """,
        filter_params
    )

    customer_data = cursor.fetchall()


    # =========================
    # CITY DATA
    # =========================

    cursor.execute(
        """
        SELECT
            c.city,
            COUNT(o.order_id) AS total_orders,
            SUM(o.amount) AS total_revenue
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY c.city
        ORDER BY total_orders DESC
        """,
        filter_params
    )

    city_data = cursor.fetchall()


    # =========================
    # MOST POPULAR RESTAURANT
    # =========================

    cursor.execute(
        """
        SELECT
            r.restaurant_name,
            COUNT(o.order_id) AS total_orders
        FROM restaurants r
        JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        JOIN customers c
            ON c.customer_id = o.customer_id
        WHERE o.status = 'Delivered'
        """ + filter_query + """
        GROUP BY r.restaurant_name
        ORDER BY total_orders DESC
        LIMIT 1
        """,
        filter_params
    )

    popular_restaurant = cursor.fetchone()


    # =========================
    # RESTAURANT REVENUE CHART
    # =========================

    cursor.execute(
        """
        SELECT
            r.restaurant_name,
            COALESCE(SUM(o.amount), 0) AS total_revenue
        FROM restaurants r
        JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        JOIN customers c
            ON c.customer_id = o.customer_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY r.restaurant_name
        ORDER BY total_revenue DESC
        """,
        filter_params
    )

    restaurant_chart_data = cursor.fetchall()


    # =========================
    # CITY ORDERS CHART
    # =========================

    cursor.execute(
        """
        SELECT
            c.city,
            COUNT(o.order_id) AS total_orders
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE 1 = 1
        """ + filter_query + """
        GROUP BY c.city
        ORDER BY total_orders DESC
        """,
        filter_params
    )

    city_chart_data = cursor.fetchall()


    # =========================
    # HIGHEST REVENUE RESTAURANT
    # =========================

    cursor.execute(
        """
        SELECT
            r.restaurant_name,
            COALESCE(SUM(o.amount), 0) AS total_revenue
        FROM restaurants r
        JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        JOIN customers c
            ON c.customer_id = o.customer_id
        WHERE o.status = 'Delivered'
        """ + filter_query + """
        GROUP BY r.restaurant_name
        ORDER BY total_revenue DESC
        LIMIT 1
        """,
        filter_params
    )

    highest_revenue_restaurant = cursor.fetchone()


    # =========================
    # HIGHEST SPENDING CUSTOMER
    # =========================

    cursor.execute(
        """
        SELECT
            c.customer_name,
            COALESCE(SUM(o.amount), 0) AS total_spending
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Delivered'
        """ + filter_query + """
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spending DESC
        LIMIT 1
        """,
        filter_params
    )

    highest_spending_customer = cursor.fetchone()


    # =========================
    # MONTHLY REVENUE TREND
    # =========================
    # Multiple months ke delivered revenue ke liye

    cursor.execute(
        """
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m') AS month,
            COALESCE(SUM(o.amount), 0) AS revenue
        FROM orders o
        JOIN customers c
            ON c.customer_id = o.customer_id
        JOIN restaurants r
            ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Delivered'
        """ + filter_query + """
        GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
        ORDER BY month ASC
        """,
        filter_params
    )

    monthly_revenue = cursor.fetchall()


    # =========================
    # CLOSE CURSOR
    # =========================

    cursor.close()


    # =========================
    # SEND DATA TO HTML
    # =========================

    return render_template(
        "index.html",

        total_orders=total_orders,
        total_customers=total_customers,
        total_restaurants=total_restaurants,
        total_revenue=total_revenue,

        cancelled_orders=cancelled_orders,
        average_order_value=average_order_value,

        restaurant_data=restaurant_data,
        customer_data=customer_data,
        city_data=city_data,

        restaurant_chart_data=restaurant_chart_data,
        city_chart_data=city_chart_data,

        all_cities=all_cities,

        popular_restaurant=popular_restaurant,

        highest_revenue_restaurant=highest_revenue_restaurant,
        highest_spending_customer=highest_spending_customer,

        monthly_revenue=monthly_revenue,

        status_data=status_data,
        delivery_success_rate=delivery_success_rate,

        username=session.get("username"),
        role=session.get("role"),

        search=search,
        city_filter=city_filter,
        status_filter=status_filter
    )


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)