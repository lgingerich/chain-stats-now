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
chains table schema:
    id: primary key
    chain_id: chain id, primarily applicable to EVM networks
    chain: chain name (e.g. ethereum, arbitrum_one, etc.)
    category: chain category (e.g. layer 1, rollup, sidechain)
    type: chain type (e.g. mainnet, zk rollup, optimistic rollup, validium, etc.)
    settlement_chain: the chain where a rollup settles to, if applicable (e.g. for Arbitrum -> Ethereum)
    tech_stack: tech stack upon which the chain is built (e.g. for Base -> OP Stack)
    purpose: chain purpose (e.g. universal, payments, gaming, etc.)
    native_currency: native chain currency (e.g. for Ethereum -> ETH)
    created_on: timestamp that the chain is started tracking
"""

def create_tables():
    command = """
    DROP TABLE IF EXISTS chains;
    CREATE TABLE chains (
        id SERIAL PRIMARY KEY,
        chain_id VARCHAR(64),
        chain VARCHAR(64) UNIQUE NOT NULL,
        category VARCHAR(64) NOT NULL,
        type VARCHAR(64) NOT NULL,
        settlement_chain VARCHAR(64),
        tech_stack VARCHAR(64),
        purpose VARCHAR(64) NOT NULL,
        native_currency VARCHAR(64) NOT NULL,
        created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
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
