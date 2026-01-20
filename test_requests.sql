SELECT 
    c.name as client_name,
    SUM(oi.quantity * oi.price) as total_spent
FROM clients c
JOIN orders o ON c.id = o.client_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC;

SELECT 
    parent.name as parent_category,
    COUNT(child.id) as children_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
HAVING COUNT(child.id) > 0
ORDER BY children_count DESC;

CREATE OR REPLACE VIEW top_products_last_month AS
SELECT 
    n.name as product_name,
    c.name as category,
    SUM(oi.quantity) as total_sold
FROM nomenclature n
JOIN order_items oi ON n.id = oi.nomenclature_id
JOIN orders o ON oi.order_id = o.id
LEFT JOIN categories c ON n.category_id = c.id
WHERE o.date >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY n.id, n.name, c.name
ORDER BY total_sold DESC
LIMIT 5;


/*
    Для оптимизации последнего запроса в условиях роста данных нужно создать индексы для фильтрации по дате:
    CREATE INDEX idx_orders_date ON orders(date);
    Если данных будет достаточно много, логично будет использовать партицирование.
*/
