import copy

INICIO = "INICIO"
VACIO = "ε"
FINAL = "$"
PRIMEROS = {}
SIGUIENTES = {}
PREDICCION = {}

NO_TERMINALS = ["A", "B", "C"]

grammar = {
    "A": [["B", "C"], ["ant", "A", "all"]],
    "B": [["big", "C"],["bus", "A", "boss"],["ε"]], 
    "C": [["cat"],["cow"]]
}


# reglasTemp = {
#     "A": [["A", ["A", "all"]],["B",["A", "boss"]] ]
#     "B":
#     "C": [["A",["C"]], ["B", ["C"]]]
# }

# NO_TERMINALS = ["S","A", "B", "C", "D"]

# grammar = {
#     "S": [["A", "uno", "B", "C"],["S", "dos"]],
#     "A": [["B", "C", "D"], ["A", "tres"], ["ε"]],
#     "B": [["D", "cuatro", "C", "tres"],["ε"]], 
#     "C": [["cinco", "D", "B"],["ε"]],
#     "D": [["seis"], ["ε"]]
# }

# NO_TERMINALS = ["S","Z","A","Y", "B", "C", "D"]

# grammar = {
#     "S": [["A", "uno", "B", "C", "Z"]],
#     "Z": [[ "dos", "Z"],["ε"]],
#     "A": [["B", "C", "D", "Y"],["Y"]],
#     "Y": [["tres", "Y"], ["ε"]],
#     "B": [["D", "cuatro", "C", "tres"],["ε"]], 
#     "C": [["cinco", "D", "B"],["ε"]],
#     "D": [["seis"], ["ε"]]
# }


#GET ALL PRIMEROS
#--TODO-- MIRAR CUESTION DE RECURION DEPTH

def getPRIMEROS(rule:list):
    if (rule == [VACIO]):
        return [VACIO]

    if rule[0] not in NO_TERMINALS:
        return [rule[0]]
    else: # rule[0] es no terminal
        
        A1 = []
        if rule[0] in PRIMEROS.keys():
            A1 = PRIMEROS[rule[0]]
        else:
            for rul in grammar[rule[0]]:
                A1.extend(getPRIMEROS(rul))
            
            PRIMEROS[rule[0]] = A1
        if VACIO in A1:
            if len(rule) == 1:
                return A1
            else:
                A1.remove(VACIO)
                if len(rule) > 1:
                    y = rule[1:]
                    x = getPRIMEROS(y)
                    A1.extend(x)
                    return A1
        return A1

for no_terminal in grammar.keys():
    allRules = grammar[no_terminal] # all rules of one no_terminal 
    PRIMEROS[no_terminal] = []
    for each_rule in allRules: 
        temp = getPRIMEROS(each_rule)
        if temp != None:
            if len(PRIMEROS[no_terminal]) == 0:
                PRIMEROS[no_terminal] =  temp
            else:
                PRIMEROS[no_terminal].extend(temp)

# GET SIGUIENTES
def getSIGUIENTES():
    SIGUIENTES["A"] = [FINAL]
    preSig = copy.deepcopy(SIGUIENTES)
    for no_terminal in grammar.keys():
        a = no_terminal
        for no_terminal2 in grammar.keys():
            b = no_terminal2
            for rule in grammar[b]:
                myLen = len(rule)
                for i in range(myLen):
                    if rule[i] == a:
                        if i == myLen - 1:
                            if a != b:
                                if a not in SIGUIENTES.keys():
                                    SIGUIENTES[a] = []
                                SIGUIENTES[a].extend(SIGUIENTES[b])
                        else:
                            if rule[i+1] not in NO_TERMINALS:
                                if a not in SIGUIENTES.keys():
                                    SIGUIENTES[a] = []
                                SIGUIENTES[a].extend([rule[i+1]])
                            else:
                                temp = copy.deepcopy(PRIMEROS[rule[i+1]])
                                if VACIO in temp:
                                    temp.remove(VACIO)
                                if a not in SIGUIENTES.keys():
                                    SIGUIENTES[a] = []
                                SIGUIENTES[a].extend(temp)
                                temp2 = getPRIMEROS(rule[i+1:])
                                if VACIO in temp2:
                                    SIGUIENTES[a].extend(SIGUIENTES[b])
                                    temp2.remove(VACIO)
                                SIGUIENTES[a].extend(temp2)

def getPREDICCION(rule, noterminal):
    x = set(getPRIMEROS(rule))
    if VACIO in x:
        x.remove(VACIO)
        return x.union(set(SIGUIENTES[noterminal]))
    else:
        return x

getSIGUIENTES()
print(PRIMEROS)
print(SIGUIENTES)

for no_terminal in grammar.keys():
    allRules = grammar[no_terminal] # all rules of one no_terminal 
    for each_rule in allRules: 
        PREDICCION["".join(each_rule)] = getPREDICCION(each_rule, no_terminal)

print(PREDICCION)