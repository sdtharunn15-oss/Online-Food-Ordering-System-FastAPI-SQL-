-- SQLite
PRAGMA table_info(orders);

SELECT
    food_item_id,
    SUM(quantity) AS total_sold
FROM orders
GROUP BY food_item_id
ORDER BY total_sold DESC;


SELECT
    SUM(total_amount) AS total_revenue
FROM orders;

SELECT
    c.id,
    c.name,
    c.email,
    COUNT(o.id) AS total_orders
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
HAVING COUNT(o.id) > 3;

SELECT
    r.id,
    r.name,
    SUM(o.quantity) AS total_orders
FROM restaurants r
JOIN food_items f ON r.id = f.restaurant_id
JOIN orders o ON f.id = o.food_item_id
GROUP BY r.id, r.name
ORDER BY total_orders DESC;


SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY DATE(created_at);

SELECT
    food_item_id,
    SUM(quantity) AS total_sold,
    RANK() OVER (ORDER BY SUM(quantity) DESC) AS rank_position
FROM orders
GROUP BY food_item_id;