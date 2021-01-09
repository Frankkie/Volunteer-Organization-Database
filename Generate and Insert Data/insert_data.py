import pymysql as sql
import csv


def connect():
    host_ = '150.140.186.221'
    user_ = 'db20_up1053706'
    psw_ = 'up1053706'
    db_ = 'project_db20_up1053706'
    conn = sql.connect(host=host_, user=user_, password=psw_, db=db_)
    return conn


def read_csv(source):

    content = []
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are: {", ".join(row)}')
                line_count += 1
            else:
                for index, elem in enumerate(row):
                    if elem == 'None' or elem == 'Null':
                        row[index] = None
                    try:
                        elem = int(elem)
                        row[index] = elem
                    except ValueError:
                        pass
                # print(row)
                content.append(row)
                line_count += 1

        print(f'Processed {line_count} lines.')
        return content


def add_departments(connection, cursor, delete_prev=True):

    if delete_prev:
        cursor.execute("DELETE FROM `University Department`;")

    departments = ['Department of Architecture',
                   'Department of Chemical Engineering',
                   'Department of Civil Engineering',
                   'Department of Computer Engineering and Informatics',
                   'Department of Electrical Engineering and Computer Technology',
                   'Department of Environmental Engineering',
                   'Department of Mechanical Engineering and Aeronautics',
                   'Department of Medicine',
                   'Department of Pharmacy']

    count = 0
    query = """
        INSERT INTO `University Department` (`Department Name`)
        VALUES (%s);
        """
    for dep in departments:
        try:
            cursor.execute(query, (dep))
            count += 1
        except sql.err.IntegrityError:
            pass

    connection.commit()

    print("Committed " + str(count) + " rows!")
    cursor.execute("SELECT * FROM `University Department`;")

    for c in cursor:
        print(list(c))

    return


def add_fields(connection, cursor, source, delete_prev=True):

    if delete_prev:
        cursor.execute("DELETE FROM `Field`;")

    fields = read_csv(source)

    count = 0
    query = """
        INSERT INTO `Field` (`Field Id`, `Field Name`)
        VALUES (%s, %s);
        """
    for dep in fields:
        try:
            cursor.execute(query, (dep))
            count += 1
        except sql.err.IntegrityError:
            pass

    connection.commit()

    print("Committed " + str(count) + " rows!")
    cursor.execute("SELECT * FROM `Field`;")

    for c in cursor:
        print(list(c))

    return


def add_teams(connection, cursor, source, delete_prev=True):

    if delete_prev:
        cursor.execute("DELETE FROM `Team`;")

    teams = read_csv(source)
    count = 0

    query = """
    INSERT INTO `Team` (`Team Id`, `Team Name`, `Team Type`, `IEEE Code`, `Field`)
    VALUES (%s, %s, %s, %s, %s);
    """

    for elem in teams:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass

    connection.commit()

    print("Committed " + str(count) + " rows!")
    cursor.execute("SELECT `Team Name` FROM `Team` WHERE `IEEE Code` IS NULL;")

    for c in cursor:
        print(list(c))

    return


def add_projects(connection, cursor, source, delete_prev=True):
    if delete_prev:
        cursor.execute("DELETE FROM `Project`;")
    projects = read_csv(source)
    count = 0
    query = """
    INSERT INTO `Project` (`Project Title`, `Start Date`, `End Date`)
    VALUES (%s, %s, %s);
    """
    for elem in projects:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()
    print("Committed " + str(count) + " rows!")
    cursor.execute("SELECT * FROM `Project`")
    for c in cursor:
        print(list(c))
    return


def add_member(connection, cursor, source, delete_prev=True):
    if delete_prev:
        cursor.execute("DELETE FROM `Member`;")
    rows = read_csv(source)
    count = 0
    query = """
    INSERT INTO `Member` (`Id`, `First Name`, `Last Name`, `Email`, `Phone`, `IEEE Number`, `Activity Status`,
                          `Training Date`, `Generation`, `Registration Date`, `Deletion Date`, `Studies at`, 
                          `Univ Grade`, `Reg Year to Univ`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()
    print("Committed " + str(count) + " rows!")

    return


def add_participants(connection, cursor, source, delete_prev=True):
    if delete_prev:
        cursor.execute("DELETE FROM `Participant`;")
    rows = read_csv(source)
    count = 0
    query = """
    INSERT INTO `Participant` (`Email`, `First Name`, `Last Name`, `Subscribed`, `Interested in Membership`)
    VALUES (%s, %s, %s, %s, %s);
    """
    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()
    print("Committed " + str(count) + " rows!")

    return


def add_teams_to_members(connection, cursor, source, delete_prev=True):

    if delete_prev:
        cursor.execute("DELETE FROM `Participates In`;")
        cursor.execute("DELETE FROM `Heads`;")
        cursor.execute("DELETE FROM `Supervises`;")
    parts = read_csv(source[0])
    heads = read_csv(source[1])
    superv = read_csv(source[2])

    count = 0
    query_parts = """
    INSERT INTO `Participates In` (`Member Id`, `Team Id`, `Title`, `Start Date`, `End Date`)
    VALUES (%s, %s, %s, %s, %s);
    """
    query_heads = """
        INSERT INTO `Heads` (`Member Id`, `Team Id`, `Title`, `Start Date`, `End Date`)
        VALUES (%s, %s, %s, %s, %s);
        """
    query_superv = """
        INSERT INTO `Supervises` (`Member Id`, `Team Id`, `Title`, `Start Date`, `End Date`)
        VALUES (%s, %s, %s, %s, %s);
        """

    for elem in heads:
        try:
            cursor.execute(query_heads, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass

    for elem in parts:
        try:
            cursor.execute(query_parts, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass

    for elem in superv:
        try:
            cursor.execute(query_superv, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()
    print("Committed " + str(count) + " rows!")

    return


def add_events(connection, cursor, source, delete_prev=True):

    if delete_prev:
        cursor.execute("DELETE FROM `Event`;")

    rows = read_csv(source)
    count = 0

    query = """
    INSERT INTO `Event` (`Event Title`, `Event Date`, `Organized By`, `Event Type`, `Place`)
    VALUES (%s, %s, %s, %s, %s);
    """

    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass

    connection.commit()


def add_attends(connection, cursor, source, delete_prev=True):
    if delete_prev:
        cursor.execute("DELETE FROM `Attends`;")
    rows = read_csv(source)
    count = 0
    query = """
    INSERT INTO `Attends` (`Participant Email`, `Event Title`, `Event Date`)
    VALUES (%s, %s, %s);
    """
    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()


def add_workson(connection, cursor, source, delete_prev=True):
    if delete_prev:
        cursor.execute("DELETE FROM `Works on`;")
    rows = read_csv(source)
    count = 0
    query = """
    INSERT INTO `Works on` (`Team Id`, `Project Id`)
    VALUES (%s, %s);
    """
    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()


def add_the_rest(connection, cursor, source, choice, delete_prev=True):
    query = ""
    if delete_prev:
        if choice == "Contact":
            cursor.execute("DELETE FROM `Contact`;")
            query = """
                INSERT INTO `Contact` (`Contact Id`, `Contact Email`, `Phone`, `First Name`, `Last Name`, `Address`,
                `Date Created`, `IEEE Position`, `Field`, `Uni Department`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        if choice == "Contribution":
            cursor.execute("DELETE FROM `Contribution`;")
            query = """
                       INSERT INTO `Contribution` (`Contribution Id`, `Given By`, `Date`, 
                       `Type`, `Package`, `Stored In`)
                       VALUES (%s, %s, %s, %s, %s, %s);
                            """
        if choice == "Purchase":
            cursor.execute("DELETE FROM `Purchase`;")
            query = """
                            INSERT INTO `Purchase` (`Purchase Id`, `Purchased by`, `Date`,
                            `Type`, `Cost`, `Stored In`)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """
        if choice == "Has Contact":
            cursor.execute("DELETE FROM `Has Contact`;")
            query = """
                            INSERT INTO `Has Contact` (`Team Id`, `Contact Id`)
                            VALUES (%s, %s);
                            """
        if choice == "Contributes to Event":
            cursor.execute("DELETE FROM `Contributes to Event`;")
            query = """
                            INSERT INTO `Contributes to Event` (`Event Title`, `Event Date`, `Contact Id`)
                            VALUES (%s, %s, %s);
                            """

    rows = read_csv(source)
    count = 0

    for elem in rows:
        try:
            cursor.execute(query, tuple(elem))
            count += 1
        except sql.err.IntegrityError:
            pass
    connection.commit()


if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()
    add_the_rest(conn, cur, "purchases.csv", "Purchase")
    add_the_rest(conn, cur, "contributions.csv", "Contribution")
    cur.close()
    conn.close()
