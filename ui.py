# Nombre: Jhon Jairo Corzo Calderon
# ID: 000427743

from cgitb import text
from statistics import median
from tkinter import *
from tkinter import messagebox
from turtle import up
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from scipy import stats
from statistics import mode,mean,median

#------------------Leer datos------------------
file = 'abalone.csv'
data = pd.read_csv(file)
data.columns = ["Sex", "Longitud", "Diametro", "Altura", "Peso entero", "Peso cascara", "Peso viseras", "Peso caparazon", "# de anillos"]

a = []

#------------------Variables------------------

root = Tk()
root.title("Abalones")
root.resizable(False, False)

frame = Frame(root)
frame.pack()


tGraph = IntVar()

longitud = IntVar()
diametro = IntVar()
altura = IntVar()
weight = IntVar()
weightC = IntVar()
weightV = IntVar()
weightCP = IntVar()
rings = IntVar()

alfa = StringVar()
dataMod = None

entrada = IntVar()
salida = IntVar()

"""
longitudE = IntVar()
diamE = IntVar()
heighE = IntVar()
weightE = IntVar()
weightCE = IntVar()
weightVE = IntVar()
weightCPE = IntVar()
ringsE = IntVar()

longitudS = IntVar()
diamS = IntVar()
heighS = IntVar()
weightS = IntVar()
weightCS = IntVar()
weightVS = IntVar()
weightCPS = IntVar()
ringsS = IntVar()
"""

#------------------Funciones botones------------------

# Graficar
def graficar(datos = None):
    if(datos == None):
        datos = data
    
    selected = choosedGraph()

    if(tGraph.get()==1): # Histograma
        if(len(selected)>2):
            messagebox.showinfo(message="Seleccionar solo una variable", title="Error")
            return ""
        try:
            plot.hist(x=datos[selected[0]])
        except:
            plot.hist(x=datos[selected[1]])
        plot.title(f"Histograma de {selected[0]}")
        plot.show()

    elif(tGraph.get()==2): #Boxplot
        if(len(selected)>2):
            messagebox.showinfo(message="Seleccionar solo una variable", title="Error")
            return ""

        try:
            plot.boxplot(x=datos[selected[0]])
        except:
            plot.boxplot(x=datos[selected[1]])

        plot.title(f"Boxplot de {selected[0]}")
        plot.show()

    elif(tGraph.get()==3): #Normalizacion
        if(len(selected)>2):
            messagebox.showinfo(message="Seleccionar solo una variable", title="Error")
            return ""

        graph = plot.figure()
        ax = graph.add_subplot(111)

        try:
            res = stats.probplot(datos[selected[0]], dist=stats.norm, sparams=(6,), plot=ax)
        except:
            res = stats.probplot(datos[selected[1]], dist=stats.norm, sparams=(6,), plot=ax)
        plot.title(f"Grafica de Normalizacion de {selected[0]}")
        plot.show()

    elif(tGraph.get()==4): #Dispercion
        if(len(selected)>4):
            messagebox.showinfo(message="Seleccionar solo 2 variables", title="Error")
            return ""
        elif(len(selected)<2):
            messagebox.showinfo(message="Seleccionar 2 variables", title="Error")
            return ""

        try:
            plot.scatter(datos[selected[0]], datos[selected[2]])
        except:
            plot.scatter(datos[selected[1]], datos[selected[3]])
            
        plot.title(f"Grafica de Dispercion de {selected[0]} y {selected[1]}")
        plot.show()
    else:
        messagebox.showinfo(message="Por favor selecione un tipo de grafica", title="Error")

# Eliminar atipicos
def eleminarAtipicos():
    nalfa = inputAlfa.get()
    
    try:
        maxlimits = []
        minlimits = []
        for i in range (1, len(data.columns)):
            q75 = np.quantile(data[data.columns[i]],.75)
            q25 = np.quantile(data[data.columns[i]],.25)
            intr_qr = q75 - q25
            maxlimits.append(q75 + (float(nalfa) * intr_qr))
            minlimits.append(q25 - (float(nalfa) * intr_qr))
        atipicos = None
        dataSin = []

        cont = 0

        for i in data.columns:
            if(i == "Sex"):
                continue    
            atipicos = (data[i] >= minlimits[cont]) & (data[i] <= maxlimits[cont])
            dataSin.append(data[i][atipicos])
            cont += 1

        graficar(dataSin)

    except ValueError:
        messagebox.showinfo(message="Por favor ingresar un numero para alfa.", title="Error")
        alfa.set("")


def analisis(datos = None):
    if(datos == None):
        datos = data
    
    selected = choosedGraph()

    media = []
    mediana = []
    moda = []
    skewnes = []
    kurtosis = []

    top = Toplevel()
    top.title('Analisis estadistico')
    cont = 0
    col = 0
    texto = None
    for i in range(0, len(selected),2):
        print(selected[i])
        #try:
        media.append(mean(datos[selected[i]]))
        mediana.append(median(datos[selected[i]]))
        moda.append(mode(datos[selected[i]]))
        skewnes.append(stats.skew(datos[selected[i]]))
        kurtosis.append(stats.kurtosis(datos[selected[i]]))
        texto = Label(top,text=f"---Analisis de {selected[i]}---\nMedia: {media[cont]}\nMediana: {mediana[cont]}\nModa: {moda[cont]}\nSimetria: {skewnes[cont]}\nCurtuosis: {kurtosis[cont]}", width=25)
        texto.config(borderwidth=2, relief="ridge")
        texto.grid(row=cont,column=col, padx= 10, pady=10)
        
        if(col == 2):
            cont+=1 
            col = 0
        else:
            col += 1
        
    
    


def choosedGraph():
    selected = []

    if(longitud.get()==1):
        selected.append("Longitud")
        selected.append(0)
    if(diametro.get()==1):
        selected.append("Diametro")
        selected.append(1)
    if(altura.get()==1):
        selected.append("Altura")
        selected.append(2)
    if(weight.get()==1):
        selected.append("Peso entero")
        selected.append(3)
    if(weightC.get()==1):
        selected.append("Peso cascara")
        selected.append(4)
    if(weightV.get()==1):
        selected.append("Peso viseras")
        selected.append(5)
    if(weightCP.get()==1):
        selected.append("Peso caparazon")
        selected.append(6)
    if(rings.get()==1):
        selected.append("# de anillos")
        selected.append(7)

    return selected

def regresion():
    messagebox.showinfo(message="Regresion :)",title="Regresion")
#------------------Interfaz------------------


Label(frame,text="Grafica con atipicos",width=20).grid(row=0,column=0,pady=10)


Label(frame,text="Tipo de grafico",width=20).grid(row=0,column=1)

Radiobutton(frame,text="Histograma",variable=tGraph,value=1).grid(row=1,column=1)
Radiobutton(frame,text="Boxplot",variable=tGraph,value=2).grid(row=1,column=2)
Radiobutton(frame,text="Normalizacion",variable=tGraph,value=3).grid(row=2,column=1)
Radiobutton(frame,text="Dispercion",variable=tGraph,value=4).grid(row=2,column=2)

Label(frame,text="Variables de entrada",width=20).grid(row=3,column=1,pady=10)

Checkbutton(frame,text="Longitud",variable=longitud, onvalue=1,offvalue=0, command=choosedGraph).grid(row=4, column=1,padx=50)
Checkbutton(frame,text="Diametro",variable=diametro, onvalue=1,offvalue=0, command=choosedGraph).grid(row=4, column=2,padx=50)
Checkbutton(frame,text="Altura",variable=altura, onvalue=1,offvalue=0, command=choosedGraph).grid(row=4, column=3,padx=50)
Checkbutton(frame,text="Peso entero",variable=weight, onvalue=1,offvalue=0, command=choosedGraph).grid(row=5, column=1)
Checkbutton(frame,text="Peso cascara",variable=weightC, onvalue=1,offvalue=0, command=choosedGraph).grid(row=5, column=2)
Checkbutton(frame,text="Peso viseras",variable=weightV, onvalue=1,offvalue=0, command=choosedGraph).grid(row=5, column=3)
Checkbutton(frame,text="Peso caparazon",variable=weightCP, onvalue=1,offvalue=0, command=choosedGraph).grid(row=6, column=1)
Checkbutton(frame,text="# de anillos",variable=rings, onvalue=1,offvalue=0, command=choosedGraph).grid(row=6, column=2)

#Boton graph
graph=Button(frame, text="Graficar datos originales", width=20, command=graficar).grid(row=6,column=3)

Label(frame,text="Grafica sin atipicos",width=20).grid(row=7,column=0,pady=10)
Label(frame,text="Valor del factor alfa para los atipicos",width=28).grid(row=7,column=1)
inputAlfa = Entry(frame,textvariable=alfa)
inputAlfa.grid(row=7,column=2)

#Boton delete
delete=Button(frame, text="Eliminar atipicos", width=20,command=eleminarAtipicos).grid(row=7,column=3)

#Boton estadisticas
estadistica=Button(frame, text="Analisis estadistico", width=20,command=analisis).grid(row=8,column=1)

Label(frame,text="Regresion",width=20).grid(row=9,column=0,pady=10)
Label(frame,text="Entrada",width=20).grid(row=9,column=1,pady=10)
Label(frame,text="Salida",width=20).grid(row=9,column=2,pady=10)
"""
Checkbutton(frame,text="Longitud",variable=longitudE, onvalue=1,offvalue=0).grid(row=9, column=1)
Checkbutton(frame,text="Diametro",variable=diamE, onvalue=1,offvalue=0).grid(row=10, column=1)
Checkbutton(frame,text="Altura",variable=heighE, onvalue=1,offvalue=0).grid(row=11, column=1)
Checkbutton(frame,text="Peso entero",variable=weightE, onvalue=1,offvalue=0).grid(row=12, column=1)
Checkbutton(frame,text="Peso cascara",variable=weightCE, onvalue=1,offvalue=0).grid(row=13, column=1)
Checkbutton(frame,text="Peso viseras",variable=weightVE, onvalue=1,offvalue=0).grid(row=14, column=1)
Checkbutton(frame,text="Peso caparazon",variable=weightCPE, onvalue=1,offvalue=0).grid(row=15, column=1)
Checkbutton(frame,text="# de anillos",variable=ringsE, onvalue=1,offvalue=0).grid(row=16, column=1)


Checkbutton(frame,text="Longitud",variable=longitudS, onvalue=1,offvalue=0).grid(row=9, column=2)
Checkbutton(frame,text="Diametro",variable=diamS, onvalue=1,offvalue=0).grid(row=10, column=2)
Checkbutton(frame,text="Altura",variable=heighS, onvalue=1,offvalue=0).grid(row=11, column=2)
Checkbutton(frame,text="Peso entero",variable=weightS, onvalue=1,offvalue=0).grid(row=12, column=2)
Checkbutton(frame,text="Peso cascara",variable=weightCS, onvalue=1,offvalue=0).grid(row=13, column=2)
Checkbutton(frame,text="Peso viseras",variable=weightVS, onvalue=1,offvalue=0).grid(row=14, column=2)
Checkbutton(frame,text="Peso caparazon",variable=weightCPS, onvalue=1,offvalue=0).grid(row=15, column=2)
Checkbutton(frame,text="# de anillos",variable=ringsS, onvalue=1,offvalue=0).grid(row=16, column=2)
"""
Radiobutton(frame,text="Longitud",variable=entrada,value=1).grid(row=10, column=1)
Radiobutton(frame,text="Diametro",variable=entrada,value=2).grid(row=11, column=1)
Radiobutton(frame,text="Altura",variable=entrada,value=3).grid(row=12, column=1)
Radiobutton(frame,text="Peso entero",variable=entrada,value=4).grid(row=13, column=1)
Radiobutton(frame,text="Peso cascara",variable=entrada,value=5).grid(row=14, column=1)
Radiobutton(frame,text="Peso viseras",variable=entrada,value=6).grid(row=15, column=1)
Radiobutton(frame,text="Peso caparazon",variable=entrada,value=7).grid(row=16, column=1)
Radiobutton(frame,text="# de anillos",variable=entrada,value=8).grid(row=17, column=1)

Radiobutton(frame,text="Longitud",variable=salida,value=1).grid(row=10, column=2)
Radiobutton(frame,text="Diametro",variable=salida,value=2).grid(row=11, column=2)
Radiobutton(frame,text="Altura",variable=salida,value=3).grid(row=12, column=2)
Radiobutton(frame,text="Peso entero",variable=salida,value=4).grid(row=13, column=2)
Radiobutton(frame,text="Peso cascara",variable=salida,value=5).grid(row=14, column=2)
Radiobutton(frame,text="Peso viseras",variable=salida,value=6).grid(row=15, column=2)
Radiobutton(frame,text="Peso caparazon",variable=salida,value=7).grid(row=16, column=2)
Radiobutton(frame,text="# de anillos",variable=salida,value=8).grid(row=17, column=2)

regresion = Button(frame, text="Obtener regresion", width=20,command=regresion).grid(row=18,column=1)


root.mainloop()


