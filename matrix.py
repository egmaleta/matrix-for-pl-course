class Matrix:
    def __init__(self, rows, columns):
        assert isinstance(rows, int) and rows > 0, \
            "'rows' must be an integer greater than 0"
        assert isinstance(columns, int) and columns > 0, \
            "'columns' must be an integer greater than 0"
        
        self._rows = rows
        self._cols = columns
        self._core = [[0 for _ in range(columns)] for _ in range(rows)]


    def _row(self, index):
        return (x for x in self._core[index])


    def _column(self, index):
        return (r[index] for r in self._core)
