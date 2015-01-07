""" Module squeal: table and database manipulation functions.

The meanings of "table" and "database" are as described in db_io.py.
"""
def get_query(user_input):
    """(str) -> dict

    Given command that is in proper SQuEal syntax, return the result in a
    dictionary format, where the tokens are keys and their respective values
    are transformed into a list.

    >>> user_input = "select * from movies where k=l"
    >>> q = get_query(user_input)
    >>> q == {"select": ["*"], "from": ["movies"], "where": ["k=l"]}
    True

    >>> user_input = "select m.title,k.title from oscars,leolost where k=1"
    >>> q = get_query(user_input)
    >>> q == {'where': ['k=1'], 'from': ['oscars', 'leolost'], 'select': ['m.title', 'k.title']}
    True
    """
    
    list = user_input.split()
    query = {}

    for i in range(0, len(list), 2):
            value = list[i + 1].split(",")
            query[list[i]] = value

    return query

def join_tables(database, query):
    """(table, database, list) -> table

    Return the product of joined tables listed in the given query and found
    from the given database.

    >>> db = {1 : {"A": [1, 2, 3]}, 2: {"B": [4, 5, 6, 7]}, 3: {"C": ["Sherlock is dead"]}}

    >>> query = {"from": [1, 1]}
    >>> result = join_tables(db, query)
    >>> result == {'A': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], 'B': [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7]}
    True
    
    >>> query = {"from": ["*"]}
    >>> result = join_tables(db, query)
    >>> result == {'A': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], 'B': [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7], 'C': ['Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead']}
    True
    """

    table_names = query["from"]

    if "*" in table_names:
        table_names = list(database)

    result_table = database[table_names[0]]
            
    
    for table in table_names[1:]:
        other_table = database[table]
        result_table = cartesian_product(result_table, other_table)

    return result_table

#Helper functions for join_tables

def cartesian_product(squeal_table1, squeal_table2):
    """(table, table) -> table

    Given squeal table 1 and sqqueal table 2, return result table with the
    updated values of the two given squeal_tables.

    >>> squeal_table1 = {"A": [1, 2, 3]}
    >>> squeal_table2 = {"B": [4, 5, 6, 7]}
    >>> result = cartesian_product(squeal_table1, squeal_table2)
    >>> result == {'A': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], 'B': [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7]}
    True

    >>> squeal_table1 = {"C": ["Sherlock is dead"]}
    >>> squeal_table2 = {"B": [4, 5, 6, 7]}
    >>> result = cartesian_product(squeal_table1, squeal_table2)
    >>> result == {'B': [4, 5, 6, 7], 'C': ['Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead', 'Sherlock is dead']}
    True
    """

    result_table = {}
    
    #All columns in the database have the same length, so the length of an
    #arbitrary column from any table in the database is sufficent
    t1_col_len = len(squeal_table1[list(squeal_table1)[0]])
    t2_col_len = len(squeal_table2[list(squeal_table2)[0]])
    
    for column_name in squeal_table1:
        values = []
        for value in squeal_table1[column_name]:
            for i in range(t2_col_len):
                values.append(value)
        result_table[column_name] = values 
    
    for column_name in squeal_table2:
        values = []
        for i in range(t1_col_len):
            values.extend(squeal_table2[column_name])
        result_table[column_name] = values

    return result_table

def filter_rows(squeal_table, query):
    """(table, dict) -> table

    Return a table with the row from the given squeal_table that match the
    argument in the given query.

    >>> squeal_table = {"A":["1", "2", "3"], "B":["1", "4", "5"]}

    >>> query = {"where": ["A=B", "A='1'"]}
    >>> result = filter_rows(squeal_table, query)
    >>> result == {'B': ["1"], 'A': ["1"]}
    True

    >>> query = {"where": ["A='2'"]}
    >>> result = filter_rows(squeal_table, query)
    >>> result == {'B': ['4'], 'A': ['2']}
    True
    """

    result_table = filter_row(squeal_table, query, 0)

    if len(query["where"]) == 1:
        return result_table

    for i in range(1, len(query["where"])):
        temp_table = copy(result_table)
        result_table = filter_row(temp_table, query, i)

    return result_table
        
    
def filter_row(squeal_table, query, index):
    """(table, dict) -> table

    Return a table with the row from the given squeal_table that match the
    argument of the query at the given index.

    >>> squeal_table = {"A":["1", "2", "3"], "B":["1", "4", "5"]}

    >>> query = {"where": ["A=B"]}
    >>> result = filter_row(squeal_table, query, 0)
    >>> result == {'B': ["1"], 'A': ["1"]}
    True

    >>> query = {"where": ["A='2'", "A='1'"]}
    >>> result = filter_row(squeal_table, query, 1)
    >>> result == {'A': ['1'], 'B': ['1']}
    True
    """
   
    operands = get_argument(query, index)

    operand2 = operands[2]
    operator = operands[1]

    result_table = {}

    for i in range(len(squeal_table[operands[0]])):
        temp_table = copy(result_table)
            
        operand1 = squeal_table[operands[0]][i]
        if operands[2] in squeal_table:
            operand2 = squeal_table[operands[2]][i]

        if operator == "=":
            condition = operand1 == operand2
        else:
            condition = operand1 > operand2

        if condition:
            append_row(result_table, squeal_table, i)

    return result_table

#Helper functions for filter_rows

def copy(squeal_table):
    """(table) -> table

    Return a deep copy of the given squeal table.

    >>> squeal_table = {1: 2, 3: 4}
    >>> copy(squeal_table)
    {1: 2, 3: 4}

    >>> squeal_table = {1: 2, 3: 4}
    >>> copy(squeal_table)
    {1: 2, 3: 4}
    """
    
    result_table = {}

    for col_name in squeal_table:
        tuple_value = tuple(squeal_table[col_name])
        list_value = []

        for item in tuple_value:
            list_value.append(item)

        if col_name in result_table:
            result_table[col_name].extend(list_value)
        else:
            result_table[col_name] = list_value

    return result_table

def get_argument(query, index):
    """(dict, int) -> tuple

    Given a query and an index, find and return the argument at that index.

    >>> query = {"where": ["what=kill"]}
    >>> get_argument(query)
    ("what", "=", "kill")

    >>>query = {"where": ["what>'no'"]}
    >>> get_argument(query)
    ("what", ">", "'no'")
    """
    
    operator = "="
    if ">" in query["where"][index]:
        operator = ">"

    str_argument = query["where"][index].replace("'", "")

    return str_argument.partition(operator)

def append_row(result_table, squeal_table, index):
    """(table, table, int) -> NoneType

    Append the rows of the given index in the given squeal table to the result
    table.

    >>> squeal_table = {"A": ["a", "b", "c"], "B": ["1", "2", "3"]}
    >>> result_table = {}
    >>> index = 1
    >>> append_rows(result_table, squeal_table, index)
    >>> result = result_table
    >>> result == {'B': ['2'], 'A': ['b']}
    True

    >>> squeal_table = {"A": ["a", "b", "c"], "B": ["1", "2", "3"]}
    >>> result_table = {'B': ['2'], 'A': ['b']}
    >>> index = 0
    >>> append_rows(result_table, squeal_table, index)
    >>> result = result_tablresult == {'B': ['2', '1'], 'A': ['b', 'a']}
    True
    """

    for col_name in squeal_table:
        if not (col_name in result_table):
            result_table[col_name] = [squeal_table[col_name][index]]
        else:
            result_table[col_name].append(squeal_table[col_name][index])

def filter_columns(squeal_table, query):
    """(table, dict) -> table

    Return a table with the keys and values from the given squeal_table, where
    the key matches the specifed keys given by the query.

    >>> squeal_table = {"A": ["all your favourite characters are dead"], "B": ["Sherlock season 3 will never come"], "C": ["This could be the last doctor"], "D": ["Eleven is going to die"]}
    >>> query = {"select": [*]}
    >>> result = filter_columns(squeal_table, query)
    >>> result == {"A": ["all your favourite characters are dead"], "B": ["Sherlock season 3 will never come"], "C": ["This could be the last doctor"], "D": ["Eleven is going to die"]}

    >>> squeal_table = {"A": ["all your favourite characters are dead"], "B": ["Sherlock season 3 will never come"], "C": ["This could be the last doctor"], "D": ["Eleven is going to die"]}
    >>> query = {"select": ["A", "C"]}
    >>> result = filter_columns(squeal_table, query)
    >>> result == {'C': ['This could be the last doctor'], 'A': ['all your favourite characters are dead']}
    """
    
    column_names = query["select"]

    #Only need soft copy since the values will not be changed, just the keys
    #Method obtained from: http://stackoverflow.com/questions/8771808/copy-a-dictionary-into-a-new-variable-without-maintaining-the-link-with-previous
    
    result_table = squeal_table.copy()

    if "*" in column_names:
        return result_table
    
    for column in squeal_table:
        if column not in column_names:
            del result_table[column]

    return result_table
