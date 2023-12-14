import string
import re

keywords = ["str", "blob","bubble", "fifi","newline", "int","cadena"]
tipos_bool = ["real","false"]
tiposVariables = ['str', 'cadena']
nom_funciones = ["cosmos", "printify"]
simbolos = ['(*', '*)', '{*', '*}', '+', ',', '==','-',';']
comp_ops = ['*=*', 'notsame', 'less', 'bigger']

def saberSiKeyword(dato):
    return dato in keywords

def saberSiFunciones(dato):
    return dato in nom_funciones


def saberSiBooleano(dato):
  return dato in tipos_bool

def saberSiSimbolo(dato):
    return dato in simbolos

def saberSiCompOp(dato):
    return dato in comp_ops

def scan(input_code):
    tokens = []
    line_number = 1

    for line in input_code.split('\n'):
        line = line.strip()
        index = 0

        while index < len(line):
            char = line[index]

            if char in string.whitespace:
                index += 1
                continue

            if char in string.ascii_letters:
                # Identificadores y palabras clave
                token = char
                index += 1

                while index < len(line) and line[index] in string.ascii_letters + string.digits:
                    token += line[index]
                    index += 1

                if saberSiKeyword(token):
                    tokens.append(('KEYWORD', token, line_number))
                elif saberSiFunciones(token):
                    tokens.append(('FUNCTION', token, line_number))
                elif saberSiBooleano(token):
                    tokens.append(('booleano', token, line_number))
                else:
                    tokens.append(('id', token, line_number))

            elif char.isdigit():
                # Números enteros
                token = char
                index += 1

                while index < len(line) and line[index].isdigit():
                    token += line[index]
                    index += 1

                tokens.append(('INT', token, line_number))

            elif char == '"':
                # Cadenas
                token = char
                index += 1

                while index < len(line) and line[index] != '"':
                    token += line[index]
                    index += 1

                if index < len(line):
                    token += line[index]  # Agregar comilla de cierre
                    index += 1

                tokens.append(('cadena', token, line_number))

            elif char in simbolos:
                # Símbolos
                tokens.append(('SYMBOL', char, line_number))
                index += 1

            elif char == '<':
                # Operadores de comparación
                token = char
                index += 1

                while index < len(line) and line[index] != '>':
                    token += line[index]
                    index += 1

                if index < len(line):
                    token += line[index]  # Agregar '>'
                    index += 1

                if saberSiCompOp(token):
                    tokens.append(('COMPOP', token, line_number))
                else:
                    tokens.append(('INVALID', token, line_number))

            else:
                # Carácter no válido
                tokens.append(('INVALID', char, line_number))
                index += 1

        line_number += 1

    return tokens

# Ejemplo de uso:
# input_code = """
# string id > cadena newline wachea ( id , ) newline
# """

def Scanner(direccion):

  input_code =""
  with open(direccion) as archivo:
    for linea in archivo:
        #print(linea)
        input_code += linea
        input_code += " newline "


  input_code = input_code.replace("\n", "")

  tokens = scan(input_code)

  retorno_Scanner = []
  retorno_Scanner_ParaTipos = []



  for token in tokens:
      print(f"Token: {token[0]}, Valor: {token[1]}, Línea: {token[2]}")
      if(token[0]=="KEYWORD"):
        retorno_Scanner.append(token[1])
        retorno_Scanner_ParaTipos.append(token[1])
      elif(token[0]=="id"):
        retorno_Scanner.append(token[0])
        retorno_Scanner_ParaTipos.append(token[1])
      elif(token[0]=="FUNCTION" or token[0]=="SYMBOL" or token[0]=="COMPOP"):
        retorno_Scanner.append(token[1])
        retorno_Scanner_ParaTipos.append(token[1])
      elif(token[0]=="cadena"):
        retorno_Scanner.append(token[0])
        retorno_Scanner_ParaTipos.append(token[1])
    #  elif(token[0]=="booleano"):
    #    retorno_Scanner.append(token[0])
    #    retorno_Scanner_ParaTipos.append(token[1])


  #print("\n\n")
  #print(retorno_Scanner)

  retorno_Scanner_texto = ""
  for dato in retorno_Scanner:
    retorno_Scanner_texto += dato + " "

  #print("\n\n")
  #print(retorno_Scanner_texto)

  print("\n\n")
  return retorno_Scanner_texto, retorno_Scanner_ParaTipos


#----------TABLA TIPOS
def hallarTipos(codigo):
  tipos = []

  for indice in range(len(codigo)):
    if(codigo[indice] in tiposVariables):

      tipos.append((codigo[indice],codigo[indice+1]))


  for elementos in tipos:
    print(elementos)

  return tipos