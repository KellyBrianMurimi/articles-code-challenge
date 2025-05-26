from lib.models.author import Author
from lib.db.connection import get_connection
import pytest

@pytest.fixture
def db_connection():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def setup_test_data(db_connection):
    cursor = db_connection.cursor()
    
    # Clear and create fresh tables
    with open("lib/db/schema.sql") as f:
        schema = f.read()
    cursor.executescript(schema)
    
    # Insert test author and get its ID
    cursor.execute("INSERT INTO authors (name) VALUES ('Test Author')")
    db_connection.commit()
    
    cursor.execute("SELECT last_insert_rowid()")
    author_id = cursor.fetchone()[0]
    
    yield author_id
    
    # Clean up
    cursor.execute("DELETE FROM authors")
    db_connection.commit()

def test_author_find_by_id(setup_test_data, db_connection):
    author_id = setup_test_data
    author = Author.find_by_id(author_id)
    
    assert author is not None
    assert author.id == author_id
    assert author.name == "Test Author"

def test_author_save(db_connection):
    # Test saving a new author
    author = Author("New Author")
    saved_author = author.save()
    
    assert saved_author.id is not None
    assert saved_author.name == "New Author"
    
    # Verify it exists in database
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (saved_author.id,))
    db_author = cursor.fetchone()
    
    assert db_author is not None
    assert db_author['name'] == "New Author"