import mysql.connector
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import os
import time

# Load environment variables
load_dotenv()

# Connection settings
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def reset_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE accounts SET balance = 1000 WHERE name = 'Alice'")
            cursor.execute("UPDATE accounts SET balance = 1500 WHERE name = 'Bob'")
            connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

def isolation_demo(isolation_level):
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level=isolation_level)
        cursor1.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")

        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level=isolation_level)
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance = cursor2.fetchone()[0]

        print(f"{isolation_level} Read: Alice's balance = {balance}")

        print(f"Transaction 1 rollback(): {datetime.now()}")
        connection1.rollback()

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def repeatable_read_demo():
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='REPEATABLE READ')
        
        # First read
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        initial_balance = cursor1.fetchone()[0]
        print(f"Transaction 1 initial read: Alice's balance = {initial_balance}")

        time.sleep(1)

        # Transaction 2: Update
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='REPEATABLE READ')
        cursor2.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")
        connection2.commit()

        # Re-read
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        updated_balance = cursor1.fetchone()[0]
        print(f"Transaction 1 re-read: Alice's balance = {updated_balance}")

        connection1.rollback()
        connection2.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def non_repeatable_read_demo():
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        
        # First read
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        initial_balance = cursor1.fetchone()[0]
        print(f"Transaction 1 initial read: Alice's balance = {initial_balance}")

        # Transaction 2: Update
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")
        connection2.commit()

        # Re-read
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        updated_balance = cursor1.fetchone()[0]
        print(f"Transaction 1 re-read: Alice's balance = {updated_balance}")

        connection1.rollback()
        connection2.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def deadlock_demo():
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1 locks first row
        connection1.start_transaction(isolation_level='SERIALIZABLE')
        cursor1.execute("SELECT * FROM accounts WHERE id = 1 FOR UPDATE")

        # Transaction 2 locks second row
        connection2.start_transaction(isolation_level='SERIALIZABLE')
        cursor2.execute("SELECT * FROM accounts WHERE id = 2 FOR UPDATE")

        cursor1.execute("SELECT * FROM accounts WHERE id = 2 FOR UPDATE")
        cursor2.execute("SELECT * FROM accounts WHERE id = 1 FOR UPDATE")

        connection1.commit()
        connection2.commit()
    except Error as e:
        print(f"Deadlock detected: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

if __name__ == "__main__":
    reset_data()
    print("READ UNCOMMITTED demo:")
    isolation_demo('READ UNCOMMITTED')

    reset_data()
    print("\n\nREAD COMMITTED demo:")
    isolation_demo('READ COMMITTED')

    reset_data()
    print("\n\nNON-REPEATABLE READ demo:")
    non_repeatable_read_demo()

    reset_data()
    print("\n\nREPEATABLE READ demo:")
    repeatable_read_demo()

    reset_data()
    print("\n\nDeadlock demo:")
    deadlock_demo()
