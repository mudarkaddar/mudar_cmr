import psycopg2

db_name = 'cmr'       # Replace with your desired database name
db_user = 'postgres'   # Replace with your desired database username
db_password = '123'   # Replace with your desired database password
db_host = 'localhost'        # Replace with your database host if necessary
db_port = '5432'             # Replace with your database port if necessary


try:
    # Connect to the PostgreSQL server without a transaction
    connection = psycopg2.connect(
        database="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    
    connection.autocommit = True
    
    # Create a cursor object
    cursor = connection.cursor()
    
    # Create the database
    cursor.execute(f"CREATE DATABASE {db_name};")
    print(f"Database '{db_name}' created successfully.")
    
except (Exception, psycopg2.Error) as error:
    print(f"Error creating database: {error}")

finally:
    # Close the cursor and connection
     if 'connection' in locals():
            cursor.close()
            connection.close()