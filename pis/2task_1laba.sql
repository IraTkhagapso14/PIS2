CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    otch VARCHAR(50),
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    driver_license VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE cars (
    car_id INT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    type VARCHAR(30) NOT NULL,
    daily_rental_rate DECIMAL(10, 2) NOT NULL,
    purchase_price DECIMAL(12, 2) NOT NULL
);

CREATE TABLE rental_agreements (
    agreement_id INT PRIMARY KEY,
    client_id INT NOT NULL,
    car_id INT NOT NULL,
    start_date DATE NOT NULL,
    expected_end_date DATE NOT NULL,
    actual_end_date DATE NULL,
    agreed_daily_rate DECIMAL(10, 2) NOT NULL,
    total_rental_cost DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
);
 -- Во 2 пункте была выбрана сущность clients
