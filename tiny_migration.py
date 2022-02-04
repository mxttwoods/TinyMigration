from glob import glob
from configparser import ConfigParser
from os import path
from mysql.connector import connect, Error, errorcode
from pprint import pprint

parser = ConfigParser()
parser.read("config.ini")
CONFIG = {
    "user": parser.get("database", "user"),
    "password": parser.get("database", "password"),
    "host": parser.get("database", "host"),
    "database": parser.get("database", "dbname"),
    "raise_on_warnings": True,
}
MIGRATIONS_PATH = "migrations/[0-9]**.sql"
MIGRATIONS_MANIFEST = []
MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS migrations (
    id INT NOT NULL AUTO_INCREMENT,
    migration VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
"""


def list_migrations():
    for file in glob(MIGRATIONS_PATH):
        MIGRATIONS_MANIFEST.append(file)


def connect_to_db():
    try:
        return connect(**CONFIG)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def run_migration(script):
    base_name = path.basename(script)
    print(f"Running migration: {base_name}")
    with open(script) as f:
        sql = f.read()
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
    print(f"Migration {base_name} completed")


def main():
    print("Running migrations...")
    list_migrations()
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT migration FROM migrations")
    existing_migrations = cursor.fetchall()
    pprint(existing_migrations)
    for migration in MIGRATIONS_MANIFEST:
        base_name = path.basename(migration)
        if migration not in existing_migrations:
            run_migration(migration)
            cursor.execute(
                "INSERT INTO migrations (migration) VALUES (%s)", (migration,)
            )
            connection.commit()
            print(f"Migration {base_name} added to database")
        else:
            print(f"Migration {base_name} already exists in database")
    connection.close()


if __name__ == "__main__":
    main()
