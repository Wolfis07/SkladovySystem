import pymssql
import json

def init_database():
    print("Načítám konfiguraci...")
    try:
        with open('config.json', 'r') as f:
            cfg = json.load(f)['database']
    except Exception as e:
        print(f"Chyba configu: {e}")
        return

    print(f"Připojuji se k serveru: {cfg['host']}...")
    
    try:
        # Připojení s autocommit (aby se změny projevily hned)
        conn = pymssql.connect(
            server=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database=cfg['database'],
            autocommit=True
        )
        cursor = conn.cursor()
        print("Připojeno! Vytvářím tabulky...")

        # SQL PŘÍKAZY PRO MSSQL (T-SQL syntaxe)
        commands = [
            # 1. Tabulka Users
            """
            IF OBJECT_ID('Users', 'U') IS NULL
            CREATE TABLE Users (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                Username VARCHAR(50) NOT NULL,
                Role VARCHAR(20) CHECK (Role IN ('Admin', 'Customer')), 
                IsActive BIT DEFAULT 1
            )
            """,
            # 2. Tabulka Categories
            """
            IF OBJECT_ID('Categories', 'U') IS NULL
            CREATE TABLE Categories (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                Name VARCHAR(100) NOT NULL
            )
            """,
            # 3. Tabulka Products
            """
            IF OBJECT_ID('Products', 'U') IS NULL
            CREATE TABLE Products (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Price FLOAT NOT NULL,
                StockQuantity INT NOT NULL,
                CategoryId INT,
                FOREIGN KEY (CategoryId) REFERENCES Categories(Id)
            )
            """,
            # 4. Tabulka Orders
            """
            IF OBJECT_ID('Orders', 'U') IS NULL
            CREATE TABLE Orders (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                UserId INT NOT NULL,
                OrderDate DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (UserId) REFERENCES Users(Id)
            )
            """,
            # 5. Tabulka OrderItems
            """
            IF OBJECT_ID('OrderItems', 'U') IS NULL
            CREATE TABLE OrderItems (
                OrderId INT NOT NULL,
                ProductId INT NOT NULL,
                Quantity INT NOT NULL,
                UnitPrice FLOAT NOT NULL,
                PRIMARY KEY (OrderId, ProductId),
                FOREIGN KEY (OrderId) REFERENCES Orders(Id),
                FOREIGN KEY (ProductId) REFERENCES Products(Id)
            )
            """,
            # 6. Pohledy (Views) - musíme nejdřív smazat, pokud existují
            "DROP VIEW IF EXISTS v_ProductDetails",
            """
            CREATE VIEW v_ProductDetails AS
            SELECT p.Id, p.Name, p.Price, p.StockQuantity, c.Name as CategoryName
            FROM Products p
            JOIN Categories c ON p.CategoryId = c.Id
            """,
            "DROP VIEW IF EXISTS v_OrderSummary",
            """
            CREATE VIEW v_OrderSummary AS
            SELECT o.Id as OrderId, u.Username, o.OrderDate, COUNT(oi.ProductId) as TotalItems, SUM(oi.Quantity * oi.UnitPrice) as TotalPrice
            FROM Orders o
            JOIN Users u ON o.UserId = u.Id
            JOIN OrderItems oi ON o.Id = oi.OrderId
            GROUP BY o.Id, u.Username, o.OrderDate
            """,
            # 7. Data (vložíme jen pokud jsou tabulky prázdné)
            "IF NOT EXISTS (SELECT * FROM Categories) INSERT INTO Categories (Name) VALUES ('Elektronika'), ('Obleceni')",
            "IF NOT EXISTS (SELECT * FROM Users) INSERT INTO Users (Username, Role) VALUES ('admin_sef', 'Admin'), ('pepa_zakaznik', 'Customer')",
            "IF NOT EXISTS (SELECT * FROM Products) INSERT INTO Products (Name, Price, StockQuantity, CategoryId) VALUES ('Herni PC', 25000.00, 5, 1), ('Mys', 500, 20, 1)"
        ]

        for sql in commands:
            cursor.execute(sql)
            print("SQL příkaz proveden OK.")

        print("\n=== HOTOVO! DATABÁZE JE PŘIPRAVENA ===")
        conn.close()

    except Exception as e:
        print(f"\n!!! CHYBA !!!\n{e}")

if __name__ == "__main__":
    init_database()