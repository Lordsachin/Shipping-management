-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS shipping_db;
USE shipping_db;

-- 2. Create 'Shipping_Methods' Table (Reference Data)
-- We create this first because 'Shipments' needs to refer to it.
CREATE TABLE IF NOT EXISTS Shipping_Methods (
    Method_ID INT AUTO_INCREMENT PRIMARY KEY,
    Method_Name VARCHAR(50) NOT NULL,
    Cost_per_km DECIMAL(10, 2) NOT NULL,
    Speed VARCHAR(20)
);

-- 3. Insert the standard Shipping Rates (From your project logic)
INSERT INTO Shipping_Methods (Method_Name, Cost_per_km, Speed) VALUES 
('Sea', 2.00, 'Slow'),
('Road', 5.00, 'Medium'),
('Air', 10.00, 'Fast'),
('Rail', 3.00, 'Medium');

-- 4. Create 'Orders' Table (Customer Info)
CREATE TABLE IF NOT EXISTS Orders (
    Order_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_Name VARCHAR(100) NOT NULL,
    Address TEXT NOT NULL,
    Phone VARCHAR(15),
    Order_Date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create 'Shipments' Table (The Core Logic)
CREATE TABLE IF NOT EXISTS Shipments (
    Shipment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID INT,
    Method_ID INT,
    Distance_km DECIMAL(10, 2),
    Total_Cost DECIMAL(10, 2),
    
    -- Foreign Keys link these tables together
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    FOREIGN KEY (Method_ID) REFERENCES Shipping_Methods(Method_ID)
);

-- 6. Create 'Tracking' Table (Status Updates)
CREATE TABLE IF NOT EXISTS Tracking (
    Tracking_ID VARCHAR(50) PRIMARY KEY, -- Example: TRK-1001
    Shipment_ID INT,
    Current_Status VARCHAR(50) DEFAULT 'Order Placed',
    Last_Updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Shipment_ID) REFERENCES Shipments(Shipment_ID)
);

-- Verify that tables are created
SHOW TABLES;
SELECT * FROM Shipping_Methods;