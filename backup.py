""" Module squeal: table and database manipulation functions.

The meanings of "table" and "database" are as described in db_io.py.
"""

# Write your Cartesian product function and all your other helper functions
# here.

def command_to_dict(command):
    """(str) -> dict

    Given command, that is in proper SQuEal syntax, return the result in a
    dictionary format, where the tokens are keys and the values are their
    respective 
    transformed into a dictionary. into a
    list)
    """
    
    list = command.split()
    result = {}

    for i in range(0, len(list), 2):
            value = list[i + 1].split(",")
            result[list[i]] = value

    return result
    
def get_argument(dict_command):
    """(dict) -> list

    Precondition: "where" must be a key in dict_command.
    """

    operator = "="

    if ">" in dict_command["where"][0]:
        operator = "="

    argument = dict_command["where"][0].split(operator)
    argument.append(operator)
        
    return argument
    
def select_table(table_name, database):
    """(str, database) -> column

    Given the name of a table, find the table in the database and return the
    table in proper format.

    >>> database = {'movies': {'m.title': ['Titanic', 'The Lord of the Rings:\
    The Return of the King', 'Toy Story 3'], 'm.year': ['1997', '2003', '2010'\
    ]}, 'oscars': {'o.category': ['Animated Feature Film', 'Directing',\
    'Directing', 'Best Picture']}}

    >>> select_table("movies", database)
    {'m.title': ['Titanic', 'The Lord of the Rings: The Return of the King',\
    'Toy Story 3'], 'm.year': ['1997', '2003', '2010']}

    >>> select_table("oscars", database)
    {'o.category': ['Animated Feature Film', 'Directing', 'Directing',\
    'Best Picture']}
    """
    return database[table_name]

def select_column(column_name, squeal_table):
    """(str, str, database) -> column
    """
    return squeal_table[column_name]

def table1 (squeal_table1, squeal_table2):
    table_holder = {}

    #All columns in the database have the same length, so the length of an
    #arbitrary column from any table in the database is sufficent
    
    table2_col_len = len(squeal_table2[list(squeal_table2)[0]])

    for column_name in squeal_table1:
        value = []
        for str in squeal_table1[column_name]:
            for i in range(len(squeal_table1[column_name])):
                value.append(str)
        table_holder[column_name] = value

    return table_holder

def table2 (squeal_table):
    """
    """
    table_holder = {}

    for column_name in squeal_table:
        
        value = []
        for i in range(len(squeal_table[column_name])):
            value.extend(squeal_table[column_name])

        table_holder[column_name] = value

    return table_holder

def cartesian_product(squeal_table1, squeal_table2):
    """(table, table) -> table

    Given squeal table 1 and sqqueal table 2, return squeal table 1 with the
    updated keys and values of squeal table 2.

    >>> database = {'movies': {'m.title': ['Titanic', 'The Lord of the Rings:\
    The Return of the King', 'Toy Story 3'], 'm.year': ['1997', '2003', '2010'\
    ]}, 'oscars': {'o.category': ['Animated Feature Film', 'Directing',\
    'Directing', 'Best Picture']}}

    >>> cartesian_product("movies", "oscars", database)
    
    """

    result = table1(squeal_table1, squeal_table2)

    #http://stackoverflow.com/questions/38987/how-can-i-merge-union-two-python
    #-dictionaries-in-a-single-expression
    result.update(table2(squeal_table2))

    return result

def filter_argument(squeal_table, dict_command):
    """
    """
    argument = get_argument(dict_command)

    operand1 = argument[0]
    operand2 = argument[1]

    if argument[-1] == "=":
        operator_equal(squeal_table)
        
    else:
        operator_greater(squeal_table)

def operator_equal(operand1, operand2, squeal_table):
    """
    """
    col1 = select_column(column_name, squeal_table)
    for i in range(len(squeal_table[operand1])):
            if operand2 in c_product:
                select_column(column_name, squeal_table)
                if c_product[operand2]:
                    operand1 = operand1
    
    
