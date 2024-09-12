# -*- coding: utf-8 -*-
import os
import mysql.connector
import pandas as pd
from mysql.connector import Error
from mysql.connector import errorcode
from dotenv import load_dotenv


load_dotenv()


def connect_database():
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_NAME')
    )

    return conn, conn.cursor()


def create_database(logger):
    try:
        conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS fx")

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error("Database does not exist")
        else:
            logger.error(err)
    else:
        if conn.is_connected():
            conn.close()


def create_symbol_table(logger, table_name):
    try:
        conn, cursor = connect_database()

        cursor.execute("USE fx")

        # Create table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timeframe VARCHAR(255),
                time DATETIME,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                tick_volume INT,
                spread INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_timeframe_time (timeframe, time)
            )
        ''')
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error("Database does not exist")
        else:
            logger.error(err)
    else:
        if conn.is_connected():
            conn.close()


def upsert_data(df, logger, table_name, timeframe):
    conn, cursor = connect_database()

    cursor.execute("USE fx")

    try:
        for _, row in df.iterrows():
            query = f"""
            INSERT INTO {table_name} 
            (timeframe, time, open, high, low, close, tick_volume, spread)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            high = VALUES(high),
            low = VALUES(low),
            close = VALUES(close),
            tick_volume = VALUES(tick_volume),
            spread = VALUES(spread)
            """
            values = (
                timeframe,
                row['time'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['tick_volume'],
                row['spread']
            )
            cursor.execute(query, values)
        
        conn.commit()
        print(f"{len(df)} rows upserted successfully.")
    except Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def fetch_data(timeframe, start_date, end_date):
    conn, cursor = connect_database()

    cursor.execute("USE fx")

    try:
        query = """
        SELECT time, open, high, low, close
        FROM usdjpy
        WHERE timeframe = %s AND time BETWEEN %s AND %s
        ORDER BY time
        """
        cursor.execute(query, (timeframe, start_date, end_date))
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close'])
        df['time'] = pd.to_datetime(df['time'])
        return df
    finally:
        cursor.close()
        conn.close()