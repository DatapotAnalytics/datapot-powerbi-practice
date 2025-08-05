
SELECT * FROM dbo.tiki_product_history;
SELECT * FROM dbo.tiki_test;
SELECT * FROM dbo.tiki_X_table;
SELECT * FROM dbo.tiki_Y_table;

-- ===================================================================================
-- Question 1 
-- (a)  Write a SQL query to find the best seller by each category.
SELECT SellerID, Category, Sales_Millions_VND
FROM
(

            SELECT SellerID, Category, Sales_Millions_VND,
                    RANK() OVER (PARTITION BY Category ORDER BY Sales_Millions_VND DESC) AS Rank
            FROM dbo.tiki_X_table

) AS T1     
WHERE Rank = 1;

-- (b) Write a SQL query to find of 3 best sellers in (a), how many award did they received in 2017.

SELECT Seller_ID, Category,
        COUNT (CASE WHEN Award_Year = 2017 THEN 1 ELSE NULL END) AS Award_In_2017
FROM dbo.tiki_Y_table AS T1
JOIN
        (
        SELECT SellerID, Category, Sales_Millions_VND
        FROM
        (

                SELECT SellerID, Category, Sales_Millions_VND,
                        RANK() OVER (PARTITION BY Category ORDER BY Sales_Millions_VND DESC) AS Rank
                FROM dbo.tiki_X_table

        ) AS T1     
        WHERE Rank = 1
        )  AS T2
ON T1.Seller_ID = T2. SellerID
GROUP BY Seller_ID, Category
ORDER BY Category;

-- ===================================================================================
-- Question 2
-- (a) Write a SQL query to find the number of product that were available for sales at the end of each month. 

WITH MonthlyProductAvailability AS (
  SELECT
    FORMAT(ph.date, 'y') AS Month, --DATEPART(month, ph.date)
    COUNT(DISTINCT CASE WHEN ph.product_status = 'ON' THEN ph.product_id ELSE NULL END) AS ProductsAvailable
  FROM dbo.tiki_product_history ph
  GROUP BY FORMAT(ph.date, 'y') --DATEPART(month, ph.date)
)
SELECT *
FROM MonthlyProductAvailability
ORDER BY Month;


-- (b) Average stock is calculated as: Total stock in a month/ total date in a month. Write a SQL query to find Product ID with the most “average stock” by month.
WITH MonthlyAverageStock AS (
  SELECT
    FORMAT(ph.date, 'y') AS Month,
    ph.product_id,
    AVG(ph.stock) AS AverageStock
  FROM dbo.tiki_product_history ph
  GROUP BY FORMAT(ph.date, 'y'), ph.product_id
--   order by FORMAT(ph.date, 'y')
)
, MonthlyAverageStock_RANK AS (
SELECT
  Month,
  product_id,
  AverageStock,
  RANK() OVER(PARTITION BY Month ORDER BY AverageStock DESC) AS RANK
FROM MonthlyAverageStock
)
SELECT * 
FROM MonthlyAverageStock_RANK
WHERE RANK = 1
ORDER BY Month;






