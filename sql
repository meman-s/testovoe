SELECT 
    e.name AS employee_name,
    p.salary AS salary,
    (p.salary * c.tax_percentage / 100) AS tax_amount
FROM employees AS e
JOIN 
    positions AS p ON e.position_id = p.id
JOIN 
    contracts AS c ON e.contract_id = c.id
WHERE 
    p.salary < 50000;
