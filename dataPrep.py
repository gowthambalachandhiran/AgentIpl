# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:08:01 2024

@author: gowtham.balachan
"""

import sqlite3
import pandas as pd


def create_db(data):
    # Load the CSV file into a pandas DataFrame
    csv_file = data
    df = pd.read_csv(csv_file)
    
    # Create an SQLite database (or connect to an existing one)
    conn = sqlite3.connect('IPL.db')
    cursor = conn.cursor()
    
    # Define the name of the table you want to create
    table_name = "BallByBall"
    
    # Convert the DataFrame to SQL and create the table in the SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Commit and close the connection
    conn.commit()
    conn.close()
    
    print(f"Table '{table_name}' created successfully in 'my_database.db'")
        
def test_connection(db,table_name):
        # Reconnect to the SQLite database
    conn = sqlite3.connect(db)
    
    # Query the data
    df = pd.read_sql(f"SELECT Batter Runs FROM {table_name} limit 5", conn)
    
    # Show the data
    print(df)
    
    # Close the connection
    conn.close()


if __name__ == '__main__':
    create_db('ball_by_ball_ipl.csv')
    test_connection(db='IPL.db',table_name='BallByBall')