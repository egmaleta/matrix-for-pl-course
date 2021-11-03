from matrix import Matrix

if __name__ == '__main__':
    
    # Se inicializan matrices de 2x2, 3x3:
    m0 = Matrix(3, 3)
    m1 = Matrix(3, 3, init_value=1)
    m2 = Matrix(2, 2, init_value=2)
    m3 = Matrix(2, 2, init_value=3)

    # Formas equivalentes de prints:
    print('m0:', m0, sep='\n')
    m1.print(name='m1')
    m2.print(name='m2')

    # Usos equivalentes de indizadores:
    m3.print(name='m3')
    m3[0,1] = 0
    m3._1_0 = 13
    setattr(m3, '_1_1', 9)
    m3.print(name='m3 (modificado)')

    # Se realizan operaciones entre las matrices:
    (m0 + m1*3).print('m0 + m1*3')
    (m2 * m3).print('m2 * m3')

    # Acceso a dimensión, vectores de columnas/filas:
    print(f'Dimensiones - m1:{m1._shape()}, m2:{m3._shape()}')
    m3.print('m3')
    print(f'\n- fila 2: {m3._row(1)}' + f'\n- columna 1: {m3._column(0)}')

    # Uso de iterador:
    print('- m3 en forma de iterador (lista):', [i for i in m3.__iter__()] , '\n')