from sqlite3.dbapi2 import connect
import sys
import datetime
import random
import sqlite3
print("Inicio programa")
try:
    con = sqlite3.connect('db.db')

    cursor = con.cursor()

    cursor.execute("""Create Table Empleado ( numEmpleado int primary key, nombre char(50), apellidoPaterno char(50), apellidoMaterno char(50), fecha_alta date  );
                    
                    """)
    con.commit()

    con.close()
except:
    pass
else:
    try:
        con = sqlite3.connect('db.db')

        cursor = con.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")
  
        cursor.execute("Create Table EmpleadoAsistencia (numEmpleado int, fecha date, movimiento char(15), CONSTRAINT fk_column FOREIGN KEY(numEmpleado) REFERENCES Empleado(numEmpleado));")
        con.commit()

        con.close()
    except sqlite3.Error as e:
        print(e)
    else:
        print("tablas creadas")
    




class Empleado:
    
    def __init__(self, empleado):
        
        self.__numEmpleado = empleado["numEmpleado"]
        self.__nombre = empleado["nombre"]
        self.__apellidoPaterno = empleado["apellidoPaterno"]
        self.__apellidoMaterno = empleado["apellidoMaterno"]
        self.__fecha_alta = empleado["fecha_alta"]

    @staticmethod
    def updateEmpleado(empleado):
        try:
            print(empleado)
            con = sqlite3.connect('db.db')

            cursor = con.cursor()
            
            sql = 'UPDATE Empleado SET nombre = :nombre, apellidoPaterno = :apellidoPaterno, apellidoMaterno = :apellidoMaterno WHERE numEmpleado = :numEmpleado'
            values = empleado

            cursor.execute(sql,values)

            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(e)
        else:
            print("Registro actualizado correctamente.")
    @staticmethod
    def getEmpleado(numEmpleado):
        try:
            con = sqlite3.connect("db.db")
            cursor = con.cursor()
            values = {
                "id":numEmpleado
            }
            sql = "select * from Empleado where numEmpleado = :id"
            cursor.execute(sql,values)
            resultado = cursor.fetchone()
            con.close()


        except sqlite3.Error as e:
            print(e)
            return False
        else:
            if resultado != None:
                return {"numEmpleado":resultado[0],"nombre":resultado[1],"apellidoPaterno":resultado[2],"apellidoMaterno":resultado[3],"fecha_alta":resultado[4]}
            return False

    @staticmethod
    def showEmpleados():
        try:
            con = sqlite3.connect('db.db')

            cursor = con.cursor()
            cursor.execute('SELECT * FROM Empleado')
            lista = cursor.fetchall()

            con.close()
        except sqlite3.Error as e:
            print(e)
        else:
            for i in lista:
                print(i)

    def save(self):
        try:
            con = sqlite3.connect('db.db')

            cursor = con.cursor()
            values = {
                "id" : self.__numEmpleado,
                "nombre" : self.__nombre,
                "apellidop" : self.__apellidoPaterno,
                "apellidom" : self.__apellidoMaterno,
                "fechaalt" : self.__fecha_alta
            }
            sql = "INSERT INTO Empleado VALUES (:id,:nombre,:apellidop,:apellidom,:fechaalt)"
            cursor.execute(sql,values)
            con.commit()

            con.close()
        except:
            pass
        else:
            print("Registro creado...")
    
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
    def check(numEmpleado,mov):
        data = {
            "numEmpleado":numEmpleado,
            "fecha":datetime.date.today(),
            "mov":mov
        }
        try:
            values = data
            con = sqlite3.connect('db.db')
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            sql = "SELECT * FROM EmpleadoAsistencia WHERE numEmpleado = :numEmpleado AND fecha = :fecha AND movimiento = :mov"
            cursor.execute(sql,values)
            resultados = cursor.fetchall()
            con.close()

        except sqlite3.Error as e:
            print("Error al verificar los datos...")
            print(e)
            return
        else:
            #print(resultados)
            if len(resultados)<1:
                try:
                    value = data
                    con = sqlite3.connect('db.db')
                    cursor = con.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON;")

                    sql = "INSERT INTO EmpleadoAsistencia (numEmpleado,fecha,movimiento) VALUES (:numEmpleado,:fecha,:mov)"
                    cursor.execute(sql,value)
                    con.commit()
                    con.close()
                except:
                    print("Error al marcar asistencia")
                else:
                    print(f"{mov} Marcada con exito.")
            else:
                print(f"Ya se ha registrado la {mov} del dia de hoy")
       

        

class Main:
    def __init__(self):
        while True:
            opcion = self.showMenu()
            if opcion == 1:
                self.marcarEntrada()#done

            elif opcion == 2:
                self.marcarSalida()#done
            elif opcion == 3:
                self.showEmpleados()#done
            elif opcion == 4:
                self.altaEmpleado()#done
            elif opcion == 5:
                self.modEmpleado()
            elif opcion == 6:
                self.exit()#done
            else:
                print("Opcion no vàlida intentalo de nuevo...")


    def showMenu(self):
        while True:
            print("1.-Marcar Entrada\n2.-Marcar Salida\n3.-Listar Empleados\n4.-Alta empleado\n5.-Modificar Empleado\n6.-Salir del programa\nElige una opcion")
            
            try:
                self.opcion = int(input())
            except:
                print("valor no valido...")
            else:
                return self.opcion

    def showEmpleados(self):
        Empleado.showEmpleados()
    def marcarEntrada(self):
        print("Marcar entrada")
        while True:
            try:
                empleado = int(input("Numero de Empleado:\n"))
            except:
                print("Valor no valido intentalo de nuevo.")
            else:
                Checador.check(empleado,"Entrada")
                break


    def marcarSalida(self):
        print("Marcar Salida")
        while True:
            try:
                empleado = int(input("Numero de Empleado:\n"))
            except:
                print("Valor no valido intentalo de nuevo.")
            else:
                Checador.check(empleado,"Salida")
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
        
        e.save()
        
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
        Empleado.updateEmpleado(data)

        
        

        
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
    
    




n = Main()


#no he implementado de forma correcta la interfaz de alta de empleado
#me quede actualizando los datos de un empleado



