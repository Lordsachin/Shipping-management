-- PostgreSQL setup script for shipping_db
-- Database: Supabase (AWS PostgreSQL)
-- If your cloud provider already gives a database, skip CREATE DATABASE and connect directly.
-- Note: This file uses PostgreSQL-specific syntax (SERIAL, ON CONFLICT, LANGUAGE plpgsql, etc.)

CREATE DATABASE shipping_db;

-- Connect to shipping_db before running the rest of this script.

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipping_methods (
    method_id SERIAL PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL,
    cost_per_km NUMERIC(10, 2) NOT NULL,
    speed VARCHAR(20)
);

INSERT INTO shipping_methods (method_name, cost_per_km, speed) VALUES
('Sea', 2.00, 'Slow'),
('Road', 5.00, 'Medium'),
('Air', 10.00, 'Fast'),
('Rail', 3.00, 'Medium')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(15),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    method_id INT REFERENCES shipping_methods(method_id),
    distance_km NUMERIC(10, 2),
    total_cost NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS tracking (
    tracking_id VARCHAR(50) PRIMARY KEY,
    shipment_id INT REFERENCES shipments(shipment_id),
    current_status VARCHAR(50) DEFAULT 'Order Placed',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional trigger to auto-update tracking.last_updated
CREATE OR REPLACE FUNCTION set_last_updated()
RETURNS TRIGGER AS $$
BEGIN
  NEW.last_updated = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_set_last_updated ON tracking;
CREATE TRIGGER trg_set_last_updated
BEFORE UPDATE ON tracking
FOR EACH ROW
EXECUTE FUNCTION set_last_updated();

SELECT * FROM shipping_methods;
