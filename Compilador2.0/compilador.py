from scanner import *
from arbol import *


def first(rule):
    global gramatica, no_terminales, \
        terminales, gramatica_claves, firsts
    if len(rule) != 0 and (rule is not None):
        if rule[0] in terminales:
          #si en la regla escogida el primer elemento esun terminal, retornarlo
            return rule[0]
        elif rule[0] == '#':
            return '#'

    if len(rule) != 0:
        if rule[0] in list(gramatica_claves.keys()):
            fres = []
            rhs_rules = gramatica_claves[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            if '#' not in fres:
                return fres
            else:

                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList

                fres.append('#')
                return fres







def follow(nt):
    global start_symbol, gramatica, no_terminales, \
        terminales, gramatica_claves, firsts, follows

    solset = set()
    if nt == start_symbol:
        solset.add('$')

    for curNT in gramatica_claves:
        rhs = gramatica_claves[curNT]
        for subrule in rhs:
            if nt in subrule:

                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]

                    if len(subrule) != 0:
                        res = first(subrule)
                        if res is not None:
                          if '#' in res:
                              newList = []
                              res.remove('#')
                              ansNew = follow(curNT)
                              if ansNew != None:
                                  if type(ansNew) is list:
                                      newList = res + ansNew
                                  else:
                                      newList = res + [ansNew]
                              else:
                                  newList = res
                              res = newList
                    else:

                        if nt != curNT:
                            res = follow(curNT)
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)






def find_first():
    global gramatica, no_terminales, \
        terminales, gramatica_claves, firsts
    for rule in gramatica:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        gramatica_claves[k[0]] = multirhs

    print(f"\nRules: \n")
    for y in gramatica_claves:
        print(f"{y}->{gramatica_claves[y]}")

    for y in list(gramatica_claves.keys()):
        t = set()
        for sub in gramatica_claves.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        firsts[y] = t

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1







def find_follows():
    global start_symbol, gramatica, no_terminales,\
        terminales, gramatica_claves, firsts, follows
    for NT in gramatica_claves:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1





def table():
    import copy
    global gramatica_claves, firsts, follows, terminales
    #print("\nFirsts and Follow Result table\n")

    # find space size
    mx_len_first = 0
    mx_len_fol = 0
    for u in gramatica_claves:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2

    # print(f"{{:<{10}}} "
    #       f"{{:<{mx_len_first + 5}}} "
    #       f"{{:<{mx_len_fol + 5}}}"
    #       .format("Non-T", "FIRST", "FOLLOW"))
    # for u in gramatica_claves:
    #     print(f"{{:<{10}}} "
    #           f"{{:<{mx_len_first + 5}}} "
    #           f"{{:<{mx_len_fol + 5}}}"
    #           .format(u, str(firsts[u]), str(follows[u])))
    ntlist = list(gramatica_claves.keys())
    terminals = copy.deepcopy(terminales)
    terminals.append('$')

    mat = []
    for x in gramatica_claves:
        row = []
        for y in terminals:
            row.append('')
        mat.append(row)

    grammar_is_LL = True
    for lhs in gramatica_claves:
        rhs = gramatica_claves[lhs]
        for y in rhs:
            res = first(y)
            if res is not None:
              if '#' in res:
                  if type(res) == str:
                      firstFollow = []
                      fol_op = follows[lhs]
                      if fol_op is str:
                          firstFollow.append(fol_op)
                      else:
                          for u in fol_op:
                              firstFollow.append(u)
                      res = firstFollow
                  else:
                      res.remove('#')
                      res = list(res) +\
                            list(follows[lhs])

              ttemp = []
              if type(res) is str:
                  ttemp.append(res)
                  res = copy.deepcopy(ttemp)
              for c in res:
                  xnt = ntlist.index(lhs)
                  yt = terminals.index(c)
                  if mat[xnt][yt] == '':
                      mat[xnt][yt] = mat[xnt][yt] \
                                     + f"{lhs}->{' '.join(y)}"
                  else:
                      if f"{lhs}->{y}" in mat[xnt][yt]:
                          continue
                      else:
                          grammar_is_LL = False
                          mat[xnt][yt] = mat[xnt][yt] \
                                         + f",{lhs}->{' '.join(y)}"

    # print("\nGenerated parsing table:\n")
    # frmt = ",\t{:>12},\t" * len(terminals)
    # print(",\t",frmt.format(*terminals),",\t")

    # j = 0
    # for y in mat:
    #     frmt1 = ",\t{:>12},\t" * len(y)
    #     print(",\t",f"{ntlist[j]} {frmt1.format(*y)}",",\t")
    #     j += 1

    return (mat, grammar_is_LL, terminals)




def seguimiento_derivacion(parsing_table, grammarll1,
    table_term_list, input_string,
    term_userdef,start_symbol):
    seguimiento = []
    print(f"\nValidate String => {input_string}\n")

    stack = [start_symbol, '$']
    buffer = []

    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    print("\t{:>20}, \t{:>20}, \t{:>20},".
    format("Buffer", "Stack","Action"))

    while True:
      if stack == ['$'] and buffer == ['$']:
        print("\t{:>20}, \t{:>20}, \t{:>20},".format(' '.join(buffer),' '.join(stack),"Valid"))
        return "\nValid String!", seguimiento
      elif stack[0] not in term_userdef:
          x = list(gramatica_claves.keys()).index(stack[0])
          y = table_term_list.index(buffer[-1])
          if parsing_table[x][y] != '':
              entry = parsing_table[x][y]
              print("\t{:>20}, \t{:>20}, \t{:>25},".format(' '.join(buffer),' '.join(stack),
              f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
            #--------------------------------
              seguimiento.append(entry)
              lhs_rhs = entry.split("->")
              lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
              entryrhs = lhs_rhs[1].split()
              stack = entryrhs + stack[1:]
          else:
            # Handle error
            print("\n \t{:>20}, \t{:>20}, \t{:>20},".format(' '.join(buffer), ' '.join(stack), "Error: No cumple las reglas  \n") )
            while buffer[-1] != "newline":
              if buffer[-1] == "$":
                return 
              buffer = buffer[:-1]

            # Skip until "newline" is found
      else:
          if stack[0] == buffer[-1]:
              print("\t{:>20}, \t{:>20}, \t{:>20},".format(' '.join(buffer),' '.join(stack),f"Matched:{stack[0]}"))
              #--------------------------------
              seguimiento.append(stack[0])
              buffer = buffer[:-1]
              stack = stack[1:]
          else:
            # Handle error
            print("\n \t{:>20}, \t{:>20}, \t{:>20},".format(' '.join(buffer), ' '.join(stack), "Error: No cumple las reglas  \n") )

            error = -1
            if(buffer[-1] != "newline" or buffer[-1] != "id" or buffer[-1] != "cadena"):
              buffer = buffer[:-1]
              stack = stack[:-1]

            else:
              while buffer[-1] != "newline":
                  print(buffer[-1])
                  if buffer[-1] == "$":
                    return 
                  buffer = buffer[:-1]

            # Skip until "newline" is found


gramatica = ["S -> Program",
             "Program -> Statement newline Statementlist",
            "Statement -> blob (* Typevar ; Expr ; Expr *) {* newline Statementlist newline *} | fifi (* Expr *) {* newline Expr newline *} | Typevar | Funciones (* ListId *) | bubble (* Expr *) {* newline Statementlist newline *}",
            "Statementlist -> Statement newline Statementlist | #",
             "ListId -> id , ListId | #",
             "Typevar -> Type id == number Stringlist",
             "Type ->  str | char | int ",
            "Stringlist -> number Stringlist | #",
             "Expr -> Orexpr",
             "Orexpr -> Andexpr",
             "Andexpr -> Notexpr Andexprprime",
             "Andexprprime -> and Notexpr Andexprprime | #",
             "Notexpr -> Compexpr Notexprprime",
             "Notexprprime -> not Compexpr Notexprprime | #",
             "Compexpr -> Intexpr Compexprprime",
             "Compexprprime -> CompOp Intexpr Compexprprime | #",
             "Intexpr -> Factor Intexprprime",
             "Intexprprime -> + Factor Intexprprime | - term Intexprprime | #",
             "Factor -> - Factor | id | cadena | (* Expr *) | int",
             "Literal -> real | false",
             "CompOp -> *=* | notsame | less | bigger",
             "Funciones -> cosmos |  printify"
]



no_terminales = [
                'S',
                 "Start_Program",
                 "StatmentList",
                 "Statement",
                 "ListId",
                 "Typevar",
                 "Type",
                 "Stringlist",
                 "Expr",
                 "Orexpr",
                 "Andexpr",
                 "Andexprprime",
                 "Notexpr",
                 "Notexprprime",
                 "Compexpr",
                 "Compexprprime",
                 "Intexpr",
                 "Intexprprime",
                 "Factor",
                 "CompOp",
                 "Funciones"
                 ]
terminales = [
  ';',
  "newline",
  "blob",
  "bubble",
  "int",
  "(*",
  "*)",
  "{*",
  "*}",
  "fifi",
  "id",
  ",",
  "==",
  "cadena",
  "str",
  "and",
  "not",
  "+",
  "-",
  "real",
  "false",
  "notsame",
  "less",
  "bigger",
  "cosmos",
  "printify",

]



#--------------SCAN-----------

# input_codigo = """
#     string idNuevo > "hola" aaaaaaaaaaa newline wachea ( idNuevo , ) newline
# """



ejemplo_entrada, paraAnalizar = Scanner("inputCodigo.txt")
print(ejemplo_entrada)



#-----------------------FIN-SCANNER



#ejemplo_entrada="string id > cadena newline wachea ( id , ) newline"

gramatica_claves = {}
firsts = {}
follows = {}

#we find the first table of all the tokens
find_first()

start_symbol = list(gramatica_claves.keys())[0]

#we find the follow table of all the tokens
find_follows()

#we find the parsing table
(parsing_table, result, tabTerm) = table()

valido =""

paraElArbol = []
#we pass an example to verify if that example is accepted in our gramatic 
if ejemplo_entrada != None:
    valido, paraElArbol = seguimiento_derivacion(parsing_table, result,
                                              tabTerm, ejemplo_entrada,
                                              terminales,start_symbol)
    print(valido)
else:
    print("\nNo input String detected")


print("\n\nPara alamcenar el arbol-----------------\n")
print(paraElArbol)

print("\n\nAlmacenamiento de los tipos--------------\n")


if valido == "\nValid String!":
    tipos_datos = hallarTipos(paraAnalizar)
    print("\n\n")
    print(paraAnalizar)
    print("\n\n Se obtienen los datos para armar el arbol-----------------\n")

    nueva_lista = [elemento for elemento in paraElArbol if '->' not in elemento]
    print(nueva_lista)



    print("\nLista enlazada------------------------------------------------\n")
    # Imprimir la nueva lista
    lista_Final_arbol = crear_lista_para_arbol(nueva_lista, paraAnalizar)
    print(lista_Final_arbol)
    hallar_funciones(lista_Final_arbol, tipos_datos)