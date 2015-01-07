"""Module db_io: functions for I/O on tables and databases.

A table file has a .csv extension.

We define "table" to mean this:

    dict of {str: list of str}

Each key is a column name from the table and each value is the list of strings
in that column from top row to bottom row.

We define "database" to mean this:

    dict of {str: table}

Each key is the name of the .csv file without the extension.  Each value is
the corresponding table as defined above.
"""

import glob


def print_csv(table):
    """ (table) -> NoneType

    Print a representation of table in the same format as a table file.
    """

    columns = list(table.keys())
    print(','.join(columns))

    # All columns are the same length; figure out the number of rows.
    num_rows = len(table[columns[0]])

    # Print each row in the table.
    for i in range(num_rows):

        # Build a list of the values in row i.
        curr_row = []
        for column_name in columns:
            curr_row.append(table[column_name][i])

        print(','.join(curr_row))


# Write your read_table and read_database functions below.
# Use glob.glob('*.csv') to return a list of csv filenames from
#   the current directory.

def table_file_to_list(table_file):
    """ (file open for reading) -> list of str

    Return a list of a list of string, where each list of string contain the
    information of the given row from the table file.
    """

    list_table = []

    line = table_file.readline()
    while line != '':
        #Strip the newline character
        if "\n" in line:
            line = line.replace("\n", "")
        list_table.append(line)
        line = table_file.readline()

    for i in range(len(list_table)):
        list_table[i] = list_table[i].split(",")

    table_file.close()

    return list_table   

def read_table(table_file):
    """ (file open for reading) -> table

    Given table_file, return a table in the proper format (a dictionary where
    the key is a string and the value is a list of string).
    """

    list_table = table_file_to_list(table_file)
    
    table = {}
    
    for column_name in list_table[0]:
        table[column_name] = []
        column_index = list_table[0].index(column_name)
        for i in range(1, len(list_table)):
           table[column_name].append(list_table[i][column_index])    

    return table

def read_database():
    """() -> database

    Return a database (where the database is a dictionary, where the key is a
    string and the value is the table)of {str: table} of the specified directory.
    """

    list_of_files = glob.glob("*.csv")

    database = {}
    
    for file_name in list_of_files:
        table_file = open(file_name, "r")
        table_name = file_name.replace(".csv", "")
        database[table_name] = read_table(table_file)

    return database
