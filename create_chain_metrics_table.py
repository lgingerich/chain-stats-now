import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

DB_NAME     = os.getenv('DB_NAME')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST     = os.getenv('DB_HOST')
DB_PORT     = os.getenv('DB_PORT')

"""
chain_metrics table schema:
    metric_id: primary key
    chain: chain name (e.g. ethereum, arbitrum_one, etc.)
    block_number: chain block number
    block_time: chain block timestamp
    transaction_count: number of transactions per block (successful and failed)
"""

def create_tables():
    command = """
    DROP TABLE IF EXISTS chain_metrics;
    CREATE TABLE chain_metrics (
        metric_id SERIAL PRIMARY KEY,
        chain VARCHAR(64) NOT NULL REFERENCES chains(chain),
        block_number BIGINT NOT NULL,
        block_time TIMESTAMP NOT NULL,
        transaction_count INT NOT NULL,
        UNIQUE(chain, block_number)  -- Ensures that for each chain, a block number is unique
    );
    """

    conn = None
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cur = conn.cursor()
        
        cur.execute(command)
        
        # Close the communication with the PostgreSQL
        cur.close()
        
        # Commit the changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()