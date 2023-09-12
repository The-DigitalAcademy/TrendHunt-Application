import psycopg2

# Database connection parameters
dbname = "postgres"
host = "localhost"
port = 5432
user = "postgres"
password = " " 

# Establish a connection to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()
    print("Connected to the PostgreSQL database")

    # Perform database operations here

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()
    print("Connection to the PostgreSQL database closed")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
