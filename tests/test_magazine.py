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
    author1 = Author.create("Author 1")
    author2 = Author.create("Author 2")
    magazine = Magazine.create("Test Magazine", "Test Category")
    Article.create("Article 1", author1, magazine)
    Article.create("Article 2", author1, magazine)
    Article.create("Article 3", author1, magazine)
    Article.create("Article 4", author2, magazine)
    
    yield
    
    # Clean up
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_magazine_creation():
    magazine = Magazine("Test Magazine", "Test Category")
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Test Category"

def test_magazine_save():
    magazine = Magazine("Test Magazine", "Test Category")
    saved_magazine = magazine.save()
    assert saved_magazine.id is not None

def test_magazine_find_by_id(setup_db):
    magazine = Magazine.find_by_id(1)
    assert magazine is not None
    assert magazine.name == "Test Magazine"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_id(1)
    articles = magazine.articles()
    assert len(articles) == 4

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributors()
    assert len(contributors) == 2

def test_magazine_article_titles(setup_db):
    magazine = Magazine.find_by_id(1)
    titles = magazine.article_titles()
    assert len(titles) == 4
    assert "Article 1" in titles

def test_magazine_contributing_authors(setup_db):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Author 1"

def test_magazine_top_publisher(setup_db):
    top_magazine = Magazine.top_publisher()
    assert top_magazine is not None
    assert top_magazine.name == "Test Magazine"