import sqlite3

conn = sqlite3.connect('test.db')
#print ("Opened database successfully")

cursor = conn.cursor()

# Create the table 
create_table_query = """
CREATE TABLE IF NOT EXISTS practice_problems (
    sent BOOLEAN,
    question VARCHAR(100),
    resources VARCHAR(100)
);
"""

cursor.execute(create_table_query)
conn.commit()

# Close the connection
cursor.close()
conn.close()