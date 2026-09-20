CREATE DATABASE food_delivery;

USE food_delivery;

-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

-- Restaurants table
CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    city VARCHAR(50),
    cuisine VARCHAR(50)
);

-- Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    restaurant_id INT,
    order_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR(20),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Customers data
INSERT INTO customers VALUES
(1, 'Rahul', 'Ludhiana'),
(2, 'Priya', 'Delhi'),
(3, 'Aman', 'Mumbai'),
(4, 'Neha', 'Chandigarh'),
(5, 'Rohit', 'Amritsar');

-- Restaurants data
INSERT INTO restaurants VALUES
(1, 'Food Hub', 'Ludhiana', 'Indian'),
(2, 'Pizza House', 'Delhi', 'Italian'),
(3, 'Burger Point', 'Mumbai', 'Fast Food'),
(4, 'Spice Garden', 'Chandigarh', 'Indian'),
(5, 'Tandoori Nights', 'Amritsar', 'Punjabi');

-- Orders data
INSERT INTO orders VALUES
(101, 1, 1, '2026-09-01', 450.00, 'Delivered'),
(102, 2, 2, '2026-09-01', 700.00, 'Delivered'),
(103, 3, 3, '2026-09-02', 350.00, 'Cancelled'),
(104, 1, 4, '2026-09-02', 600.00, 'Delivered'),
(105, 4, 4, '2026-09-03', 800.00, 'Delivered'),
(106, 5, 5, '2026-09-03', 550.00, 'Delivered'),
(107, 2, 2, '2026-09-04', 900.00, 'Delivered'),
(108, 3, 3, '2026-09-04', 400.00, 'Delivered'),
(109, 1, 1, '2026-09-05', 750.00, 'Delivered'),
(110, 5, 5, '2026-09-05', 650.00, 'Cancelled');

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Analyst'
);