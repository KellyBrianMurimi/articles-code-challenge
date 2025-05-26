import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def start_debug_session():
    print("\n WELCOME TO THE DEBUG CONSOLE!")
    print("Let's explore authors, magazines and articles!\n")
    print("Creating sample data...\n")
    
    # Test data
    kelly = Author.create("Kelly Brian")
    mwarika = Author.create("Mwarika Mwaura")
    bob = Author.create("Bob Johnson")
    
    tech = Magazine.create("Tech Today", "Technology")
    science = Magazine.create("Science Weekly", "Science")
    business = Magazine.create("Business Insights", "Business")
    
    Article.create("Python Programming", kelly, tech)
    Article.create("Machine Learning", kelly, tech)
    Article.create("Quantum Physics", mwarika, science)
    Article.create("Neuroscience", mwarika, science)
    Article.create("Stock Market", bob, business)
    Article.create("Startup Funding", bob, business)
    
    console_vars = {
        'Author': Author,
        'Magazine': Magazine,
        'Article': Article,
        'kelly': kelly,
        'mwarika': mwarika,
        'bob': bob,
        'tech': tech,
        'science': science,
        'business': business
    }
    
    # Show help message
    help_msg = """
Try these commands:
kelly.articles()       # See Kelly's articles
mwarika.magazines()    # See magazines Mwarika writes for
bob.articles()         # See Bob's articles
tech.contributors()    # See who writes for Tech Today
Magazine.get_all()     # List all magazines
Article.find_by_author(kelly)  # Find Kelly's articles

Available variables:
- Authors: kelly, mwarika, bob
- Magazines: tech, science, business
- Classes: Author, Magazine, Article

Type exit() to quit
"""
    print(help_msg)
    
    import code
    code.interact(local=console_vars, banner="", exitmsg="")

if __name__ == "__main__":
    start_debug_session()