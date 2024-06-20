import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

def create_table():
    """Create the exhibitions table if it does not exist."""
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS exhibitions (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                min_price TEXT,
                max_price TEXT,
                image TEXT,
                location VARCHAR(100)
            );
        """)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def insert_exhibition(exhibition):
    """Insert a single exhibition into the database."""
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        insert_query = """
            INSERT INTO exhibitions (url, title, description, min_price, max_price, image, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """
        cur.execute(insert_query, (
            exhibition['url'],
            exhibition['title'],
            exhibition.get('description', None),
            exhibition.get('min_price', None),
            exhibition.get('max_price', None),
            exhibition.get('image', None),
            exhibition.get('location', None)
        ))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def insert_exhibitions(exhibition_list):
    """Insert a list of exhibitions into the database."""
    for exhibition in exhibition_list:
        insert_exhibition(exhibition)

def main():
    print("Environment Variables:")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")

    # Create the table (if it doesn't exist)
    create_table()

    # Example list of exhibitions
    exhibitions = [
        {
            'url': 'https://www.southbankcentre.co.uk/whats-on/festivals-series/online-events',
            'title': 'Online events',
            'description': None,
            'min_price': 'Not listed',
            'max_price': '£10',
            'image': 'https://d33hx0a45ryfj1.cloudfront.net/transform/134be982-b2b9-4e71-b50a-6dbfe4489d04/sally-rooney?io=transform:fill,width:600,height:600',
            'location': None
        }
    ]

    # Insert exhibitions into the database
    insert_exhibitions(exhibitions)

if __name__ == "__main__":
    main()
