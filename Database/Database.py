import psycopg2


def insert_exhibitions(exhibition_list):
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price NUMERIC(10, 2),
            image JSONB,
            location VARCHAR(100)
        );
    """)

    # SQL statement to insert data into the table
    insert_query = """
            INSERT INTO products (url, name, description, price, images, location)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

    # Iterate over the list of exhibitions and insert them into the database
    for exhibition in exhibition_list:
        cur.execute(insert_query, (
            exhibition['url'],
            exhibition['name'],
            exhibition.get('description', None),
            exhibition.get('price', None),
            exhibition.get('image', None),
            exhibition.get('location', None)
        ))

    # Commit the transaction
    conn.commit()

    # Close cursor
    cur.close()
