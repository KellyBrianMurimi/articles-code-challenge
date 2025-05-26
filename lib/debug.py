import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def start_debug_session():
    print("Creating sample data...\n")
    
    # Creating authors
    kelly = Author.create("Kelly Brian")
    mwarika = Author.create("Mwarika Mwaura")
    bob = Author.create("Bob Johnson")

    # Creating magazines
    tech = Magazine.create("Tech Today", "Technology")
    science = Magazine.create("Science Weekly", "Science")
    business = Magazine.create("Business Insights", "Business")

    # Creating articles
    Article.create("Python Programming", kelly, tech)
    Article.create("Machine Learning", kelly, tech)
    Article.create("Quantum Physics", mwarika, science)
    Article.create("Neuroscience", mwarika, science)
    Article.create("Stock Market", bob, business)
    Article.create("Startup Funding", bob, business)
    
    # Show help message
    help_msg = """
Try these commands (type exactly as shown, no extra spaces):
kelly.articles()       # See Kelly's articles
mwarika.magazines()    # See magazines Mwarika writes for
bob.articles()         # See Bob's articles
tech.contributors()    # See who writes for Tech Today
Magazine.get_all()     # List all magazines
Article.find_by_author(kelly)  # Find Kelly's articles

Type exit() to quit
"""
    print(help_msg)
    
    import code
    vars = locals()
    code.interact(local=vars, banner="", exitmsg="")

if __name__ == "__main__":
    start_debug_session()