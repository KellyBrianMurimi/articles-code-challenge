import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    
    # Create test data
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine", "Test Category")
    Article.create("Test Article", author, magazine)
    
    yield
    
    # Clean up
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_author_creation():
    author = Author("Test Author")
    assert author.name == "Test Author"

def test_author_save():
    author = Author("Test Author")
    saved_author = author.save()
    assert saved_author.id is not None

def test_author_find_by_id(setup_db):
    author = Author.find_by_id(1)
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_db):
    author = Author.find_by_id(1)
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Test Magazine"

def test_author_topic_areas(setup_db):
    author = Author.find_by_id(1)
    topics = author.topic_areas()
    assert len(topics) == 1
    assert topics[0] == "Test Category"