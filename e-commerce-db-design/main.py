import mysql.connector
from mysql.connector import Error
import random
import os
from dotenv import load_dotenv
from faker import Faker

fake = Faker()
load_dotenv()

HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_users(connection, num_rows):
    cursor = connection.cursor()
    generated_emails = set()
    
    for _ in range(num_rows):
        username = fake.user_name()
        email = fake.email()
        
        while email in generated_emails:
            email = fake.email()
        generated_emails.add(email)
        
        password_hash = fake.sha256()
        query = f"""
        INSERT INTO Users (Username, Email, PasswordHash)
        VALUES ('{username}', '{email}', '{password_hash}');
        """
        cursor.execute(query)
    
    connection.commit()
    print(f"Inserted {num_rows} rows into Users table")

def insert_user_profiles(connection, num_rows):
    cursor = connection.cursor()
    query = "SELECT UserID FROM Users"
    cursor.execute(query)
    user_ids = [row[0] for row in cursor.fetchall()]

    used_user_ids = set()
    for _ in range(num_rows):
        while True:
            user_id = random.choice(user_ids)
            if user_id not in used_user_ids:
                used_user_ids.add(user_id)
                break
        
        full_name = fake.name()
        address = fake.address().replace('\n', ', ')
        phone_number = fake.phone_number()
        if len(phone_number) > 20:
            phone_number = phone_number[:20]
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
        
        query = f"""
        INSERT INTO UserProfile (UserID, FullName, Address, PhoneNumber, DateOfBirth)
        VALUES ({user_id}, '{full_name}', '{address}', '{phone_number}', '{date_of_birth}');
        """
        cursor.execute(query)
    connection.commit()
    print(f"Inserted {num_rows} rows into UserProfile table")


def insert_products(connection, num_rows):
    cursor = connection.cursor()
    for _ in range(num_rows):
        product_name = fake.word() + " " + fake.word()
        description = fake.text(max_nb_chars=200)
        price = round(random.uniform(10.0, 1000.0), 2)
        stock = random.randint(1, 100)
        query = f"""
        INSERT INTO Products (ProductName, Description, Price, Stock)
        VALUES ('{product_name}', '{description}', {price}, {stock});
        """
        cursor.execute(query)
    connection.commit()
    print(f"Inserted {num_rows} rows into Products table")

def insert_orders(connection, num_rows):
    cursor = connection.cursor()
    query = "SELECT UserID FROM Users"
    cursor.execute(query)
    user_ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(num_rows):
        user_id = random.choice(user_ids)
        status = random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
        query = f"""
        INSERT INTO Orders (UserID, Status)
        VALUES ({user_id}, '{status}');
        """
        cursor.execute(query)
    connection.commit()
    print(f"Inserted {num_rows} rows into Orders table")

def insert_order_products(connection, num_rows):
    cursor = connection.cursor()

    cursor.execute("SELECT OrderID FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT ProductID FROM Products")
    product_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        order_id = random.choice(order_ids)
        num_products = random.randint(1, 5)
        chosen_product_ids = random.sample(product_ids, num_products)

        for product_id in chosen_product_ids:
            quantity = random.randint(1, 10)
            query = f"""
            INSERT INTO Order_Products (OrderID, ProductID, Quantity)
            VALUES ({order_id}, {product_id}, {quantity});
            """
            cursor.execute(query)

    connection.commit()
    print(f"Inserted {num_rows} rows into OrderProducts table")

def main():
    connection = create_connection()
    
    try:
        insert_users(connection, 500000)
        insert_user_profiles(connection, 500000)
        insert_products(connection, 100000)
        insert_orders(connection, 100000)
        insert_order_products(connection, 300000)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
