from os import remove
from pandas.io.html import read_html
import csv
import pandas as pd
import bs4
from urllib.request import urlopen


def nombreDeLaCarrera(url):
    htmlf = urlopen(url)
    subhtml = htmlf.read()
    soup = bs4.BeautifulSoup(subhtml,features="lxml")
    nombre = soup.find('h5',attrs={'class':'titulo-pag'}).get_text()    
    return nombre

def hacerArchivoCsv(urlDeTabla, nombreDelArchivo):
    #Read_html lee  el link en el primer parametro y busca atributos en el segundo.
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

def diferencia(primerTabla,segundaTabla,nombreCarrera1,nombreCarrera2,resultado):

    with open(primerTabla, 'r',encoding="utf8") as t1, open (segundaTabla, 'r',encoding="utf8") as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()
    with open('diferencias.csv', 'w',encoding="utf8",) as outfile:
        if(resultado == '1' or resultado == '3'):
            outfile.write('--------- COINCIDEN -------------\n')
        if(resultado == '2' or resultado =='3'):
            print('--------- COINCIDEN -------------\n')
        for line in fileone:
            if line in filetwo:
                if (resultado == '1' or resultado == '3'):
                    if(resultado == '3'):
                        print(line)
                    outfile.write(line)
                else:
                    print(line)
        if(resultado == '1' or resultado == '3'):
            outfile.write('\n--------- NO COINCIDEN (Pertenecen a {0}) -------------\n'.format(carrera1))
        if(resultado == '2' or resultado =='3'):
            print('\n--------- NO COINCIDEN (Pertenecen a {0}) -------------\n'.format(carrera1))   

        for line in fileone:
            if line not in filetwo:
                if(resultado == '1' or resultado == '3'):
                    if (resultado == '3'):
                        print(line)
                    outfile.write(line)

        if(resultado == '1' or resultado == '3'):
            outfile.write('\n--------- NO COINCIDEN (Pertenecen a {0}) -------------\n'.format(carrera2))
        if(resultado == '2' or resultado =='3'):
            print('\n--------- NO COINCIDEN (Pertenecen a {0}) -------------\n'.format(carrera2))   
        #Lo de abajo itera las materias que no estan en el primer plan de estudios, ya iterado
        
        for line in filetwo:
            if line not in fileone:
                if (resultado == '1' or resultado == '3'):
                    if (resultado == '3'):
                        print(line)
                    outfile.write(line)
                else:
                    print(line)

    eliminarTablas(primerTabla)
    eliminarTablas(segundaTabla)
    

def hacerTablas(tabla,url):
    hacerArchivoCsv(url,tabla)
    removerColumnas(tabla,'output',[1,2,3])
    eliminarTablas(tabla)
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
            if '1' in line:
                if line == 1:
                    print(line)
            if 'Nombre' in line:
                continue
            if (line.find(" (") != -1):
                line = line.split(" (")
                line = line[0] + '\n'
            if (line.find('"') != -1):
                line = line.split('"')
                line = line[1] + '\n'     
            tabla.write(line)
    remove('tercerOutput.csv')
def eliminarTablas(nombreDelArchivo):
    if '.csv' not in nombreDelArchivo:
        nombreDelArchivo += '.csv'
    remove(nombreDelArchivo)
def parsearATexto(tabla):
    with open('diferencias.csv', 'r',encoding="utf8") as tabla:
        fileone = tabla.readlines()
    with open('diferenciasTexto.txt','w',encoding="utf8") as texto:
        for line in fileone:
            if 'Nombre' or '1' in line:
                continue
            texto.write(line)

print('Por favor, ingrese el link del primer plan de estudios: ')

URL1 = 'https://www.info.unlp.edu.ar/carreras-gradoarticulo/2015linuevo/'

print('Por favor, ingrese el link del segundo plan de estudios: ')
URL2 = 'https://www.info.unlp.edu.ar/carreras-gradoarticulo/plan-2015-licenciatura-en-sistema/'



hacerTablas('primeraTabla.csv', URL1)
hacerTablas('segundaTabla.csv', URL2)

carrera1 = nombreDeLaCarrera(URL1)
carrera2 = nombreDeLaCarrera(URL2)


print('\nComo desea obtener el resultado? Archivo csv, mostrar en linea de comandos, las 2 [1,2,3]:')
resultado = input()
while(resultado != '1' and resultado != '2' and resultado != '3' and resultado != 'exit'):
    print('Valor erroneo. Por favor, vuelva a ingresar:')
    resultado = input()
    if(resultado == 'exit'):
        break

if(resultado != 'exit'):
    diferencia('primeraTabla.csv','segundaTabla.csv',carrera1,carrera2,resultado)
    parsearATexto('diferencias.csv')
else:
    eliminarTablas('primeraTabla.csv')
    eliminarTablas('segundaTabla.csv')







# EN CASO DE QUE LA URL INGRESADA, NO SEA UNA URL PROPIAMENTE DICHA O ESTE MAL ESCRITA
# USAR UN TRY CATCH.




