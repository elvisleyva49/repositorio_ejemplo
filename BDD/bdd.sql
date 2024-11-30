-- Crear la base de datos
CREATE DATABASE CasaDeCambioDB;
GO

USE CasaDeCambioDB;
GO

-- Crear tabla de Usuarios
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedDate DATETIME DEFAULT GETDATE()
);
GO

-- Crear tabla de Cuentas
CREATE TABLE Accounts (
    AccountId INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    BalanceUSD DECIMAL(18,2) DEFAULT 0.00,
    BalanceEUR DECIMAL(18,2) DEFAULT 0.00,
    BalancePEN DECIMAL(18,2) DEFAULT 0.00,
    LastUpdated DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
);
GO

-- Crear tabla de Transacciones
CREATE TABLE Transactions (
    TransactionId INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    FromCurrency VARCHAR(3) NOT NULL,
    ToCurrency VARCHAR(3) NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Rate DECIMAL(18,4) NOT NULL,
    Result DECIMAL(18,2) NOT NULL,
    TransactionDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
);
GO

-- Insertar algunos datos de prueba
INSERT INTO Users (Username, PasswordHash) VALUES 
('admin', 'admin123'),
('usuario1', 'pass123');
GO

-- Insertar saldos iniciales para los usuarios
INSERT INTO Accounts (UserId, BalanceUSD, BalanceEUR, BalancePEN) VALUES 
(1, 1000.00, 1000.00, 1000.00),
(2, 500.00, 500.00, 500.00);
GO