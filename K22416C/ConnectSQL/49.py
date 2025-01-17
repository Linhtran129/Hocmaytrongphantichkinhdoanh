import sqlite3
import pandas as pd


def get_customers_with_invoices(db_path, min_invoices):
    try:
        # Connect to SQLite database
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print('Database connection initialized.')

        # Query to fetch customers with at least N invoices
        query = f'''
        SELECT C.CustomerId, C.FirstName, C.LastName, COUNT(I.InvoiceId) AS InvoiceCount
        FROM Customer C
        JOIN Invoice I ON C.CustomerId = I.CustomerId
        GROUP BY C.CustomerId, C.FirstName, C.LastName
        HAVING COUNT(I.InvoiceId) >= {min_invoices};
        '''

        # Execute query
        cursor.execute(query)

        # Fetch results and convert to DataFrame
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['CustomerId', 'FirstName', 'LastName', 'InvoiceCount'])

        # Close the cursor
        cursor.close()

        return df

    except sqlite3.Error as error:
        print('Error occurred -', error)
        return None

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite connection closed.')


# Example usage
db_path = 'C:/Users/admin/PycharmProjects/K22416C/Dataset/database/Chinook_Sqlite.sqlite'
min_invoices = 5
customer_df = get_customers_with_invoices(db_path, min_invoices)

if customer_df is not None:
    print(customer_df)
