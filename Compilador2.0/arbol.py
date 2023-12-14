class Nodo:
  def __init__(self, valor):
      self.valor = valor
      self.hijos = []

def construir_arbol(lista):
  raiz = Nodo(lista[0])
  actual = raiz
  pila = [actual]

  for elemento in lista[1:]:
      if elemento == '(':
          # Nuevo nivel en el árbol
          nuevo_nodo = Nodo(pila[-1].valor)
          pila[-1].hijos.append(nuevo_nodo)
          pila.append(nuevo_nodo)
      elif elemento == ')':
          # Volvemos al nivel anterior
          pila.pop()
      else:
          # Añadir hijo
          actual.hijos.append(Nodo(elemento))

  return raiz


def buscar_tupla(lista_tuplas, elemento):
  for tupla in lista_tuplas:
      if elemento in tupla:
          return tupla
  return None  # Si no se encuentra el elemento en ninguna tupla


def imprimir_arbol(nodo, tipos_datos, prefijo="", es_ultimo=True):
  tupla = buscar_tupla(tipos_datos ,nodo.valor)
  if tupla is not None:
      print(prefijo + ("└── " if es_ultimo else "├── ") + f"{tupla[0]}: {tupla[1]}")
  else:
      print(prefijo + ("└── " if es_ultimo else "├── ") + nodo.valor)


  prefijo += "    " if es_ultimo else "│   "

  for i, hijo in enumerate(nodo.hijos):
      imprimir_arbol(hijo, tipos_datos, prefijo, i == len(nodo.hijos) - 1)

#------------------------------------------------


nombres_funciones = ["crack", "mvp", "localiza", "saca", "wachea"]

def hallar_funciones(codigo, tipos_datos):
 #tipos datos: tupla
 #codigo: los matches del parser
 i = 0
 while i < len(codigo):
      if(codigo[i] in nombres_funciones):
          print("\n\nARBOL FUNCION---------- ")
          armar_arbol = []
          while codigo[i] != "newline":
              if(codigo[i] != ","):
                  armar_arbol.append(codigo[i])
              i=i+1
          print(armar_arbol)
          print("Devuelve un char\n")
          # Construir el árbol
          raiz_arbol = construir_arbol(armar_arbol)

          # Imprimir el árbol
          imprimir_arbol(raiz_arbol, tipos_datos)

      i=i+1


#----------------------------------------------------------------------------------------
# Listas proporcionadas

palabras_reservadas = ['str','char','==','newline','blob','(*','*)',',','cosmos','printify', 'fifi', 'notsame', 'less', 'bigger']


def crear_lista_para_arbol(lista_base, lista_reemplazo):
  lista_nueva = []
  i_reemplazo = 0
  i_base = 0
  while i_base < len(lista_base):
      if lista_base[i_base] in palabras_reservadas:
          lista_nueva.append(lista_base[i_base])
      elif lista_base[i_base] == 'id':
          while i_reemplazo < len(lista_reemplazo) and not lista_reemplazo[i_reemplazo].startswith('id'):
              i_reemplazo += 1
          if i_reemplazo < len(lista_reemplazo):
              lista_nueva.append(lista_reemplazo[i_reemplazo])
      elif lista_base[i_base] == 'cadena':
          while i_reemplazo < len(lista_reemplazo) and not lista_reemplazo[i_reemplazo].startswith('"'):
              i_reemplazo += 1
          if i_reemplazo < len(lista_reemplazo):
              lista_nueva.append(lista_reemplazo[i_reemplazo])
      elif lista_base[i_base] == 'booleano':
          while i_reemplazo < len(lista_reemplazo) and lista_reemplazo[i_reemplazo] not in ('true', 'false'):
              i_reemplazo += 1
          if i_reemplazo < len(lista_reemplazo):
              lista_nueva.append(lista_reemplazo[i_reemplazo])
      i_reemplazo += 1
      i_base += 1
  
  return lista_nueva
