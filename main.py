from os import remove
from pandas.io.html import read_html
import csv
from tkinter import ttk
from tkinter import *
import sqlite3
import pandas as pd

# Desde esta linea y hasta la linea 68, es una prueba de hacerlo gui.


# class Comparador:

#     db_name = 'database.db'


#     def __init__(self,window):
#         self.wind = window
#         self.wind.title('Comparador de planes de estudio')
        

#         # Creating a Frame Container
#         frame = LabelFrame(self.wind, text='Ingresa la url de los planes de estudio:')
#         frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

#         # URL1 Input
#         Label(frame, text = 'URL 1: ',).grid(row = 1, column = 0)
#         self.url1 = Entry(frame)
#         self.url1.focus()
#         self.url1.grid(row = 1, column = 1)
#         self.make_csv

#         # URL2 Input
#         Label(frame,text = 'URL 2: ').grid(row = 2, column = 0)
#         self.url2 = Entry(frame)
#         self.url2.grid(row = 2, column = 1)

#         # Boton llamar a paginas
#         ttk.Button(frame,text = 'Comparar planes de estudio').grid(row = 3, columnspan = 2, sticky = W + E)

# #         # Table
#         self.tree = ttk.Treeview(height = 20, columns = 2)
#         self.tree.grid(row = 4, column = 0, columnspan = 2)
#         self.tree.heading('#0',text = 'Codigo', anchor = CENTER)
#         self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        

#     def run_query(self, query, parameters = ()):
#         with sqlite3.connect(self.db_name) as conn:
#             cursor = conn.cursor()
#             result = cursor.execute(query, parameters)
#             conn.commit()
#         return result
#     def make_csv(self):
#         table1 = read_html(self.url1, attrs={"class":"table-bordered"})
#         file_name_table1 = './tabla_1.csv'
#         table1[0].to_csv(file_name_table1, sep= '\t')
#         with open('tabla_1.csv', encoding='utf8',newline='') as tabla_1:
#             spamreader = csv.reader(csvfile, delimiter=",", quotechar = ",", quoting = csv.QUOTE_MINIMAL)
#             for row in spamreder:
#                 print(", ".join(row))



# if __name__ == '__main__':
#     window = Tk()
#     application = Comparador(window)
#     window.mainloop()









# print('Inserte la URL de la primer pagina')

URL1 = 'https://www.info.unlp.edu.ar/carreras-gradoarticulo/plan-2015-analista-programador-universitario-nuevo/'

URL2 = 'https://www.info.unlp.edu.ar/carreras-gradoarticulo/2015linuevo/'

def hacerArchivoCsv(urlDeTabla, nombreDelArchivo):
    tabla1 = read_html(urlDeTabla,attrs={"class":"table-bordered"})
    if '.csv' not in nombreDelArchivo:
        nombreDelArchivo = nombreDelArchivo + ".csv"
    # Escribiendo como parametro (table_1, sep="\") lo que hace es determinar la diferencia entre cada celda con un tab.
    tabla1[0].to_csv(nombreDelArchivo)

def removerColumnas(nombreTabla,nombreOutput,cols_to_remove):
    if '.csv' not in nombreTabla:
        nombreTabla += '.csv'
    if '.csv' not in nombreOutput:
        nombreOutput += '.csv'
    row_count = 0
    with open(nombreTabla, 'r') as source:
        reader = csv.reader(source)
        with open(nombreOutput,'w',newline="") as result:
            writer = csv.writer(result)
            for row in reader:
                row_count +=1
                print('\r{0}'.format(row_count), end="")
                for col_index in cols_to_remove:
                    del row[col_index]
                writer.writerow(row)

def diferencia(primerTabla,segundaTabla, valorDeDiferencia):
    if '.csv' not in primerTabla:
        primerTabla+= '.csv'
    if '.csv' not in segundaTabla:
        segundaTabla += '.csv'
    with open(primerTabla, 'r') as t1, open (segundaTabla, 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()
    with open('diferencias.csv', 'w') as outfile:
        if(valorDeDiferencia == '2' or valorDeDiferencia == '3'):
            for line in fileone:
                if line not in filetwo:
                    outfile.write(line)
        if (valorDeDiferencia == '1' or valorDeDiferencia == '3'):
            for line in filetwo:
                if line not in fileone:
                    outfile.write(line)
    if(valorDeDiferencia == 'exit()'):
        remove('diferencias.csv')

def hacerTablas(tabla,url):
    hacerArchivoCsv(url,tabla)
    removerColumnas(tabla,'output',[1,2,3])
    remove(tabla)
    removerColumnas('output','segundoOutput',[2])
    remove('output.csv')
    removerColumnas('segundoOutput', 'tercerOutput', [0])
    remove('segundoOutput.csv')
    #El chorizo de acá abajo saca caracteres como "  y (, que quede llano el nombre de la materia.
    with open('tercerOutput.csv','r') as tercerOutput:
        fileone = tercerOutput.readlines()
    with open(tabla,'w', newline= "") as tabla:
        writer = csv.writer(tabla)
        for line in fileone:
            if (line.find(" (") != -1):
                line = line.split(" (")
                line = line[0] + '\n'
            if (line.find('"') != -1):
                line = line.split('"')
                line = line[1] + '\n'     
            tabla.write(line)
    remove('tercerOutput.csv')

def eliminarTablas(nombreDelArchivo):
    remove(nombreDelArchivo)


hacerTablas('primerTabla.csv', URL1)
hacerTablas('segundaTabla.csv', URL2)

print('\nIngresa el valor de la diferencia entre materias que desea obtener(ingrese el valor que esta entre parentesis de lo que quiera): ')
print('Diferencia del segundo plan de estudios con respecto del primero(1)')
print('Diferencia del primer plan de estudios con respecto del segundo(2)')
print('Diferencia total entre los dos planes de estudio(3)')
valorDeDiferencia = input('Ingrese ahora:')



while ( valorDeDiferencia != '1' and valorDeDiferencia != '2' and valorDeDiferencia != '3' ):
    print('Valor erroneo. Por favor intentalo de nuevo.')
    valorDeDiferencia = input()    
    if (valorDeDiferencia == 'exit()'):
        break
diferencia('primerTabla.csv','segundaTabla.csv',valorDeDiferencia)





# EN CASO DE QUE LA URL INGRESADA, NO SEA UNA URL PROPIAMENTE DICHA O ESTE MAL ESCRITA
# USAR UN TRY CATCH.




