from ..database import abrirConexion,cerrarConexion
class productosVendidos:
    def consulta():
        conexion=abrirConexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from producto_salida")
        consulta=cursor.fetchall()
        cerrarConexion(conexion)
        return consulta

