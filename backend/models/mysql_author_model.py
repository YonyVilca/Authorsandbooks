from backend.models.mysql_connection_pool import MySQLPool

class AuthorModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def get_author(self, author_id):    
        params = {'author_id': author_id}
        try:
            rv = self.mysql_pool.execute("SELECT * FROM authors WHERE author_id=%(author_id)s", params)
            if rv:
                return [{'author_id': result[0], 'author_name': result[1], 'author_bio': result[2], 
                         'author_photo': result[3]} for result in rv]
            else:
                return "Autor no encontrado."
        except Exception as e:
            print(f"Error fetching author: {e}")
            return "Error fetching author."

    def get_authors(self):  
        try:
            rv = self.mysql_pool.execute("SELECT * FROM authors")
            return [{'author_id': result[0], 'author_name': result[1], 'author_bio': result[2], 
                     'author_photo': result[3]} for result in rv]
        except Exception as e:
            print(f"Error fetching authors: {e}")
            return "Error fetching authors."

    def create_author(self, author_name, author_bio, author_photo):    
        data = {
            'author_name': author_name,
            'author_bio': author_bio,
            'author_photo': author_photo
        }  
        query = """INSERT INTO authors (author_name, author_bio, author_photo) 
                   VALUES (%(author_name)s, %(author_bio)s, %(author_photo)s)"""    
        lastrowid = self.mysql_pool.execute(query, data, commit=True)
        return "Autor creado con ID: {}".format(lastrowid)

    def update_author(self, author_id, author_name, author_bio, author_photo):    
        data = {
            'author_id': author_id,
            'author_name': author_name,
            'author_bio': author_bio,
            'author_photo': author_photo
        }  
        query = """UPDATE authors 
                   SET author_name = %(author_name)s, author_bio = %(author_bio)s, author_photo = %(author_photo)s 
                   WHERE author_id = %(author_id)s"""    
        self.mysql_pool.execute(query, data, commit=True)
        return "Autor actualizado."

    def delete_author(self, author_id):    
        params = {'author_id': author_id}      
        query = """DELETE FROM authors WHERE author_id = %(author_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)
        return "Autor eliminado."