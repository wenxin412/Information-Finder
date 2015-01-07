"""
Process SQuEaL queries from the keyboard and print the results.
"""

import db_io
import squeal


def main():
    """ () -> NoneType

    Ask for queries from the keyboard; stop when empty line is received. For
    each query, process it and use db_io.print_csv to print the results.
    """
    
    database = db_io.read_database()
    
    user_input = input("Please enter query: ")

    while user_input != "":
        query = squeal.get_query(user_input)

        result_table = squeal.join_tables(database, query)

        if "where" in query:
            result_table = squeal.filter_rows(result_table, query)
            
        result_table = squeal.filter_columns(result_table, query)

        db_io.print_csv(result_table)

        user_input = input("Please enter query: ")


if __name__ == '__main__':
    main()
