"""database.py - Manage table creation and inserts."""


def create_states_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS states (
            state TEXT PRIMARY KEY,
            total INTEGER
        )
    """)


def save_state(conn, record):
    conn.execute(
        "INSERT OR REPLACE INTO states (state, total) VALUES (?, ?)",
        (record["state"], record["total"]),
    )