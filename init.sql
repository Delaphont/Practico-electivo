CREATE TABLE IF NOT EXISTS Amenazas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50),
    Medida ENUM('Richter', 'Metros', 'Km/h', 'Km^2'),
    Intensidad DECIMAL(10,2),
    Fecha DATE,
    CoordenadaNorte DECIMAL(9,6),
    CoordenadaEste DECIMAL(9,6)
);


INSERT INTO Amenazas (Nombre, Medida, Intensidad, Fecha, CoordenadaNorte, CoordenadaEste) VALUES
('Terremoto', 'Richter', 6.5, '2024-04-12', 34.0522, -118.2437),
('Tsunami', 'Metros', 15.0, '2024-03-10', 38.3220, 142.3690),
('Huracán', 'Km/h', 150.0, '2024-02-20', 25.0343, -77.3963),
('Incendio', 'Km^2', 45.0, '2024-01-15', 34.0522, -118.2437),
('Tornado', 'Km/h', 220.0, '2024-04-05', 37.7749, -122.4194);


