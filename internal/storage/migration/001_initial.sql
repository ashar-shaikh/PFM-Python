CREATE TABLE rss_feeds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feed_link VARCHAR(255) NOT NULL,
    lang varchar(2) NULL DEFAULT 'en',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_successfully_monitored TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE background_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name ENUM('rss_feed_updates', 'content_analysis') NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    row_count INT NOT NULL,
    status ENUM('pending', 'in_progress', 'completed', 'failed') NOT NULL DEFAULT 'pending',
    completed_rows INT DEFAULT 0,
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE news_content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feed_id INT NOT NULL,
    guid VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    link VARCHAR(255),
    pub_date DATETIME,
    description TEXT,
    content TEXT,
    is_discarded BOOLEAN NOT NULL DEFAULT FALSE,
    is_analyzed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE content_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT NOT NULL,
    classification VARCHAR(255),
    sentiment VARCHAR(50),
    summary VARCHAR(400),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Asset table
CREATE TABLE asset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(50) NOT NULL DEFAULT 'stock',
    description varchar(250) null,
    market VARCHAR(50) NOT NULL DEFAULT 'PSX',
    sector VARCHAR(100),
    industry VARCHAR(100),
    country VARCHAR(100) default 'PK',
    currency VARCHAR(3) NOT NULL DEFAULT 'PKR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE live_asset_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    price decimal(9, 2) NOT NULL,
    volume_traded decimal(16, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_id_live (asset_id)
);

CREATE TABLE daily_asset_positions (
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