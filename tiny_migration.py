from mysql.connector import connect, Error, errorcode
from glob import glob

config = {
    "user": "root",
    "password": "",
    "host": "127.0.0.1",
    "database": "employees",
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
        return connect(**config)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def run_migration(script):
    print("Running migration: {}".format(script))
    connection = connect_to_db()
    with open(script) as f:
        sql = f.read()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()


# select all migrations that have been run from the database
# compare the list of migrations to the list of migrations in the manifest
# if the manifest has a migration that has not been run, run it and insert into the database
# if the manifest has a migration that has been run, skip it


def main():
    list_migrations()
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM migrations")
    migrations_run = [row[1] for row in cursor.fetchall()]
    for migration in MIGRATIONS_MANIFEST:
        if migration not in migrations_run:
            run_migration(migration)
            cursor.execute(
                "INSERT INTO migrations (migration) VALUES (%s)", (migration,)
            )
            connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
