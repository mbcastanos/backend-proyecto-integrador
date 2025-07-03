import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",

        password="tuclave",
        database="huellasdb",
    )
