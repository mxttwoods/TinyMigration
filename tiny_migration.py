from glob import glob
from configparser import ConfigParser
from os import path
from mysql.connector import connect, Error, errorcode

__author__ = "Matthew Woods"
__email__ = "Matthew Woods <mxttwoods@gmail.com>"
__version__ = "0.1.0-alpha"

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
MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS migrations (
    id INT NOT NULL AUTO_INCREMENT,
    migration VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
"""
MIGRATIONS_SELECT = """
SELECT migration FROM migrations;
"""
MIGRATIONS_INSERT = """
INSERT INTO migrations (migration) VALUES (%s);
"""


def connect_to_db():
    try:
        return connect(**CONFIG)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password", "\n", err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist", "\n", err)
        else:
            print(err)


def run_migration(base_name, script):
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
    manifest = []
    print("Running migrations...")
    for file in glob(MIGRATIONS_PATH):
        print(f"Found migration: {file}")
        manifest.append(file)
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(MIGRATIONS_TABLE)
    cursor.execute(MIGRATIONS_SELECT)
    existing_migrations = cursor.fetchall()
    print("Existing migrations: ", "\n", existing_migrations)
    for migration in manifest:
        base_name = path.basename(migration)
        if migration not in existing_migrations:
            run_migration(base_name, migration)
            cursor.execute(MIGRATIONS_INSERT, (migration,))
            connection.commit()
            print(f"Migration {base_name} added to database")
        else:
            print(f"Migration {base_name} already exists in database")
    connection.close()


if __name__ == "__main__":
    main()
