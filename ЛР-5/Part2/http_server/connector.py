import contextlib
import sqlite3


@contextlib.contextmanager
def db_connector(con: sqlite3.Connection) -> sqlite3.Connection:
    """
    Context manager for database connection.

    Args:
        con: sqlite3.Connection - Connection to SQLite database.

    Yields:
        sqlite3.Connection - Connection to SQLite database.

    Notes:
        Creates 'logtable' table if it does not exist.
        Commits changes after leaving the context.
    """
    con.execute('''CREATE TABLE IF NOT EXISTS logtable (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        datetime TEXT,
                                        func_name TEXT,
                                        params TEXT,
                                        result TEXT
                                    )''')
    try:
        yield con
    finally:
        con.commit()
        con.close()
