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
    article = Article.create("Test Article", author, magazine)
    
    yield
    
    # Clean up
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_creation():
    article = Article("Test Article", 1, 1)
    assert article.title == "Test Article"
    assert article.author_id == 1
    assert article.magazine_id == 1

def test_article_save():
    article = Article("Test Article", 1, 1)
    saved_article = article.save()
    assert saved_article.id is not None

def test_article_find_by_id(setup_db):
    article = Article.find_by_id(1)
    assert article is not None
    assert article.title == "Test Article"

def test_article_author(setup_db):
    article = Article.find_by_id(1)
    author = article.author()
    assert author is not None
    assert author.name == "Test Author"

def test_article_magazine(setup_db):
    article = Article.find_by_id(1)
    magazine = article.magazine()
    assert magazine is not None
    assert magazine.name == "Test Magazine"

def test_article_find_by_author(setup_db):
    author = Author.find_by_id(1)
    articles = Article.find_by_author(author)
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_article_find_by_magazine(setup_db):
    magazine = Magazine.find_by_id(1)
    articles = Article.find_by_magazine(magazine)
    assert len(articles) == 1
    assert articles[0].title == "Test Article"