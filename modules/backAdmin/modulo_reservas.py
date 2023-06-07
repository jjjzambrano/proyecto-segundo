from ..database import abrirConexion,cerrarConexion
    
class moduloreservas():
    def productosVendidos(c):
        conexion=abrirConexion()            
        cursor=conexion.cursor()
        cursor.execute("select id_producto_salida from producto_salida")
        id = cursor.fetchall()
         # Validaciones de id 
         # si existe algun dato registrado  
        if(id!=[]):
          cursor.execute("select id_producto_salida from producto_salida")
          a = cursor.fetchall()
          a1 = (len(a))+1
          cursor.execute("select id_ordenes_clientes from aceptar_reserva where id_aceptar_reserva ={}".format(c))
          consultaorden=cursor.fetchone()
          consultaorden=consultaorden[0]
          cursor.execute("select * from ordenes_clientes where id_ordenes_clientes={}".format(consultaorden))
          consultaorden1=cursor.fetchall()
          #print(consultaorden1[0][3],consultaorden1[0][5],'Holaaaaaaaaaaaaaaaaaaaaaaaaa2222222222222222222222222222222222')
          cursor.execute("select nombre_producto_ingresado from producto_ingresado where id_producto_ingresado ={}".format(consultaorden1[0][2]))
          nombreproducto=cursor.fetchone()
          nombreproducto=nombreproducto[0]
          print(consultaorden1[0][3],consultaorden1[0][5],'Holaaaaaaaaaaaaaaaaaaaaaaaaa2222222222222222222222222222222222')
          cursor.execute("INSERT INTO producto_salida values ({},{},'{}',{},{})".format(a1,c,nombreproducto,consultaorden1[0][3],consultaorden1[0][5]))
          conexion.commit()
        else:
          a2 = 1
          cursor.execute("select id_ordenes_clientes from aceptar_reserva where id_aceptar_reserva ={}".format(c))
          consultaorden=cursor.fetchone()
          consultaorden=consultaorden[0]
          cursor.execute("select * from ordenes_clientes where id_ordenes_clientes={}".format(consultaorden))
          consultaorden1=cursor.fetchall()
          cursor.execute("select nombre_producto_ingresado from producto_ingresado where id_producto_ingresado ={}".format(consultaorden1[0][2]))
          nombreproducto=cursor.fetchone()
          nombreproducto=nombreproducto[0]
          print(consultaorden1[0][3],consultaorden1[0][5],'Holaaaaaaaaaaaaaaaaaaaaaaaaa2222222222222222222222222222222222')
          cursor.execute("INSERT INTO producto_salida values ({},{},'{}',{},{})".format(a2,c,nombreproducto,consultaorden1[0][3],consultaorden1[0][5]))
          conexion.commit()
        cerrarConexion(conexion)

    def Aceptar(b):
        conexion=abrirConexion()
        cursor=conexion.cursor()
        cursor.execute("select id_aceptar_reserva from aceptar_reserva")
        id = cursor.fetchall()
         # Validaciones de id 
         # si existe algun dato registrado  
        if(id!=[]):
          cursor.execute("select id_aceptar_reserva from aceptar_reserva")
          a = cursor.fetchall()
          a1 = (len(a))+1
          cursor.execute("INSERT INTO aceptar_reserva values ({},{},1)".format(a1,b))
          conexion.commit()
          moduloreservas.productosVendidos(a1)
        else:
          a2 = 1
          cursor.execute("INSERT INTO aceptar_reserva values ({},{},1)".format(a2,b))
          conexion.commit()
          moduloreservas.productosVendidos(a2)
        cerrarConexion(conexion)
    def rechazar(b):
        conexion=abrirConexion()
        cursor=conexion.cursor()
        cursor.execute("select id_aceptar_reserva from aceptar_reserva")
        id = cursor.fetchall()
         # Validaciones de id 
         # si existe algun dato registrado  
        if(id!=[]):
          cursor.execute("select id_aceptar_reserva from aceptar_reserva")
          a = cursor.fetchall()
          a1 = (len(a))+1
          cursor.execute("INSERT INTO aceptar_reserva values ({},{},0)".format(a1,b))
          conexion.commit()
        else:
          a2 = 1
          cursor.execute("INSERT INTO aceptar_reserva values ({},{},0)".format(a2,b))
          conexion.commit()
        cerrarConexion(conexion)
    def prueba():
            conexion=abrirConexion()
            cursor=conexion.cursor()
            v=1
            numeros=[]
            cursor.execute("select * from ordenes_clientes where estado=0")
            consulta1=cursor.fetchall()

            cursor.execute("select * from ordenes_clientes o ,aceptar_reserva l where o.id_ordenes_clientes=l.id_ordenes_clientes")
            lista=cursor.fetchall()
            for i in lista:
                v=i[0]
                numeros.append(v)
                print(v)
            print(numeros)
            
            consultaF=[]
            for p in numeros:
              for i in consulta1:
                    if i[0]==p:
                        
                        consulta1.remove(i)
                        print(i[0],'esto es i')
                        print(i,'se esta eliminanddo esto')
                        print(p,'esto es p')
                    # cursor.execute("select * from ordenes_clientes where id_ordenes_clientes<>{}".format(p))
                    # resultado=cursor.fetchall()
                    # consultaF.append(resultado)
                    # cursor.execute("select * from ordenes_clientes where id_ordenes_clientes <> {p}".format())
                    # consulta2=cursor.fetchone()

            #print("sadsadasdasd")
            #print(consulta1,"")
            return consulta1

        
