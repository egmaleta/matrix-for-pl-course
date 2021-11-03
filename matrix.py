import re


class Matrix:
    def __init__(self, rows, columns, init_value=0):
        """
        Se inicializa la matriz con `rows` cantidad de filas y `columns` cantidad
        de columnas, con todos sus valores inicializados en `init_value`.
        """
        assert isinstance(rows, int) and rows > 0, \
            "'rows' must be an integer greater than 0"
        assert isinstance(columns, int) and columns > 0, \
            "'columns' must be an integer greater than 0"
        
        self._rows = rows
        self._cols = columns
        self._core = [[init_value for _ in range(columns)] for _ in range(rows)]

    def __getitem__(self, key):
        """
        Definicion del operador [] para indizar y obtener un valor.
        """
        assert isinstance(key, tuple) and len(key) == 2 and \
            isinstance(key[0], int) and 0 <= key[0] < self._rows and \
            isinstance(key[1], int) and 0 <= key[1] < self._cols, \
            "'index' operation went wrong"
        
        return self._core[key[0]][key[1]]

    def __setitem__(self, key, value):
        """
        Definicion del operador [] para indizar y establecer un valor.
        """
        assert isinstance(key, tuple) and len(key) == 2 and \
            isinstance(key[0], int) and 0 <= key[0] < self._rows and \
            isinstance(key[1], int) and 0 <= key[1] < self._cols, \
            "'index' operation went wrong"
        
        self._core[key[0]][key[1]] = value

    def __getattr__(self, name):
        """
        Acceso dinámico a los atributos, incluyendo la posibilidad de:
            - indizar dinámicamente con el formato ._i_j o .getattr('_i_j')
            - convertir la matriz de tipo A a una matriz de tipo B con el formato .as_B
        """
        if re.fullmatch(r'_\d+_\d+', name):
            i_str, j_str = name.split('_')[1:]
            i, j = int(i_str), int(j_str)

            return self[i, j]
        
        if re.fullmatch(r'as_[a-zA-Z]+', name):
            t_str = name[3:]
            t = eval(t_str)

            res = Matrix(self._rows, self._cols)
            for i in range(self._rows):
                for j in range(self._cols):
                    res[i, j] = t(self[i, j])
            
            return res

    def __setattr__(self, name, value):
        """
        Acceso y modificación dinámicos a los atributos, incluyendo la posibilidad de 
        indizar y settear dinámicamente con el formato ._i_j o .getattr('_i_j')
        """
        if re.fullmatch(r'_\d+_\d+', name):
            i_str, j_str = name.split('_')[1:]
            i, j = int(i_str), int(j_str)

            self[i, j] = value
        else:
            super().__setattr__(name, value)

    def _shape(self):
        """
        Sea una matriz m de dimensión NxM, m._shape() devuelve la tupla (N, M)
        """
        return self._rows, self._cols

    def __add__(self, other):
        """
        Adición entre dos matrices del mismo tipo y misma dimensión.
        """
        assert isinstance(other, Matrix), \
            f"'add' operation not supported with '{type(other).__name__}' type"
        assert self._shape() == other._shape(), \
            "'add' operation not supported for matrixes with different shape"
        
        res = Matrix(self._rows, self._cols)
        for i in range(self._rows):
            for j in range(self._cols):
                res[i, j] = self[i, j] + other[i, j]
        
        return res

    def _row(self, index):
        """
        Devuelve el vector (lista) correspondiente a la fila i-ésima.
        """
        return [x for x in self._core[index]]

    def _column(self, index):
        """
        Devuelve el vector (lista) correspondiente a la columna i-ésima.
        """
        return [r[index] for r in self._core]

    def __mul__(self, other):
        """
        Multiplicación entre dos matrices del mismo tipo y misma dimensión
        ó entre una matriz y un entero/float.
        """
        if isinstance(other, Matrix):
            assert self._cols == other._rows, \
                """'mul' operation not supported: the number of columns of 
                left-side matrix doesn't match with the number of rows of the 
                right-side matrix"""
            
            res = Matrix(self._rows, other._cols)
            for i in range(self._rows):
                r = self._row(i)
                
                for j in range(other._cols):
                    c = other._column(j)

                    res[i, j] = sum([rv*cv for rv, cv in zip(r, c)])
            
            return res

        if isinstance(other, (int, float)):
            res = Matrix(self._rows, self._cols)
            for i in range(self._rows):
                for j in range(self._cols):
                    res[i, j] = self[i, j] * other
            
            return res
        
        raise AssertionError(
            f"'mul' operation not supported with '{type(other).__name__}' type"
        )

    def __iter__(self):
        """
        Definición de un iterador para las matrices, aprovechando la semántica de yield.
        """
        for i in range(self._rows):
            for j in range(self._cols):
                yield self[i, j]

    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self._core)

    def print(self, name=''):
        name = f'{name}:\n' if name else ''
        print(f'\n{name}{str(self)}')