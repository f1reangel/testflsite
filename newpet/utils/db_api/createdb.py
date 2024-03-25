import psycopg2


def create_reservations_table():
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="88461978"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the CREATE TABLE statement
        create_table_query = """
        CREATE TABLE reservations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            reservation_date VARCHAR(20) NOT NULL,
            reservation_time VARCHAR(20) NOT NULL,
            guests_count VARCHAR(20) NOT NULL,
            table_number INT NOT NULL,
            news_subscription BOOLEAN NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print("Table 'reservations' created successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error creating table:", error)

if __name__ == "__main__":
    create_reservations_table()
