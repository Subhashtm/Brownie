-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url TEXT,
    category VARCHAR(100) DEFAULT 'brownie',
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cart table
CREATE TABLE IF NOT EXISTS cart (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_receipt_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Create settings table for admin configurations
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample products
INSERT INTO products (name, description, price, category, image_url) VALUES
('Classic Chocolate Brownie', 'Rich and fudgy chocolate brownie made with premium cocoa', 199.99, 'brownie', ''),
('Walnut Brownie', 'Chocolate brownie loaded with crunchy walnuts', 249.99, 'brownie', ''),
('Salted Caramel Brownie', 'Decadent brownie with salted caramel swirl', 299.99, 'brownie', ''),
('Double Chocolate Brownie', 'Extra chocolatey brownie with chocolate chips', 229.99, 'brownie', ''),
('Peanut Butter Brownie', 'Chocolate brownie with creamy peanut butter layers', 269.99, 'brownie', ''),
('Mint Chocolate Brownie', 'Refreshing mint-infused chocolate brownie', 249.99, 'brownie', '');

-- Insert default settings
INSERT INTO settings (key, value) VALUES
('contact_info', '{"email": "contact@brownieshop.com", "phone": "+91-9876543210", "address": "123 Brownie Street, Sweet City, Mumbai, Maharashtra 400001"}'),
('payment_info', '{"qr_code_url": "", "payment_email": "payments@brownieshop.com"}');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_available ON products(available);
CREATE INDEX IF NOT EXISTS idx_cart_user_email ON cart(user_email);
CREATE INDEX IF NOT EXISTS idx_orders_user_email ON orders(user_email);
CREATE INDEX IF NOT EXISTS idx_settings_key ON settings(key);