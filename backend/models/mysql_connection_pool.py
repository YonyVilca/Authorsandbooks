import time
import mysql.connector.pooling
import configparser

# Cargar la configuración de la base de datos
config = configparser.ConfigParser()
config.read('/home/global/project/mysql_config.ini')

dbconfig = {
    "host": config.get('mysql', 'host'),
    "port": config.get('mysql', 'port'),
    "user": config.get('mysql', 'user'),
    "password": config.get('mysql', 'pass'),
    "database": config.get('mysql', 'database'),
}

class MySQLPool(object):
    def __init__(self):             
        self.pool = self.create_pool(pool_name='task_pool', pool_size=3)

    def create_pool(self, pool_name, pool_size):
        # Crear una conexión de grupo
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **dbconfig
        )
        return pool

    def close(self, conn, cursor):
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

    def execute(self, sql, args=None, commit=False):
        # Ejecutar una consulta SQL
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)

            if commit:
                conn.commit()
                return cursor.lastrowid  # Devuelve el ID de la última fila insertada
            else:
                res = cursor.fetchall()
                return res
        except Exception as e:
            print(f"Error executing SQL: {e}")
            raise
        finally:
            self.close(conn, cursor)

    def executemany(self, sql, args, commit=False):
        # Ejecutar múltiples consultas SQL
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, args)
            if commit:
                conn.commit()
                return None
            else:
                res = cursor.fetchall()
                return res
        except Exception as e:
            print(f"Error executing SQL with many args: {e}")
            raise
        finally:
            self.close(conn, cursor)

if __name__ == "__main__":
    mysql_pool = MySQLPool()
    sql = "SELECT * FROM authors"  # Cambiado a la tabla authors        
    rv = mysql_pool.execute(sql)
    for result in rv:
        print(result)
    print("done")