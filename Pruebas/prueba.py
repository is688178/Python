import unittest
import cambia_texto


class ProbarCambiaTexto(unittest.TestCase):

    """El nombre de la función debe comenzar con test"""
    def test_mayusculas(self):
        palabra = 'buen dia'
        resultado = cambia_texto.todo_mayusculas(palabra)
        self.assertEquals(resultado, 'BUEN DIA')


if __name__ == '__main__':
    unittest.main()
