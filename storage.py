import sqlite3
import pandas as pd

# Define class for database storage
class DBStorage():
    # Initialize the class
    def __init__(self):
        self.con = sqlite3.connect('links.db')
        self.setup_tables()

    # Function to setup tables in the database
    def setup_tables(self):
        # Create a cursor object to interact with the database
        cur = self.con.cursor()
        # Define the SQL query to create a table named 'results' if it does not exist
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created DATETIME,
                relevance INTEGER,
                UNIQUE(query, link)
            );
            """
        # Execute the SQL query to create the table
        cur.execute(results_table)
        # Commit the changes to the database
        self.con.commit()
        # Close the cursor object
        cur.close()

    # Function to query results from the database
    def query_results(self, query):
        # Read SQL query results into a Pandas DataFrame
        df = pd.read_sql(f"select * from results where query='{query}' order by rank asc", self.con)
        # Return the DataFrame
        return df

    # Function to insert a row into the results table
    def insert_row(self, values):
        # Create a cursor object to interact with the database
        cur = self.con.cursor()
        try:
            # Execute the SQL query to insert values into the results table
            cur.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?, ?, ?, ?, ?, ?, ?)', values)
            # Commit the changes to the database
            self.con.commit()
            # Handle the case where there is an integrity error (e.g. duplicate entries)
        except sqlite3.IntegrityError:
            pass
        # Close cursor object
        cur.close()

    # Function to update the relevance of a result
    def update_relevance(self, query, link, relevance):
        # Create a cursor object to interact with the database
        cur = self.con.cursor()
        # Execute the SQL query to update the relevance value in the results table
        cur.execute('UPDATE results SET relevance=? WHERE query=? AND link=?', [relevance, query, link])
        # Commit the changes to the database
        self.con.commit()
        # Close the cursor object
        cur.close()
