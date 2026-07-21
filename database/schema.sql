-- MotoERP Database Schema for Supabase

-- Create clients table
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    type VARCHAR(50) NOT NULL CHECK (type IN ('persoană', 'service', 'magazin', 'dealer')),
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    credit_limit DECIMAL(12, 2) DEFAULT 0,
    total_purchases DECIMAL(12, 2) DEFAULT 0,
    profit_generated DECIMAL(12, 2) DEFAULT 0,
    last_order_date TIMESTAMP,
    observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    contact_person VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    website VARCHAR(255),
    currency VARCHAR(3) DEFAULT 'EUR',
    avg_delivery_time INTEGER,
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    operator VARCHAR(255),
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'cerere', 'ofertă trimisă', 'confirmată', 'comandată la furnizor',
        'în transport', 'ajunsă', 'livrată', 'finalizată', 'anulată'
    )),
    total_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    profit DECIMAL(12, 2) DEFAULT 0,
    observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create parts table
CREATE TABLE IF NOT EXISTS parts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    oem_code VARCHAR(100) NOT NULL UNIQUE,
    supplier_code VARCHAR(100),
    brand VARCHAR(100),
    model VARCHAR(100),
    year VARCHAR(4),
    category VARCHAR(50) NOT NULL CHECK (category IN (
        'motor', 'frâne', 'suspensie', 'electric', 'alt'
    )),
    supplier_cost DECIMAL(12, 2) NOT NULL,
    transport_cost DECIMAL(12, 2) DEFAULT 0,
    taxes DECIMAL(12, 2) DEFAULT 0,
    tva DECIMAL(12, 2) DEFAULT 0,
    final_cost DECIMAL(12, 2),
    sale_price DECIMAL(12, 2) NOT NULL,
    profit DECIMAL(12, 2),
    margin_percent DECIMAL(5, 2),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create price history table
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID NOT NULL REFERENCES parts(id) ON DELETE CASCADE,
    old_price DECIMAL(12, 2),
    new_price DECIMAL(12, 2) NOT NULL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transport table
CREATE TABLE IF NOT EXISTS transport (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    supplier_id UUID REFERENCES suppliers(id),
    tracking_number VARCHAR(100),
    courier VARCHAR(100),
    weight DECIMAL(10, 2),
    volume DECIMAL(10, 2),
    total_cost DECIMAL(12, 2) NOT NULL DEFAULT 0,
    distribution_method VARCHAR(50) CHECK (distribution_method IN ('greutate', 'volum', 'egal', 'manual')),
    departure_date TIMESTAMP,
    arrival_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('furnizor', 'client')),
    invoice_number VARCHAR(100) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    vat DECIMAL(12, 2) DEFAULT 0,
    paid_amount DECIMAL(12, 2) DEFAULT 0,
    outstanding_amount DECIMAL(12, 2),
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) NOT NULL CHECK (category IN (
        'internet', 'marketing', 'transport', 'comisioane bancă',
        'combustibil', 'ambalaje', 'salarii', 'alt'
    )),
    amount DECIMAL(12, 2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order items table (piese in comenzi)
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    part_id UUID NOT NULL REFERENCES parts(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(12, 2) NOT NULL,
    total_price DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create wishlist table
CREATE TABLE IF NOT EXISTS wishlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    part_id UUID NOT NULL REFERENCES parts(id) ON DELETE CASCADE,
    notes TEXT,
    follow_up_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create blacklist table
CREATE TABLE IF NOT EXISTS blacklist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order documents table
CREATE TABLE IF NOT EXISTS order_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    document_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_clients_email ON clients(email);
CREATE INDEX idx_clients_phone ON clients(phone);
CREATE INDEX idx_orders_client_id ON orders(client_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_parts_oem_code ON parts(oem_code);
CREATE INDEX idx_parts_brand ON parts(brand);
CREATE INDEX idx_parts_category ON parts(category);
CREATE INDEX idx_transport_order_id ON transport(order_id);
CREATE INDEX idx_invoices_order_id ON invoices(order_id);
CREATE INDEX idx_expenses_category ON expenses(category);
CREATE INDEX idx_expenses_date ON expenses(expense_date);

-- Enable RLS (Row Level Security) if needed
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE transport ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
