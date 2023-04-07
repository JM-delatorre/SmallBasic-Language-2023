import copy
import os

INICIO = "INICIO"
VACIO = "&"
FINAL = "$"
PRIMEROS = {}
SIGUIENTES = {}
PREDICCION = {}

grammar = {
    "INICIO": [["A"]],
    "A": [["B", "C"], ["ant", "A", "all"]],
    "B": [["big", "C"],["bus", "A", "boss"],["&"]], 
    "C": [["cat"],["cow"]]
}

NO_TERMINALS = grammar.keys()
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

# ALL FUNCTIONS
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

def getSIGUIENTES():
    SIGUIENTES["INICIO"] = [FINAL]
    preSig = copy.deepcopy(SIGUIENTES)
    for no_terminal in NO_TERMINALS:
        a = no_terminal
        for no_terminal2 in NO_TERMINALS:
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

# GET PRIMEROS
for no_terminal in NO_TERMINALS:
    allRules = grammar[no_terminal] # all rules of one no_terminal 
    PRIMEROS[no_terminal] = []
    for each_rule in allRules: 
        temp = getPRIMEROS(each_rule)
        if temp != None:
            if len(PRIMEROS[no_terminal]) == 0:
                PRIMEROS[no_terminal] =  temp
            else:
                PRIMEROS[no_terminal].extend(temp)

getSIGUIENTES()

#GET PREDICCION
PREDICCION = copy.deepcopy(grammar)
for no_terminal in NO_TERMINALS:
    allRules = grammar[no_terminal] # all rules of one no_terminal 
    for i in range(len(allRules)):
        PREDICCION[no_terminal][i] = getPREDICCION(allRules[i], no_terminal)


dir_path = os.path.dirname(os.path.realpath(__file__))
routeFile = dir_path + "/parser.py"
fileSyntactic = open(routeFile, "w")
fileSyntactic.write('# TODO ADD github \n')
fileSyntactic.write('# TODO ADD LEXIC \n\n')

fileSyntactic.write('''def errorSin(mylist):
    l = ",".join(mylist)
    print(f"[{token.row}:{token.col}] Error sintactico: Se encontro: {token.id}; se esperaba: {l}")\n
''')

fileSyntactic.write('''def emparejar(item):
    if token.id == item:
        ITERATOR += 1
        token = allmytokens[ITERATOR]
    else:
        errorSin([item])\n
''')

def createFunctions(): 
    allFunctions = ""
    for item in NO_TERMINALS:
        listaAEntregar = set()
        allFunctions += f"def {item}():\n"
        for iconjuntos in range(len(PREDICCION[item])): #itarate in sets
            listaAEntregar.update(PREDICCION[item][iconjuntos])
            if (iconjuntos == 0):
                allFunctions += f"\tif token.id in {PREDICCION[item][iconjuntos]}:\n"
            else:
                allFunctions += f"\telif token.id in {PREDICCION[item][iconjuntos]}:\n"
                
            actualRule = grammar[item][iconjuntos]            
            for itemRegla in actualRule:
                if itemRegla in NO_TERMINALS:
                    allFunctions += f"\t\t{itemRegla}()\n"
                else:
                    allFunctions += f"\t\temparejar(\"{itemRegla}\")\n"
        allFunctions += f"\telse:\n"
        allFunctions += f"\t\terrorSin({list(listaAEntregar)})\n"
        allFunctions += f"\tprint(\'esta es mi funcion {item}\')\n\n"
    return allFunctions

fileSyntactic.write(createFunctions())
fileSyntactic.close()

