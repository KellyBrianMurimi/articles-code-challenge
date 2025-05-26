import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.db.connection import get_connection

def setup_database():
    with open("lib/db/schema.sql") as f:
        schema = f.read()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()