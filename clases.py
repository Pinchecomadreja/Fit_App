class Usuario:
    def __init__(self, nombre, apellido, edad,password,naciemiento):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.password = password
        self.naciemiento = naciemiento

    def mostrar_datos(self):
        print(f"Nombre: {self.nombre}"  )
        print(f"Apellido: {self.apellido}")
        print(f"Edad:{self.edad} ")
        print(f"Naciemiento: { self.naciemiento}")

    def a_dic(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'naciemiento': self.naciemiento,
            'password': self.password
        }
'''
    def get_paswword(self):
        return self.__password

    def set_password(self, password):
        self.__password = password
'''

