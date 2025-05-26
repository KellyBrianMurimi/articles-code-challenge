from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Clear existing data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    # Create authors
    author1 = Author.create("Kelly Brian")
    author2 = Author.create("Mwarika Mwaura")
    author3 = Author.create("Bob Johnson")

    # Create magazines
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Science Weekly", "Science")
    magazine3 = Magazine.create("Business Insights", "Business")

    # Create articles
    Article.create("Python Programming", author1, magazine1)
    Article.create("Machine Learning", author1, magazine1)
    Article.create("Quantum Physics", author2, magazine2)
    Article.create("Neuroscience", author2, magazine2)
    Article.create("Stock Market", author3, magazine3)
    Article.create("Startup Funding", author3, magazine3)
    Article.create("AI Ethics", author1, magazine2)
    Article.create("Data Science", author1, magazine2)
    Article.create("Blockchain", author2, magazine1)
    Article.create("Cybersecurity", author3, magazine1)

def get_connection():
    from lib.db.connection import get_connection as get_db_connection
    return get_db_connection()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")