from lib.models.article import Article

def test_article_save():
    from lib.models.author import Author
    from lib.models.magazine import Magazine
    
    author = Author("Test Author").save()
    magazine = Magazine("Test Magazine", "Test").save()
    
    article = Article("Test Article", author.id, magazine.id)
    saved_article = article.save()
    
    assert saved_article.id is not None
    assert saved_article.title == "Test Article"
    assert saved_article.author_id == author.id
    assert saved_article.magazine_id == magazine.id