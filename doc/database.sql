-- Vytvoření tabulek
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Price FLOAT NOT NULL,
    Stock INT NOT NULL,
    CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
    IsActive BIT DEFAULT 1 -- Logická hodnota (Bool)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FullName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    RegistrationDate DATETIME DEFAULT GETDATE() -- Datum a čas
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    OrderDate DATETIME DEFAULT GETDATE(),
    Status VARCHAR(20) CHECK (Status IN ('Pending', 'Paid', 'Shipped', 'Cancelled')) -- Enum přes Check Constraint
);

CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT NOT NULL,
    UnitPrice FLOAT NOT NULL
);

-- Vložení testovacích dat
INSERT INTO Categories (Name) VALUES ('Electronics'), ('Clothing'), ('Home');

INSERT INTO Products (Name, Price, Stock, CategoryID) VALUES 
('Super Monitor', 5000, 10, 1),
('Draha Klavesnice', 2000, 5, 1),
('Levne Triko', 150, 100, 2),
('Zimni Bunda', 3000, 20, 2);

INSERT INTO Customers (FullName, Email) VALUES 
('Jan Novak', 'jan@novak.cz'),
('Petr Svoboda', 'petr@svoboda.cz');

-- Vytvoření pohledů (Views)
GO
CREATE VIEW View_ProductSummary AS
SELECT p.Name AS ProductName, c.Name AS CategoryName, p.Price, p.Stock
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID;
GO

CREATE VIEW View_OrderDetails AS
SELECT o.OrderID, cu.FullName, o.OrderDate, o.Status, SUM(oi.Quantity * oi.UnitPrice) AS TotalPrice
FROM Orders o
JOIN Customers cu ON o.CustomerID = cu.CustomerID
JOIN OrderItems oi ON o.OrderID = oi.OrderID
GROUP BY o.OrderID, cu.FullName, o.OrderDate, o.Status;
GO
