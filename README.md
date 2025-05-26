# articles-code-challenge

## Problem Statement
Build a system to model the relationship between Authors, Articles, and Magazines, with data persisted in a SQL database. In this domain:
- An `Author` can write many `Articles`
- A `Magazine` can publish many `Articles`
- An `Article` belongs to both an `Author` and a `Magazine`
- The `Author`-`Magazine` relationship is many-to-many
 

Setup Instructions
 

Choose one of the following options to set up your environment:
 

## Option 1: Using Pipenv
1. Install dependencies
pipenv install pytest sqlite3
2. Activate the virtual environment
pipenv shell
 

## Option 2: Using venv
1. Create a virtual environment
python -m venv env

2. Activate virtual environment (Mac/Linux)
source env/bin/activate
# OR (Windows)
# env\Scripts\activate
 

3. Install dependencies
pip install pytest
 

4. Database Setup
You can choose between SQLite (simpler) or PostgreSQL (more powerful) for this challenge:
 

### Option 1: SQLite (Recommended for beginners)
In lib/db/connection.py
import sqlite3

def get_connection():
conn = sqlite3.connect('articles.db')
conn.row_factory = sqlite3.Row # This enables column access by name
return conn
 

### Option 2: PostgreSQL
1. First create a database in PostgreSQL
createdb articles_challenge
# In lib/db/connection.py
import psycopg2
from psycopg2.extras import RealDictCursor
def get_connection():
conn = psycopg2.connect(
"dbname=articles_challenge user=your_username password=your_password"
)
conn.cursor_factory = RealDictCursor # This enables column access by name
return conn
```
 

## Recommended Project Structure
Use this structure with database components:
```
code-challenge/
├── lib/ # Main code directory
│ ├── models/ # Model classes
│ │ ├── __init__.py # Makes models a package
│ │ ├── author.py # Author class with SQL methods
│ │ ├── article.py # Article class with SQL methods
│ │ └── magazine.py # Magazine class with SQL methods
│ ├── db/ # Database components
│ │ ├── __init__.py # Makes db a package
│ │ ├── connection.py # Database connection setup
│ │ ├── seed.py # Seed data for testing
│ │ └── schema.sql # SQL schema definitions
│ ├── controllers/ # Optional: Business logic
│ │ └── __init__.py # Makes controllers a package
│ ├── debug.py # Interactive debugging
│ └── __init__.py # Makes lib a package
├── tests/ # Test directory
│ ├── __init__.py # Makes tests a package
│ ├── test_author.py # Tests for Author class
│ ├── test_article.py # Tests for Article class
│ └── test_magazine.py # Tests for Magazine class
├── scripts/ # Helper scripts
│ ├── setup_db.py # Script to set up the database
│ └── run_queries.py # Script to run example queries
└── README.md # Project documentation
```
 

### Structure Guidelines:
1. **Models**: Python classes that interact with the database via SQL
- `author.py`: Author class with methods using SQL queries
- `article.py`: Article class with relationships to Author and Magazine
- `magazine.py`: Magazine class with relationships
 

2. **Database Layer**:
- `connection.py`: Database connection handling
- `schema.sql`: Table definitions and constraints
- `seed.py`: Populate database with test data
 

3. **Package Organization**:
- Use `__init__.py` files to make directories into packages
- Each model file should handle its own SQL queries
 

4. **Testing**:
- Create separate test files for each model
- Tests should verify SQL queries and data integrity
- Run tests with `pytest` from the main directory
 

## Testing Your Code
- Run `pytest` to verify your implementation
- For debugging, use `python lib/debug.py` to start an interactive session
- Set up test database with: `python scripts/setup_db.py`
 

## Deliverables
 1. Database Schema
Create SQL tables for Authors, Articles, and Magazines with appropriate relationships:
 

```sql
-- Example schema (implement in lib/db/schema.sql)
CREATE TABLE IF NOT EXISTS authors (
id INTEGER PRIMARY KEY,
name VARCHAR(255) NOT NULL
);
 

CREATE TABLE IF NOT EXISTS magazines (
id INTEGER PRIMARY KEY,
name VARCHAR(255) NOT NULL,
category VARCHAR(255) NOT NULL
);
 

CREATE TABLE IF NOT EXISTS articles (
id INTEGER PRIMARY KEY,
title VARCHAR(255) NOT NULL,
author_id INTEGER,
magazine_id INTEGER,
FOREIGN KEY (author_id) REFERENCES authors(id),
FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);
```
 

 2. Python Classes with SQL Methods
 

#### Author Class
- Implement an Author class with proper initialization
- Write SQL methods to:
- Save an author to the database
- Find an author by ID or name
- Properties and validations for name
- Include methods to work with relationships
 

#### Magazine Class
- Implement a Magazine class with proper initialization
- Write SQL methods to:
- Save a magazine to the database
- Find a magazine by ID, name, or category
- Properties and validations for name and category
- Include methods to work with relationships
 

#### Article Class
- Implement an Article class with proper initialization
- Write SQL methods to:
- Save an article to the database
- Find articles by ID, title, author, or magazine
- Properties and validations for title
- Include methods to work with relationships
 

 3. SQL Query Methods
Implement these SQL queries within your model classes:
 

1. Get all articles written by a specific author
```python
# Example in Author class
def articles(self):
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
SELECT * FROM articles
WHERE author_id = ?
""", (self.id,))
return cursor.fetchall()
```
 

2. Find all magazines a specific author has contributed to
```python
# Example in Author class
def magazines(self):
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
SELECT DISTINCT m.* FROM magazines m
JOIN articles a ON m.id = a.magazine_id
WHERE a.author_id = ?
""", (self.id,))
return cursor.fetchall()
```
 

3. Get all authors who have written for a specific magazine
4. Find magazines with articles by at least 2 different authors
5. Count the number of articles in each magazine
6. Find the author who has written the most articles
 

4. Relationship Methods
 

#### Author Methods
- `articles()`: Returns list of all articles written by the author (using SQL)
- `magazines()`: Returns unique list of magazines the author has contributed to (using SQL)
- `add_article(magazine, title)`: Creates and inserts a new Article into the database
- `topic_areas()`: Returns unique list of categories of magazines the author has contributed to (using SQL)
 

#### Magazine Methods
- `articles()`: Returns list of all articles published in the magazine (using SQL)
- `contributors()`: Returns unique list of authors who have written for this magazine (using SQL)
- `article_titles()`: Returns list of titles of all articles in the magazine (using SQL)
- `contributing_authors()`: Returns list of authors with more than 2 articles in the magazine (using SQL)
 

5. Database Transactions
Implement transaction handling with Python's context managers:
 

```python
# Example transaction handling
def add_author_with_articles(author_name, articles_data):
"""
Add an author and their articles in a single transaction
articles_data: list of dicts with 'title' and 'magazine_id' keys
"""
conn = get_connection()
try:
conn.execute("BEGIN TRANSACTION")
cursor = conn.cursor()
# Insert author
cursor.execute(
"INSERT INTO authors (name) VALUES (?) RETURNING id",
(author_name,)
)
author_id = cursor.fetchone()[0]
# Insert articles
for article in articles_data:
cursor.execute(
"INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
(article['title'], author_id, article['magazine_id'])
)
conn.execute("COMMIT")
return True
except Exception as e:
conn.execute("ROLLBACK")
print(f"Transaction failed: {e}")
return False
finally:
conn.close()
```
 

### Bonus Challenges
1. Implement `Magazine.top_publisher()` class method using a complex SQL query to find the magazine with the most articles
2. Add database indexes to improve query performance
3. Implement a CLI tool that allows users to query the database interactively
 

## Evaluation Criteria
- Working code that correctly uses raw SQL queries within Python classes
- Proper database schema design with correct relationships
- SQL queries that are efficient and correct
- Transaction management and error handling
- Code organization and adherence to OOP principles
- Protection against SQL injection
- Test coverage of all SQL operations
 

## Version Control Requirements
 

You must create a Git repository and commit your work incrementally. Follow these guidelines:
 

### Repository Setup
1. Create a new Git repository for this challenge
2. Initialize with a README.md explaining the project
3. Set up a `.gitignore` file for Python (include virtual environments, cache files, database files, etc.)
 

### Commit Practices
1. Make small, focused commits that represent logical units of work
2. Commit frequently as you complete features or fix issues
3. Write clear, concise commit messages following this format:
```
[Feature/Fix/Refactor]: Brief description of what changed
 

- More detailed explanation if needed
- List specific changes made
```
 

### Commit Message Examples
- "Initialize project structure and database connection"
- "Implement Author class with SQL methods"
- "Add queries for article listing by author"
- "Fix transaction handling in article creation"
- "Optimize query performance for magazine contributors"
 

### Recommended Commit Sequence
1. Initial project setup and database connection
2. Database schema creation
3. Basic class implementation with SQL methods
4. Relationship query methods
5. More complex SQL query implementations
6. Transaction handling and error management
7. Tests and optimization
8. Documentation updates
 

### Submission
When you're ready to submit, ensure:
1. All tests pass
2. Your database schema is properly implemented
3. SQL queries are properly implemented and optimized
4. Your code is properly documented
5. Your repository shows a clear progression of work through commits
6. You've addressed all the requirements in the deliverables

## Technologies used
-Python
-SQL
-sqlite3
## License

Copyright <2025> <Kelly Brian>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

