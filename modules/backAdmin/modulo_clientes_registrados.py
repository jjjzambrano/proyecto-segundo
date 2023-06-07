from ..database import abrirConexion,cerrarConexion
def consulta():
    conexion=abrirConexion()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM personas where estado=0 order by id_personas asc")
    personas=cursor.fetchall()
    # cursor.execute("SELECT count(*) FROM personas ")
    # # total=cursor.fetchone()
    # total=cursor.fetchone()
    # total=total[0]
    cerrarConexion(conexion)
    return personas

def consultaClintes():
    conexion=abrirConexion()
    cursor= conexion.cursor()
    cursor.execute("SELECT count(*) FROM personas where estado=0")
    total=cursor.fetchone()
    total=total[0]
    cursor.execute("SELECT count(*) FROM personas where estado=1 ")
    totalEliminado=cursor.fetchone()
    totalEliminado=totalEliminado[0]

    cerrarConexion(conexion)
    return total,totalEliminado

def eliminarClientes(id):
    print('el id es:',id)
    conexion=abrirConexion()
    cursor=conexion.cursor()
    cursor.execute("update personas set estado=1 where id_personas={}".format(id))
    # cursor.execute("DELETE FROM personas WHERE id_personas={}".format(id))
    conexion.commit()
    cerrarConexion(conexion)

def consultaId(id):
    conexion=abrirConexion()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM personas WHERE id_personas={}".format(id))
    consulta=cursor.fetchall()
    conexion.commit()
    cerrarConexion(conexion)
    return consulta

    
def busquedaCliente(name):
    conexion=abrirConexion()
    cursor=conexion.cursor()
    cursor.execute("select * from personas where nombre_personas='{}'".format(name))
    consulta=cursor.fetchall()
    conexion.commit()
    cerrarConexion(conexion)
    return consulta
class Productoscliente:
    def consulta(d):
        conexion=abrirConexion()
        cursor= conexion.cursor()
        cursor.execute("select * from ordenes_clientes where id_personas={}".format(d))
        consulta=cursor.fetchall()
        cursor.execute("select count(*) from ordenes_clientes where id_personas={}".format(d))
        total=cursor.fetchone()
        total=total[0]
        cerrarConexion(conexion)
        return consulta,total
