import re


class Matrix:
    def __init__(self, rows, columns, init_value=0):
        assert isinstance(rows, int) and rows > 0, \
            "'rows' must be an integer greater than 0"
        assert isinstance(columns, int) and columns > 0, \
            "'columns' must be an integer greater than 0"
        
        self._rows = rows
        self._cols = columns
        self._core = [[init_value for _ in range(columns)] for _ in range(rows)]


    def __getitem__(self, key):
        assert isinstance(key, tuple) and len(key) == 2 and \
            isinstance(key[0], int) and 0 <= key[0] < self._rows and \
            isinstance(key[1], int) and 0 <= key[1] < self._cols, \
            "'index' operation went wrong"
        
        return self._core[key[0]][key[1]]

    def __setitem__(self, key, value):
        assert isinstance(key, tuple) and len(key) == 2 and \
            isinstance(key[0], int) and 0 <= key[0] < self._rows and \
            isinstance(key[1], int) and 0 <= key[1] < self._cols, \
            "'index' operation went wrong"
        
        self._core[key[0]][key[1]] = value


    def __getattr__(self, name):
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
        if re.fullmatch(r'_\d+_\d+', name):
            i_str, j_str = name.split('_')[1:]
            i, j = int(i_str), int(j_str)

            self[i, j] = value
        else:
            super().__setattr__(name, value)


    def _shape(self):
        return self._rows, self._cols

    def __add__(self, other):
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
        return [x for x in self._core[index]]

    def _column(self, index):
        return [r[index] for r in self._core]

    def __mul__(self, other):
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
