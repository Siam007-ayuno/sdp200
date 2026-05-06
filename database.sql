CREATE DATABASE IF NOT EXISTS safezone_db;
USE safezone_db;

CREATE TABLE IF NOT EXISTS areas (
    area_id INT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    current_score INT DEFAULT 100,
    current_status VARCHAR(50) DEFAULT 'Safe'
);

CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    area_id INT,
    incident_type VARCHAR(255) NOT NULL,
    severity INT CHECK (severity BETWEEN 1 AND 5),
    description TEXT,
    report_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    reporter_name VARCHAR(255),
    contact VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (area_id) REFERENCES areas(area_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Insert sample areas
INSERT INTO areas (area_name, city, state, current_score, current_status) VALUES
('Mohammadpur', 'Dhaka', 'Dhaka', 100, 'Safe'),
('Mirpur', 'Dhaka', 'Dhaka', 100, 'Safe'),
('Gulshan', 'Dhaka', 'Dhaka', 100, 'Safe'),
('Banani', 'Dhaka', 'Dhaka', 100, 'Safe');

-- Insert sample reports
INSERT INTO reports (area_id, incident_type, severity, description, reporter_name, status) VALUES
(1, 'Theft', 3, 'Phone snatched near bus stand', 'John Doe', 'approved'),
(3, 'Violence', 5, 'Mugging near the park', 'Jane Smith', 'approved'),
(3, 'Harassment', 4, 'Eve teasing on main street', '', 'approved');

-- Insert default admin (password: admin123)
INSERT INTO admins (username, password_hash) VALUES
('admin', 'admin123');
