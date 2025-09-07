CREATE TABLE IF NOT EXISTS booking_tickets (
    booking_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    start_location VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    trip_date DATE NOT NULL,
    seats VARCHAR(100) NOT NULL
);
