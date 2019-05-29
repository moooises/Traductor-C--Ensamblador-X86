import sys

tablaFunciones = {}

class manejadorFunciones():
  selectLista = 0

  def selector(self, id):
    if id in tablaFunciones:
      self.selectLista = id

  def crearTabla(self, id, list):
    global tablaFunciones
    tablaFunciones[id] = list

  def devolverTabla(self):
    global tablaFunciones
    print(tablaFunciones[self.selectLista])

if __name__ == '__main__':
  p = manejadorFunciones()
  lista = ['1','2']
  lista2 = ['3', '4']
  #p.crearTabla('main', lista)
  #p.crearTabla('funcion', lista2)
  #p.devolverTabla()

  if len(sys.argv) == 2:
    print("La cadena introducida tiene", sys.argv[1], "caracteres");
  else:
    print("Este programa necesita un parámetro");

  dir = './' + sys.argv[1]
  reader = open(dir, 'r')
  print(reader.read())