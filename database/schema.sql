CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(10) NOT NULL CHECK (role IN ('driver','manager'))
);

CREATE TABLE vehicles (
    id          SERIAL PRIMARY KEY,
    plate       VARCHAR(15) UNIQUE NOT NULL,
    token_hash  VARCHAR(255) NOT NULL,
    driver_id   INTEGER UNIQUE REFERENCES users(id)
);

CREATE TABLE positions (
    id          BIGSERIAL PRIMARY KEY,
    vehicle_id  INTEGER NOT NULL REFERENCES vehicles(id),
    lat         DOUBLE PRECISION NOT NULL,
    lon         DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    received_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pos_vehicle_time ON positions(vehicle_id, recorded_at DESC);
