class Token():
    def __init__(self,id:str,row:int,col:int,lex:str = None) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.lex = lex

    def __repr__(self) -> str:
        actualLex = (', ' + self.lex) if self.lex != None else ''
        toPrint = f'<{self.id}{actualLex}, {self.row}, {self.col}>' 
        return toPrint

perro = Token('Mi ID',4,5, "Hola")
print(perro)