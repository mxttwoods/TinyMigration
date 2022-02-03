from glob import glob
from mysql.connector import connect

DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = 3306
MIGRATIONS_PATH = "migrations/*"
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
    return connect(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


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
