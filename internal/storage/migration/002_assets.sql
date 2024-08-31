
-- Asset table
CREATE TABLE asset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,  -- e.g., 'stock', 'real_estate', 'art'
    asset_symbol VARCHAR(10) NULL,
    description VARCHAR(250),
    country VARCHAR(100) DEFAULT 'PK',
    currency VARCHAR(3) NOT NULL DEFAULT 'PKR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,  -- Foreign key to asset table
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    market VARCHAR(50) NOT NULL DEFAULT 'PSX',
    sector VARCHAR(100),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_id_stock (asset_id),
    FOREIGN KEY (asset_id) REFERENCES asset(id) ON DELETE CASCADE
);


CREATE TABLE live_traded_asset_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    price decimal(9, 2) NOT NULL,
    volume_traded decimal(16, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_id_live (asset_id)
);

CREATE TABLE daily_traded_asset_positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    date DATE NOT NULL,
    opening_price DECIMAL(9, 2) NOT NULL,
    closing_price DECIMAL(9, 2) NOT NULL,
    high_price DECIMAL(9, 2) NOT NULL,
    low_price DECIMAL(9, 2) NOT NULL,
    total_volume DECIMAL(16, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(asset_id, date),  -- Ensure only one record per asset per day
    INDEX idx_asset_id_daily (asset_id)
);