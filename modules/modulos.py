# MODULOS se comunica con los modulos inferiores, envia datos a la db y envia datos a las rutas 
#from database import con
#from backCliente.modulo_reserva_cliente import igual
#from modules.database import cerrarConexion,abrirConexion
# aqui para routes
from flask import render_template,request
from datetime import datetime
from threading import current_thread
#from backCliente.modulo_reserva_cliente import ver
#from modules.database import abrirConexion,cerrarConexion
import time 

#from backCliente.modulo_reserva_cliente import ver


# def l():
#   lt=ver()
#   print(lt)
#   return lt

# l()

#from backCliente.modulo_reserva_cliente import ver
# def resiva():
#         cone=con
#         cursor= cone.cursor()
#         cursor.execute('SELECT * FROM rol')
#         print(cursor.fetchall())
        
#         cone.commit
# resiva()




