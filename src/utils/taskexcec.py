def taskInsert(task, volumen, connection, cursor, factor):
    """
    Insert a task into the task list.
    """
    stringquery = ""
    for x in range(volumen):
        
        stringquery += task(x, volumen)
       
        if x % factor == 0:
            print(f"Insertando datos ficticios en la tabla ... {x}/{volumen}")
            cursor.execute(stringquery)
            stringquery = ""
            connection.commit()