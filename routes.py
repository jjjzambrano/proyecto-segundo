import os
from flask import Flask 
from flask import render_template,request,redirect,flash,url_for,jsonify,send_from_directory
from datetime import datetime
from random import randint
from modules.backCliente.modulo_reserva_cliente import ints,alm,eliminar,bebidas,carnes,vegetales,update,eed
#solo import aqui
from flask.helpers import url_for
# from de module aqui
from modules.users import users,Persona
#from modules.modulos import almaceje,edit,resiva
#from backCliente.modulo_reserva_cliente import ver
from wtforms import Form, BooleanField, StringField, validators
from modules.backCliente.modulo_almacenados import buscarP
from modules.backAdmin.modulo_productos_ingresados import productosIngresados,Actual,amostrar
from modules.backAdmin.modulo_clientes_registrados import consulta,consultaClintes,eliminarClientes,consultaId,busquedaCliente,Productoscliente
from modules.backAdmin.modulo_reservas import moduloreservas
from modules.backAdmin.modulo_productos_vendidos import productosVendidos
app=Flask(__name__)
app.secret_key="Develoteca"
CARPETA=os.path.join('static/images')
app.config['CARPETA']=CARPETA
@app.route('/static/images/<nombre>')
def img(nombre):
   return send_from_directory(app.config['CARPETA'],nombre)
# index 
@app.route('/')
def index():
    
    return render_template('index.html')

# users 
@app.route('/users/login')
def login():
   users.admin()
   return render_template('users/login.html')

@app.route('/users/login_admin', methods=['GET', 'POST'])
def loguin():
   if request.method == 'POST':
      email=request.form['email']
      password= request.form['password']
      print(email,password)
      correcto = users.loguin(email, password)
      if (correcto==0):
         flash ("Usuario y contraseña no validos")
         return redirect(url_for('login'))
      if (correcto==1):
         if(email == 'MADJS@gmail.com'):
            return redirect(url_for('panel'))

         return redirect(url_for('index'))

@app.route('/users/registrar/', methods=['GET','POST'])
def registrar():
      form=Persona()

      if form.validate_on_submit():
         try:
            name=request.form['nombre']
            dir=request.form['direccion']
            telf=int(request.form['telefono'])
            email=request.form['correo']
            clave1=request.form['clave']
            print(type(name),dir,telf,email,clave1)
            
            if telf<0:
               flash('Error en el campo telefono')
               return redirect(url_for('registrar'))

            
            users.registro(name,dir,telf,email,clave1)
            return redirect('/users/registrar/')
         except ValueError:
            # Esta captura el error cuando se manda un string en el telefono
            flash('Esta ingresando datos erroneos')
            return redirect(url_for('registrar'))

      return render_template('users/registrar.html', form=form)
# admin
@app.route('/panel')
def panel():
   return render_template('index_admin.html')

@app.route('/modulo/clientes')
def mClientes():
   personas=consulta()
   total,eliminados=consultaClintes()
   
   
   return render_template('admin/clientes_registrados.html',personas=personas,total=total,eliminados=eliminados)
# modal clientes registrados
@app.route('/ajaxfile', methods=['POST', 'GET'])
def ajaxfile():
   if request.method=='POST':
      userid= request.form['userid']

      personas,total=Productoscliente.consulta(userid)

   return jsonify({'htmlresponse': render_template('admin/reservasClientes.html',personas=personas,total=total )})


@app.route('/ajaxBuscar', methods=['POST', 'GET'])
def ajaxBus():
   if request.method=='POST':
      busqueda= request.form['uBuscar']
      print(busqueda)
      consulta=busquedaCliente(busqueda)
      if consulta != []:
         mensaje="Se ha encontrado el cliente"
         return jsonify({'htmlresponse': render_template('admin/busquedaCliente.html',consulta=consulta,mensaje=mensaje)})
      # eliminarClientes(userid)
      if consulta == []:
         mensaje="No se ha encontrado el cliente"
         return jsonify({'htmlresponse': render_template('admin/busquedaCliente.html',consulta=consulta,mensaje=mensaje)})


@app.route('/ajaxElim', methods=['POST', 'GET'])
def ajaxElim():
   if request.method=='POST':
      userid= int(request.form['userid'])
      personas=consultaId(userid)
      # eliminarClientes(userid)

      
   return jsonify({'htmlresponse': render_template('admin/alerta.html',personas=personas)})   

@app.route('/eliminar/<int:id>')
def meliminarClientes(id):
   eliminarClientes(id=id)

   return redirect('/modulo/clientes')

@app.route('/modulo/productosIngresados' , methods=['POST','GET'])
def mProductosI():
   productos = productosIngresados.consulta()
   proveedores = productosIngresados.consultaProveedor()
   #if request.method=='POST':
   #   proveedor = request.form['proveedor']
   #   empresa = request.form['empresa']
   #   nombre = request.form['nombre']
   #   precio = request.form['precio']
   #   cantidad = request.form['cantidad']
   #   productosIngresados.registro(proveedor,empresa,nombre,precio,cantidad) 
   #   return redirect(url_for('mProductosI')) 
   return render_template('admin/productos_ingresados.html', productos=productos, proveedores=proveedores)

@app.route('/crearProveedor',  methods=['POST','GET'])
def crearProveedor():
   if request.method=='POST':
      nombre = request.form['nombre']
      ruc = request.form['ruc']
      direccion = request.form['direccion']
      telefono = request.form['telefono']
      email = request.form['email']
      productosIngresados.registroProveedor(nombre,ruc,direccion,telefono,email) 
      return redirect(url_for('mProductosI')) 
   return render_template('admin/productos_ingresados.html')

@app.route('/registrarProducto',  methods=['POST','GET'])
def registrarProducto():
    if request.method=='POST':
       proveedor = request.form['proveedores']
       nombre = request.form['nombre']
       precio = request.form['precio']
       cantidad = request.form['cantidad']
       _imagen = request.files['imagen']
       categoria=request.form['categoria']
       now = datetime.now()
       tiempo = now.strftime("%Y%H%M%S")
       if _imagen.filename != '' :
        nuevaImagen = tiempo + _imagen.filename
        _imagen.save("static/images/"+nuevaImagen) 
       # _imagen.save("../static/imagen"+nuevaImagen) 
        productosIngresados.registro(proveedor,nombre,precio,cantidad,nuevaImagen,categoria) 
        return redirect(url_for('mProductosI')) 
    return render_template('admin/productos_ingresados.html')

#EditarProducto
@app.route('/modulo/edit/producto')
def editarProducto():
   return render_template('admin/editarProductos.html')

@app.route('/actualizarAd/<id>', methods=['POST'])
def actu(id):
   if request.method== 'POST':
    proveedor=request.form['proveedores']
    nombre=request.form['nombre']
    precio=request.form['precio']
    cantidad=request.form['cantidad']

    if(proveedor=='' or nombre == '' or precio==''  or cantidad=='' ):
       flash('Error existen Campos vacios')
       return redirect(url_for('mProductosI'))
   id=id[1]
   print(id)
   Actual.actualizar(proveedor,nombre,precio,cantidad,id)
   #print(nombre , cedula,correo,fecha)
   return redirect(url_for('mProductosI'))


@app.route('/editt/<int:id>',methods=['POST','GET'])
def editsd(id): 
    formulario,id=amostrar.editaa([id])
    return render_template('/admin/editarProductos.html',formulario=formulario,id=id)




@app.route('/modulo/productosVendidos')
def mProductosV():
   productos=productosVendidos.consulta()
   return render_template('admin/productos_vendidos.html',productos=productos)

@app.route('/modulo/reservas')
def mReservas():
   formulario=moduloreservas.prueba()
   return render_template('admin/reservas.html',formulario=formulario)

@app.route('/aceptarReserva/<id>')
def mInventario(id):
  moduloreservas.Aceptar(id)
  return redirect('/modulo/reservas')

@app.route('/rechazarReserva/<id>')
def rechazar(id):
  moduloreservas.rechazar(id)
  return redirect('/modulo/reservas')

# cliente 
@app.route('/cliente/almacenados')
def almacenados():
   formulario,elim=alm.almacenados()
   print(formulario)
   return render_template('cliente/almacenados.html',formulario=formulario,elim=elim)


## restaurar

@app.route('/restaurar/<int:id>')
def restaurar(id):
    alm.restaurar([id])
    return redirect(url_for('almacenados'))


# almacenados()

@app.route('/destroy/<int:cedula>')
def destroy(cedula):
    el=eliminar.dest([cedula])

    return redirect('/cliente/almacenados')


## comentar o descomentar almacenaje
# def almacena():
#    formulario=alm.almacenados()
#    #print(formulario)
#    return formulario

# almacena()
## comentar o descomentar  el insert into

@app.route('/cliente/reservar/')
def reservar():
   
   return render_template('cliente/reservar.html')

@app.route('/ajaxBuscarP',methods=['POST','GET'])
def ajaxBuscarP():
   
   if request.method=='POST':
      consulta=request.form['buscar'] 
      mensaje,respuesta= buscarP.busquedaProducto(consulta)
      
   return jsonify({'htmlresponse': render_template('cliente/BusquedaProducto.html',mensaje=mensaje,respuesta=respuesta)})

@app.route('/ajaxlimpieza', methods=['POST', 'GET'])
def rer():
   if request.method=='POST':
      id=request.form['userid']
   return jsonify({'respuesta': render_template('cliente/registroreserva.html',id=id)})


@app.route('/reservar/<id>', methods=['POST'])
def reser(id):
   nombre=request.form['txtNombre']
   cantidad=request.form['txtCantidad']
   cedula=request.form['txtCedula']
   correo=request.form['txtCorreo']
   fecha=request.form['txtFecha']
   id=id
   if(nombre=='' or cantidad =='' or cedula==''  or correo=='' or fecha=='' ):
      flash('Error existen Campos vacios')
      return redirect(url_for('reservar'))

   mensaje= ints.resr(nombre , cantidad,cedula,correo,fecha,id)
   if mensaje==0:
      return redirect(url_for('reservar'))
   #print(nombre , cedula,correo,fecha)
   return redirect('/cliente/reservar/')

### limpieza 
@app.route('/cliente/limpieza/')
def resert():
   limpieza=ints.consultaLimpieza()

   return render_template('cliente/limpieza.html',limpieza=limpieza)

@app.route('/reservar', methods=['POST'])
def resr():
   nombre=request.form['txtNombre']
   cantidad=request.form['txtCantidad']
   cedula=request.form['txtCedula']
   correo=request.form['txtCorreo']
   fecha=request.form['txtFecha']

   if(nombre=='' or cantidad == '' or cedula==''  or correo=='' or fecha=='' ):
      flash('Error existen Campos vacios')
      return redirect(url_for('reservar'))

   ints.resr(nombre , cantidad,cedula,correo,fecha)
   #print(nombre , cedula,correo,fecha)
   return redirect('/cliente/limpieza/')




###  bebidas 

@app.route('/cliente/bebidas/')
def rese():
   bebidas=ints.consultabebidas()
   return render_template('cliente/bebidas.html', bebidas=bebidas)

@app.route('/bebid', methods=['POST'])
def bbs():
   nombre=request.form['txtNombre']
   cantidad=request.form['txtCantidad']
   cedula=request.form['txtCedula']
   correo=request.form['txtCorreo']
   fecha=request.form['txtFecha']

   if(nombre=='' or cantidad == '' or cedula==''  or correo=='' or fecha=='' ):
      flash('Error existen Campos vacios')
      return redirect(url_for('rese'))

   bebidas.beb(nombre ,cantidad, cedula,correo,fecha)
   #print(nombre , cedula,correo,fecha)
   return redirect('/cliente/bebidas/')


## carnes
@app.route('/cliente/carnes/')
def crn():
   carnes=ints.consultacarnes()
   return render_template('cliente/carnes.html', carnes=carnes)

@app.route('/carnes', methods=['POST'])
def crs():
   nombre=request.form['txtNombre']
   cantidad=request.form['txtCantidad']
   cedula=request.form['txtCedula']
   correo=request.form['txtCorreo']
   fecha=request.form['txtFecha']

   if(nombre=='' or cantidad == '' or cedula==''  or correo=='' or fecha=='' ):
      flash('Error existen Campos vacios')
      return redirect(url_for('rese'))

   carnes.car(nombre ,cantidad, cedula,correo,fecha)
   #print(nombre , cedula,correo,fecha)
   return redirect('/cliente/carnes/')

## vegetales

@app.route('/cliente/vegetales/')
def veget():
   vegetales=ints.consultavegetales()
   return render_template('cliente/vegetales.html',vegetales=vegetales)

@app.route('/vegetales', methods=['POST'])
def vgt():
   nombre=request.form['txtNombre']
   cantidad=request.form['txtCantidad']
   cedula=request.form['txtCedula']
   correo=request.form['txtCorreo']
   fecha=request.form['txtFecha']

   if(nombre=='' or cantidad == '' or cedula==''  or correo=='' or fecha=='' ):
      flash('Error existen Campos vacios')
      return redirect(url_for('rese'))

   vegetales.ve(nombre , cantidad,cedula,correo,fecha)
   #print(nombre , cedula,correo,fecha)
   return redirect('/cliente/vegetales/')
#
#
# editar 
@app.route('/cliente/editar/')
def actua():

   return render_template('cliente/edit.html')

@app.route('/update/<int:id>', methods=['POST'])
def act(id):
   if request.method== 'POST':
    nombre=request.form['txtNombre']
    cantidad=request.form['txtCantidad']
    cedula=request.form['txtCedula']
    correo=request.form['txtCorreo']
    fecha=request.form['txtFecha']

    if(nombre=='' or cantidad == '' or cedula==''  or correo=='' or fecha=='' ):
       flash('Error existen Campos vacios')
       return redirect(url_for('almacenados'))

   update.actualizar(nombre ,cantidad, cedula,correo,fecha,id)
   #print(nombre , cedula,correo,fecha)
   return redirect(url_for('almacenados'))


@app.route('/edit/<int:id>')
def editrs(id): 
    formulario=eed.editaa([id])
    return render_template('/cliente/edit.html',formulario=formulario)




### funciona pero no guarda correctamente y no muestra ver por que error en formulario si se cambia la cedula no vale

# @app.route('/cliente/almacenados')
# def almacenados():
#    formulario=alm.almacenados()
#    print(formulario)
#    return render_template('cliente/almacenados.html',formulario=formulario)

# # almacenados()

# @app.route('/destroy/<int:cedula>')
# def destroy(cedula):
#     el=eliminar.dest([cedula])

#     return redirect('/cliente/almacenados')

#ejemplo

# @app.route('/ejemplo')
# def ejemplo():
#    ver = insert()
#    pw=resiva()
#    print(pw)
#    i=into()
#    print(i)
#    return ver, pw
# ejemplo()
if __name__=='__main__':
    app.run(debug=True)
