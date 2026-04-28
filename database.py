import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    """Database connection handler for MySQL"""
    
    @staticmethod
    def get_connection():
        """Create and return a MySQL database connection"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute a single query (INSERT, UPDATE, DELETE)"""
        connection = Database.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            result = cursor.lastrowid
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            connection.rollback()
            return None
        finally:
            connection.close()
    
    @staticmethod
    def fetch_all(query, params=None):
        """Fetch all results from a SELECT query"""
        connection = Database.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            connection.close()
    
    @staticmethod
    def fetch_one(query, params=None):
        """Fetch a single result from a SELECT query"""
        connection = Database.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            connection.close()
    
    @staticmethod
    def init_database():
        """Initialize the database and create tables if they don't exist"""
        connection = Database.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Create cameras table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS cameras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                ip_address VARCHAR(15) NOT NULL UNIQUE,
                status ENUM('active', 'inactive') DEFAULT 'active',
                resolution VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Database initialized successfully")
            cursor.close()
            return True
        except Error as e:
            print(f"Error initializing database: {e}")
            return False
        finally:
            connection.close()
