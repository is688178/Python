def suma():
    n1 = int(input("número 1: "))
    n2 = int(input("número 2: "))
    print(n1 + n2)
    print("Gracias por sumar")

try:
    suma()
except TypeError:
    print("Estas intentando concatenar tipos distintos")
except ValueError:
    print("Ese no es un número")
except:
    print("Algo no ha salido bien")
else:
    print("Hiciste todo bien")
finally:
    print("Eso fue todo")
