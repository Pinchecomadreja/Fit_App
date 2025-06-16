class Usuario:
    def __init__(self, nombre, apellido, edad,password,naciemiento):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.__password = password
        self.naciemiento = naciemiento
    def get_paswword(self):
        return self.__password
