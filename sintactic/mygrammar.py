
grammar = {
    "INICIO": [["A"]],
    "A": [["B", "C"], ["ant", "A", "all"]],
    "B": [["big", "C"],["bus", "A", "boss"],["&"]], 
    "C": [["cat"],["cow"]]
}