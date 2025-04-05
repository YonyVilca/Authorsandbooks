from backend.models.mysql_connection_pool import MySQLPool

class BookModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def author_exists(self, author_id):
        params = {'author_id': author_id}
        rv = self.mysql_pool.execute("SELECT COUNT(*) FROM authors WHERE author_id=%(author_id)s", params)
        return rv[0][0] > 0  # Devuelve True si el autor existe

    def get_book(self, book_id):    
        params = {'book_id': book_id}
        try:
            rv = self.mysql_pool.execute("SELECT * FROM books WHERE book_id=%(book_id)s", params)
            if rv:
                return [{'book_id': result[0], 'book_title': result[1], 'book_description': result[2], 
                         'author_id': result[3], 'publication_year': result[4], 'genre': result[5]} for result in rv]
            else:
                return "libro no encontrado."
        except Exception as e:
            print(f"Error fetching book: {e}")
            return "Error fetching book."

    def get_books(self):  
        try:
            rv = self.mysql_pool.execute("SELECT * FROM books")
            return [{'book_id': result[0], 'book_title': result[1], 'book_description': result[2], 
                     'author_id': result[3], 'publication_year': result[4], 'genre': result[5]} for result in rv]
        except Exception as e:
            print(f"Error fetching books: {e}")
            return "Error fetching books."

    def create_book(self, book_title, book_description, author_id, publication_year, genre):    
        if not self.author_exists(author_id):
            raise ValueError(f"Author with ID {author_id} does not exist.")

        data = {
            'book_title': book_title,
            'book_description': book_description,
            'author_id': author_id,
            'publication_year': publication_year,
            'genre': genre
        }  
        query = """INSERT INTO books (book_title, book_description, author_id, publication_year, genre) 
                   VALUES (%(book_title)s, %(book_description)s, %(author_id)s, %(publication_year)s, %(genre)s)"""    
        lastrowid = self.mysql_pool.execute(query, data, commit=True)
        return "Libro creado con ID: {}".format(lastrowid)

    def update_book(self, book_id, book_title, book_description, author_id, publication_year, genre):    
        data = {
            'book_id': book_id,
            'book_title': book_title,
            'book_description': book_description,
            'author_id': author_id,
            'publication_year': publication_year,
            'genre': genre
        }  
        query = """UPDATE books 
                   SET book_title = %(book_title)s, book_description = %(book_description)s, author_id = %(author_id)s, 
                       publication_year = %(publication_year)s, genre = %(genre)s 
                   WHERE book_id = %(book_id)s"""    
        self.mysql_pool.execute(query, data, commit=True)
        return "Libro actualizado."

    def delete_book(self, book_id):    
        params = {'book_id': book_id}      
        query = """DELETE FROM books WHERE book_id = %(book_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)
        return "Libro eliminado."