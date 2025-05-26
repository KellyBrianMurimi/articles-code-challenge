import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def db_connection():
    """Fixture for database connection with automatic cleanup"""
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def test_data(db_connection):
    """Fixture for creating consistent test data"""
    cursor = db_connection.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    db_connection.commit()
    
    # Create test data
    author1 = Author.create("Author 1")
    author2 = Author.create("Author 2")
    magazine = Magazine.create("Tech Magazine", "Technology")
    
    # Create articles with varied data
    articles = [
        ("Python Basics", author1, magazine),
        ("Advanced Python", author1, magazine),
        ("Web Development", author1, magazine),
        ("Data Science", author2, magazine)
    ]
    
    for title, author, mag in articles:
        Article.create(title, author, mag)
    
    yield {
        'authors': [author1, author2],
        'magazine': magazine,
        'articles': articles
    }
    
    # Cleanup handled by db_connection fixture

class TestMagazineModel:
    """Test suite for Magazine model"""
    
    def test_magazine_creation(self):
        magazine = Magazine("Science Journal", "Science")
        assert magazine.name == "Science Journal"
        assert magazine.category == "Science"
    
    def test_magazine_save(self, db_connection):
        magazine = Magazine("Business Weekly", "Business")
        saved_magazine = magazine.save()
        
        assert saved_magazine.id is not None
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (saved_magazine.id,))
        db_record = cursor.fetchone()
        assert db_record is not None
        assert db_record['name'] == "Business Weekly"

    def test_magazine_find_by_id(self, test_data):
        magazine = Magazine.find_by_id(test_data['magazine'].id)
        assert magazine is not None
        assert magazine.name == "Tech Magazine"
        assert magazine.category == "Technology"

    def test_magazine_articles(self, test_data):
        magazine = test_data['magazine']
        articles = magazine.articles()
        assert len(articles) == 4
        assert all(isinstance(article, Article) for article in articles)

    def test_magazine_contributors(self, test_data):
        magazine = test_data['magazine']
        contributors = magazine.contributors()
        assert len(contributors) == 2
        assert all(contributor.name in ["Author 1", "Author 2"] for contributor in contributors)

    def test_magazine_article_titles(self, test_data):
        magazine = test_data['magazine']
        titles = magazine.article_titles()
        assert len(titles) == 4
        assert "Python Basics" in titles
        assert "Data Science" in titles

    def test_magazine_contributing_authors(self, test_data):
        magazine = test_data['magazine']
        contributors = magazine.contributing_authors()
        assert len(contributors) == 1
        assert contributors[0].name == "Author 1"

    def test_magazine_top_publisher(self, test_data):
        # Create additional magazine for comparison
        Magazine.create("Science Digest", "Science")
        top_magazine = Magazine.top_publisher()
        assert top_magazine is not None
        assert top_magazine.name == "Tech Magazine"