CREATE TABLE categories(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 name VARCHAR(255) NOT NULL,
 parent_id UUID REFERENCES categories(id) ON DELETE CASCADE,

 CONSTRAINT valid_parent CHECK (id != parent_id)
);

CREATE TABLE nomenclature(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 name VARCHAR(255) NOT NULL,
 quantity INTEGER NOT NULL DEFAULT 0,
 price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
 category_id UUID REFERENCES categories(id) ON DELETE SET NULL,

 CONSTRAINT non_negative_quantity CHECK (quantity >= 0),
    CONSTRAINT non_negative_price CHECK (price >= 0)
);

CREATE TABLE clients(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 name VARCHAR(255) NOT NULL,
 address TEXT
);

CREATE TABLE orders(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
 date TIMESTAMP NOT  NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
 nomenclature_id UUID NOT NULL REFERENCES nomenclature(id) ON DELETE RESTRICT,
 quantity INTEGER NOT NULL,
 price DECIMAL(10,2) NOT NULL,
 
 CONSTRAINT non_negative_quantity CHECK (quantity > 0),
    CONSTRAINT non_negative_price CHECK (price >= 0),
 UNIQUE (order_id,nomenclature_id)
);

CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_nomenclature_category_id ON nomenclature(category_id);
CREATE INDEX idx_orders_client_id ON orders(client_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_nomenclature_id ON order_items(nomenclature_id);