from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    def delete(self):
        if not self.id:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, title, author, magazine):
        article = cls(title, author.id, magazine.id)
        return article.save()

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['title'], row['author_id'], row['magazine_id'], row['id'])
        return None

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def find_by_author(cls, author):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author.id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine.id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]