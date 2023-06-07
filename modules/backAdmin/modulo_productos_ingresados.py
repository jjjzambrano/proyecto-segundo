from ..database import abrirConexion,cerrarConexion
# from datetime import datetime

class productosIngresados():
        def consulta():
         abrir = abrirConexion()
         cursor = abrir.cursor()
         cursor.execute("select * from producto_ingresado")
         extraer = cursor.fetchall()
         cerrarConexion(abrir)
         return extraer

        def consultaProveedor():
         abrir = abrirConexion()
         cursor = abrir.cursor()
         cursor.execute("select * from proveedor")
         extraer = cursor.fetchall()
         cerrarConexion(abrir)
         return extraer


        def registro(proveedor,nombre,precio,cantidad,imagen,categoria):
         # Llammamos a la conexion a la base de datos
         con= abrirConexion()
         conexion=con
         #Creamos el cursor con la conexion anteriormente llamado
         cursor= conexion.cursor()
         cursor.execute("select id_producto_ingresado from producto_ingresado")
         id = cursor.fetchall()
         # Validaciones de id 
         # si existe algun dato registrado  
         if(id!=[]):
          cursor.execute("select id_producto_ingresado from producto_ingresado")
          a = cursor.fetchall()
          a1 = (len(a))+1
          cursor.execute("insert into producto_ingresado values ({},{},'{}',{},{},'{}','{}')".format(a1,proveedor,nombre,precio,cantidad,imagen,categoria))
          conexion.commit()
         else:
          a2 = 1
          cursor.execute("insert into producto_ingresado values ({},{},'{}',{},{},'{}','{}')".format(a2,proveedor,nombre,precio,cantidad,imagen,categoria))
          conexion.commit()
         cerrarConexion(conexion)

        def registroProveedor(nombre,ruc,direccion,telefono,email):
         # Llammamos a la conexion a la base de datos
         con= abrirConexion()
         conexion=con
         #Creamos el cursor con la conexion anteriormente llamado
         cursor= conexion.cursor()
         cursor.execute("select id_proveedor from proveedor")
         id = cursor.fetchall()
         # Validaciones de id 
         # si existe algun dato registrado  
         if(id!=[]):
          cursor.execute("select id_proveedor from proveedor")
          a = cursor.fetchall()
          a1 = (len(a))+1
          cursor.execute("insert into proveedor values ({},'{}','{}','{}',{},'{}')".format(a1,nombre,ruc,direccion,telefono,email))
          conexion.commit()
         else:
          a2 = 1
          cursor.execute("insert into proveedor values ({},'{}','{}','{}',{},'{}')".format(a2,nombre,ruc,direccion,telefono,email))
          conexion.commit()
         cerrarConexion(conexion)


class Actual():

    def actualizar(proveedor,nombre,precio,cantidad,idrecivido):
      proveedor=proveedor
      nombre=nombre
      precio=precio
      cantidad=cantidad
      conexion= abrirConexion()
      cursor=conexion.cursor()

      cursor.execute("select id_producto_ingresado from producto_ingresado")
      id = cursor.fetchall()

      if(id!=[]):
            print('tiene datos')
            print(id)
            cursor.execute("select id_producto_ingresado from producto_ingresado")
            a1 = cursor.fetchall()
            a2= (len(a1))+1
            
            # cursor.execute("insert into ordenes_clientes values ({},{},{},12,'{}',{},'{}','vegetales','{}')".format(a2,b2,c2,nombre,cedula,correo,fecha))
            #query="UPDATE  producto_ingresado SET id_proveedor=%s, nombre_producto_ingresado=%s,precio_producto_ingresado=%s,cantidad_producto_ingresado=%s WHERE producto_ingresado.id_proveedor=%s;"
            # query="UPDATE  ordenes_clientes SET ({},{},{},12,'{}','{}','vegetales','{}' WHERE cedula_ordenes_cliente={})".format(a2,b2,c2,nombre,cedula,correo,fecha,cedula)
            #datos=(proveedor,nombre,precio,cantidad,id)
            data=cursor.execute("UPDATE  producto_ingresado SET id_proveedor={}, nombre_producto_ingresado='{}',precio_producto_ingresado={},cantidad_producto_ingresado={} WHERE id_producto_ingresado={};".format(proveedor,nombre,precio,cantidad,idrecivido))
            conexion.commit()
      else:
            value=1
            
            # cursor.execute("insert into personas (id_personas,id_rol,nombre_personas,dir_personas,telf_personas,email_personas,clave_personas) values ({},2,'dylan','12',12,'12','12')".format(value)

            # cursor.execute("insert into ordenes_clientes values ({},{},{},12,'{}',{},'{}','vegetales','{}')".format(value,value1,value2,nombre,cedula,correo,fecha))
            # query="UPDATE  ordenes_clientes SET ({},{},{},12,'{}','{}','vegetales','{}' WHERE cedula_ordenes_cliente={})".format(value,value1,value2,nombre,correo,fecha,cedula)
            query="UPDATE  producto_ingresado SET id_proveedor=%s, nombre_producto_ingresado=%s,precio_producto_ingresado=%s,cantidad_producto_ingresado=%s WHERE producto_ingresado.id_proveedor=%s;"
            # query="UPDATE  ordenes_clientes SET id_ordenes_clientes,id_clientes,numero_ordenes_clientes,subtotal_ordenes_clientes,nombre_ordenes_cliente,,correo_ordenes_cliente=,categoria_ordenes_cliente,fecha_ordenes_cliente WHERE cedula_ordenes_clientes;".format(value,value1,value2,nombre,cedula,correo,fecha,cedula)
            datos=(proveedor,nombre,precio,cantidad,id)
            data=cursor.execute(query,datos)
            conexion.commit()
      return data


class amostrar():
 def editaa(id): 
    conexion=abrirConexion()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM producto_ingresado WHERE id_producto_ingresado=%s",(id))
    formulario=cursor.fetchall()
    print(formulario)
    conexion.commit()
    return formulario,id
