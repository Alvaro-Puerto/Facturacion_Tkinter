import sqlite3


def solo_numero(char):
    return char in '12345678.'


def conexion_consulta(consulta, parametros=()):
    with sqlite3.connect('Base_Facturacion.db') as conexion:
        try: #Captura la excepcion en caso de que algo falle
            cursor = conexion.cursor()
            resultado = cursor.execute(consulta, parametros) #  Establece la consulta sql a realizar y sus parametros
            conexion.commit()
                
            return resultado

        except Exception as e:

            print(e)
            conexion.close()
            return False
