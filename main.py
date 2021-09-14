from sqlite3.dbapi2 import connect
import sys
import datetime
import random
import sqlite3

class Conexion:
    
    def open(self):
        try:
            self.con = sqlite3.connect('db.db')
            self.cursor = self.con.cursor()
        except sqlite3.Error as e:
            print(e)
        else:
            pass
            #print("Conexion con exito...")

    def createTables(self):
        try:
            self.open()
            self.cursor.execute("""Create Table Empleado ( numEmpleado int primary key, nombre char(50), apellidoPaterno char(50), apellidoMaterno char(50), fecha_alta date  );  
                    """)
            self.con.commit()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
  
            self.cursor.execute("Create Table EmpleadoAsistencia (numEmpleado int, fecha date, movimiento char(15), CONSTRAINT fk_column FOREIGN KEY(numEmpleado) REFERENCES Empleado(numEmpleado));")
            self.con.commit()
            self.con.close()
        except sqlite3.Error as e:
            if "already exists" in str(e):
                pass
            else:
                print(type(e))
        else:
            print("Tablas creadas con exito..")

    def deleteEmpleado(self,numEmpleado):
        try:
            self.open()
            sql = 'DELETE FROM Empleado WHERE numEmpleado = :numEmpleado'
            values = {
                "numEmpleado":numEmpleado
            }
            self.cursor.execute(sql,values)
            self.con.commit()
            self.con.close()   
        except sqlite3.Error as e:
            print("Error al eliminar usuario")
            print(e)
        else:
            print("Usuario Eliminado con exito.")

    def getEmpledo(self,numEmpleado):
        try:
            self.open()
            values = {
                "id":numEmpleado
            }
            sql = "select * from Empleado where numEmpleado = :id"
            self.cursor.execute(sql,values)
            resultado = self.cursor.fetchone()
            self.con.close()
        except sqlite3.Error as e:
            print(e)
            return False
        else:
            if resultado != None:
                return {"numEmpleado":resultado[0],"nombre":resultado[1],"apellidoPaterno":resultado[2],"apellidoMaterno":resultado[3],"fecha_alta":resultado[4]}
            print("Empleado no existe...")
            return False
    def updateEmpledo(self,empleado):
        try:
            self.open()
            sql = 'UPDATE Empleado SET nombre = :nombre, apellidoPaterno = :apellidoPaterno, apellidoMaterno = :apellidoMaterno WHERE numEmpleado = :numEmpleado'
            values = empleado
            self.cursor.execute(sql,values)
            self.con.commit()
            self.con.close()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Registro actualizado correctamente.")
    
    def showEmpleados(self):
        try:
            self.open()
            self.cursor.execute('SELECT * FROM Empleado')
            lista = self.cursor.fetchall()
            self.con.close()
        except sqlite3.Error as e:
            print(e)
        else:
            return lista
    def saveEmpleado(self,data):
        try:
            self.open()
            values = data
            sql = "INSERT INTO Empleado VALUES (:id,:nombre,:apellidop,:apellidom,:fechaalt)"
            self.cursor.execute(sql,values)
            self.con.commit()
            self.con.close()
        except:
            pass
        else:
            print("Registro creado...")
    def checkChecked(self,data):
        try:
            values = data
            self.open()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            sql = "SELECT * FROM EmpleadoAsistencia WHERE numEmpleado = :numEmpleado AND fecha = :fecha AND movimiento = :mov"
            self.cursor.execute(sql,values)
            resultados = self.cursor.fetchall()
            self.con.close()
        except sqlite3.Error as e:
            print("Error al verificar los datos...")
            print(e)
            return False
        else:
            return resultados
    def check(self,data):
        try:
            value = data
            self.open()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            sql = "INSERT INTO EmpleadoAsistencia (numEmpleado,fecha,movimiento) VALUES (:numEmpleado,:fecha,:mov)"
            self.cursor.execute(sql,value)
            self.con.commit()
            self.con.close()
        except:
            print("Error al marcar asistencia")
        else:
            print(f"{data['mov']} Marcada con exito.")
        
        
class Empleado:
    def __init__(self, empleado):
        
        self.__numEmpleado = empleado["numEmpleado"]
        self.__nombre = empleado["nombre"]
        self.__apellidoPaterno = empleado["apellidoPaterno"]
        self.__apellidoMaterno = empleado["apellidoMaterno"]
        self.__fecha_alta = empleado["fecha_alta"]
    @staticmethod
    def deleteEmpleado(numEmpleado,c):
        c.deleteEmpleado(numEmpleado)  
    @staticmethod
    def getEmpleado(numEmpleado,c):
        return c.getEmpledo(numEmpleado)
    @staticmethod
    def updateEmpleado(empleado,c):
        c.updateEmpledo(empleado)
    @staticmethod
    def showEmpleados(c):
        lista = c.showEmpleados()
        if lista:
            for i in lista:
                print(i)
    def save(self,c):
        values = {
                "id" : self.__numEmpleado,
                "nombre" : self.__nombre,
                "apellidop" : self.__apellidoPaterno,
                "apellidom" : self.__apellidoMaterno,
                "fechaalt" : self.__fecha_alta
                }
        c.saveEmpleado(values)
    @property
    def numEmpleado(self):
        return self.__numEmpleado

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self,nombre):
        self.__nombre = nombre
    
    @property 
    def apellidoPaterno(self):
        return self.__apellidoPaterno
    @apellidoPaterno.setter
    def apellidoPaterno(self,paterno):
        self.__apellidoPaterno = paterno

    @property 
    def apellidoMaterno(self):
        return self.__apellidoMaterno
    @apellidoMaterno.setter
    def apellidoMaterno(self,materno):
        self.__apellidoMaterno = materno

    
    def showData(self):
        print(self.__numEmpleado)
        print(self.__nombre)
        print(self.__apellidoPaterno)
        print(self.__apellidoMaterno)
        print(self.__fecha_alta)
        

class Checador:
    
    @staticmethod
    def check(numEmpleado,mov,c):
        data = {
            "numEmpleado":numEmpleado,
            "fecha":datetime.date.today(),
            "mov":mov
        }
        checadas = c.checkChecked(data)
        #print(checadas)
        if checadas != False:
            if len(checadas)<1:
                c.check(data)
            else:
                print(f"Ya se ha registrado la {mov} del dia de hoy")
       

        

class Main:
    def __init__(self,conexion):
        self.con = conexion
        while True:
            print(SEPARADOR)
            opcion = self.showMenu()
            if opcion == 1:
                print(SEPARADOR)
                self.marcarEntrada()#done

            elif opcion == 2:
                print(SEPARADOR)
                self.marcarSalida()#done
            elif opcion == 3:
                print(SEPARADOR)
                self.showEmpleados()#done
            elif opcion == 4:
                print(SEPARADOR)
                self.altaEmpleado()#done
            elif opcion == 5:
                print(SEPARADOR)
                self.modEmpleado()
            elif opcion == 6:
                self.bajaEmpleado()#done

            elif opcion == 0:
                self.exit()#done
            else:
                print("Opcion no vàlida intentalo de nuevo...")


    def showMenu(self):
        while True:
            print("1.-Marcar Entrada\n2.-Marcar Salida\n3.-Listar Empleados\n4.-Alta empleado\n5.-Modificar Empleado\n6.-Eliminar Empleado\n0.-Salir del programa\nElige una opcion")
            
            try:
                self.opcion = int(input())
            except:
                print("valor no valido...")
            else:
                return self.opcion

    def showEmpleados(self):
        Empleado.showEmpleados(self.con)
    def marcarEntrada(self):
        print("Marcar entrada")
        while True:
            try:
                empleado = int(input("Numero de Empleado: <0 para salir>\n"))
            except:
                print("Valor no valido intentalo de nuevo.")
            else:
                if empleado == 0:
                    return
                Checador.check(empleado,"Entrada",self.con)
                break

    def marcarSalida(self):
        print("Marcar Salida")
        while True:
            try:
                empleado = int(input("Numero de Empleado: <0 para salir>\n"))
            except:
                print("Valor no valido intentalo de nuevo.")
            else:
                if empleado == 0:
                    return
                Checador.check(empleado,"Salida",self.con)
                break
    def altaEmpleado(self):
        nombre = self.inputAdd("Nombre")
        paterno = self.inputAdd("Apellido Paterno")
        materno = self.inputAdd("Apellido Materno")
        fecha = datetime.date.today()
        data = {
            "numEmpleado":round(random.random()*100),
            "nombre":nombre,
            "apellidoPaterno":paterno,
            "apellidoMaterno":materno,
            "fecha_alta":fecha
        }
        e = Empleado(data)
        
        e.save(self.con)
        
        del e
    def modEmpleado(self):
        print(20*"*")
        #print(Empleado.getEmpleado(91147))
        while True:
            try:
                numEmpleado = int(input("Ingrese el numero de empleado... 0 para volver"))
                data = Empleado.getEmpleado(numEmpleado)
                if data != False:
                    e = Empleado(data)
                    print("se obtuvo empleado")

                else:
                    if numEmpleado == 0:
                        return
                    print("Ningun empleado encontrado...")
                    continue
            except sqlite3.Error as e:
                print(e)
            except Exception as e:
                print(e)
            else:
                break

        
        print(20*"*")

        value = self.inputEdit("Nombre: ",e.nombre)
        if value != False:
            
            e.nombre = value
            e.showData()
        value = self.inputEdit("Apellido Paterno: ",e.apellidoPaterno)
        if value != False:
            e.apellidoPaterno = value

        value = self.inputEdit("Apellido Materno: ",e.apellidoMaterno)
        if value != False:
            e.apellidoMaterno = value
        
        data = {
            "numEmpleado" : e.numEmpleado,
            "nombre" : e.nombre,
            "apellidoPaterno" : e.apellidoPaterno,
            "apellidoMaterno" : e.apellidoMaterno
        }
        while True:
            print(f"Numero Empleado : {data['numEmpleado']}\nNombre : {data['nombre']}\nApellidos : {data['apellidoPaterno']} {data['apellidoMaterno']}")
            editar = input("Desea guardar los cambios? <1 si - 0 no>")
            if editar in ("1","0"):
                if editar == "1":
                    Empleado.updateEmpleado(data,self.con)
                    break
                elif editar == "0":
                    print("Operacion cancelada...")
                    break
            else:
                print("Opcion no válida")

        
    def bajaEmpleado(self):
        while True:
            print("Eliminar Usuario")
            try:
                numEmpleado = int(input("Numero de Empleado: <0 para volver>\n"))
                if numEmpleado == 0:
                    return
            except:
                print("Valor no valido...")
            else:
                empleado = Empleado.getEmpleado(numEmpleado,self.con)
                if empleado != False:
                    while True:
                        print("Desea eliminar al empleado con los siguientes datos: <1 si - 0 no>")
                        print(f"No. Empleado: {empleado['numEmpleado']}\nNombre Completo: {empleado['nombre']} {empleado['apellidoPaterno']} {empleado['apellidoMaterno']}")
                        delete = input()
                        if delete in ("1","0"):
                            if delete == "1":
                                Empleado.deleteEmpleado(numEmpleado,self.con)
                                return
                            elif delete == "0":
                                print("Operacion cancelada.")
                                return

                        
                        else:
                            print("Opcion no valida intentalo de nuevo por favor")



        
    def inputEdit(self,label,value):
        print(label,value,'0 para dejar el mismo\n')
        new_value = input(f"Nuevo {label}:\n")
        if new_value == "0":
            return False
        return new_value
    
    def inputAdd(self,label):
        while True:
            value = input(f'Ingrese el {label}\n')
            if len(value) > 0:
                return value
            else:
                print(f"Ingrese el {label}")
            
        
        
        
    def exit(self):
        print("Saliendo del programa")
        sys.exit()
    
    

SEPARADOR = "*"*50
print(SEPARADOR)
print("Iniciando programa")



c = Conexion()
c.open()
c.createTables()
n = Main(c)

print(SEPARADOR)
print("Fin del programa")







