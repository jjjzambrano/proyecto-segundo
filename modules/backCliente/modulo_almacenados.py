from ..database import abrirConexion ,cerrarConexion
class buscarP():
 def busquedaProducto(p):
  conexion=abrirConexion()
  cursor= conexion.cursor()
  cursor.execute("select * from producto_ingresado Where nombre_producto_ingresado = '{}';".format(p))
  consulta=cursor.fetchall()
  if consulta==[]:
      print('Producto No Encontrado')
      cerrarConexion(conexion)
      return 'Producto No Encontrado',consulta
  else:  
     print(consulta,'Holaaaaaaaaaaaaaaaaaaaaaaa')
     cerrarConexion(conexion)
     return 'Producto Encontrado',consulta

