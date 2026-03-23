## Database Diagram in MySQL Workbench
<img width="492" height="363" alt="Model_MySQL_Workbench" src="https://github.com/user-attachments/assets/dbf9e622-3123-4d5c-bb0a-fdab72d29ee2" />

## Database in PostgreSQL
CREATE TABLE locations (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE measurements (
    id SERIAL PRIMARY KEY,
    location_id INT NOT NULL,
    sensor_id INT NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,

    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

---

## AI Usage

This project was developed with the help of AI tools.

Used ChatGPT for:
- understanding project requirements;
- explaining some parts of Python code and making changes to the code;
- debugging issues.

All code was reviewed and adapted manually.

Database design myself.
