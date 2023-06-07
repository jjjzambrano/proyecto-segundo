import psycopg2


# try:
def abrirConexion():
        con= psycopg2.connect(
            host = 'localhost',
            database = 'MADJS-F',
            user = 'postgres',
            password  = '152018'
            )
        return con

# except:
            # print('Error al conectarse ')    

def cerrarConexion(con):
    con.close() 





