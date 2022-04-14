from numpy.core.fromnumeric import transpose
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
import PySimpleGUI as sg
import os
os.system("clear")


def utext(s):
    return '\033[4m'+s+'\033[0m'

def btext(s):
    return '\033[1m'+s+'\033[0m'

datos1 = [[1,0,0,1,0,1,0,0],
            [0,1,1,0,0,1,0,0],
            [1,0,0,1,0,0,1,1],
            [0,0,1,0,0,1,0,0],
            [0,0,0,1,1,0,0,1]]

datos2 = [[0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0]]

def dca_mejorado(df):
    def sumarFilas(df):
        columnas = list(df.columns)
        filas = list(df.transpose().columns)
        df["SumaF"]=0
        for j in range(len(filas)-1):
            for i in range(len(columnas)-1):
                df["SumaF"][filas[j]] += df[columnas[i]][filas[j]] * (2**(len(columnas)-2-i))
        return df
            
    def sumarColumnas(df):
        columnas = list(df.columns)
        filas = list(df.transpose().columns)
        df.loc["SumaC"] = 0
        for i in range(len(columnas)-1):
            for j in range(len(filas)-1):
                df[columnas[i]]["SumaC"] += df[columnas[i]][filas[j]] * (2**(len(filas)-2-j)) 
        return df

    def ordenarFilas(df):
        df["SumaF"]["SumaC"]=-1
        df = df.sort_values(by=["SumaF"],ascending=False)
        df = sumarColumnas(df)
        return df

    def ordenarColumnas(df):
        df["SumaF"]["SumaC"]=-1
        df = df.sort_values(by=["SumaC"],ascending=False,axis=1)
        df["SumaF"]["SumaC"]=0
        df = sumarFilas(df)
        return df

    def paso1(df):
        df = sumarFilas(df)
        df = sumarColumnas(df)
        return df

    def paso2(df):
        columnas = list(df.columns.values) 
        filas = list(df.index)
        while list(ordenarColumnas(df).columns.values)!=columnas or list(ordenarFilas(df).index)!=filas:
            df = ordenarFilas(df)
            df = ordenarColumnas(df)
            columnas = list(df.columns.values) 
            filas = list(df.index)
        df = df.drop("SumaF",axis = 1)
        df = df.drop("SumaC",axis = 0)
        return df

    def graficarFINAL(df,dfS,tiempo):
        try:
            df = df.drop("SumaF",axis = 1)
            df = df.drop("SumaC",axis = 0)
        except:
            pass

        df.replace(0, np.nan, inplace=True)
        dfS.replace(0, np.nan, inplace=True)

        fig,ax = plt.subplots(1,2,figsize=(9,5))
        fig.canvas.set_window_title('DCA mejorado | Pablo Gutiérrez')
        cdf = list(df.columns.values)
        fdf = list(df.index)
        ax[0].set_title("Matriz inicial")
        ax[0].imshow(df,cmap="RdBu",interpolation='nearest')
        ax[0].set_xticklabels(cdf)
        ax[0].set_yticklabels(fdf)
        ax[0].set_xticks([(i) for i in range(len(df.columns.values))])
        ax[0].set_yticks([(i) for i in range(len(np.array(df.index)))])

        cdfS = list(dfS.columns.values)
        fdfS = list(dfS.index)
        ax[1].set_title(f"Matriz Final, tiempo = {tiempo}[s]")
        ax[1].imshow(dfS,cmap="RdBu",interpolation='nearest')
        ax[1].set_xticklabels(cdfS)
        ax[1].set_yticklabels(fdfS)
        ax[1].set_xticks([(i) for i in range(len(dfS.columns.values))])
        ax[1].set_yticks([(i) for i in range(len(np.array(dfS.index)))])

        #signaturebar(fig,"Pablo Gutiérrez")
        plt.show()
    
    inicial = time()
    dfn = paso1(df)
    dfn = paso2(dfn)
    final = time()
    tiempo = final-inicial
    graficarFINAL(df,dfn,float("%.3f"%tiempo))

def dca(df):
    def paso1(df):
        df["SumaF"]=df.sum(axis=1)
        df.loc["SumaC"] = df.sum(axis=0)

        df["SumaF"]["SumaC"]=-1
        df = df.sort_values(by=["SumaF"],ascending=False)
        df["SumaF"]["SumaC"]=1000
        df = df.sort_values(by=["SumaC"],ascending=True,axis=1)
        df["SumaF"]["SumaC"]=0

        df = df.drop("SumaF",axis = 1)
        df = df.drop("SumaC",axis = 0)

        return df

    def ordenar_columnas(df):
        filas = list(df.index)
        columnas = list(df.columns.values)
        new = pd.DataFrame(index = filas)
        copiadas = []
        for i in range(len(filas)):
            for j in range(len(columnas)):
                if df[columnas[j]][filas[i]] == 1 and (columnas[j] not in copiadas):
                    new[columnas[j]] = df[columnas[j]]
                    copiadas.append(columnas[j])     
        return new

    def ordenar_filas(df):
        new =  df.transpose()
        new = ordenar_columnas(new)
        new = new.transpose()
        return new

    def graficarFINAL(df,dfS,tiempo):
        try:
            df.replace(0, np.nan, inplace=True)
            dfS.replace(0, np.nan, inplace=True)
        except:
            pass
        
        fig,ax = plt.subplots(1,2,figsize=(9,5))
        fig.canvas.set_window_title('DCA | Pablo Gutiérrez')
        cdf = list(df.columns.values)
        fdf = list(df.index)
        ax[0].set_title("Matriz inicial")
        ax[0].imshow(df,cmap="RdBu",interpolation='nearest')
        ax[0].set_xticklabels(cdf)
        ax[0].set_yticklabels(fdf)
        ax[0].set_xticks([(i) for i in range(len(df.columns.values))])
        ax[0].set_yticks([(i) for i in range(len(np.array(df.index)))])

        cdfS = list(dfS.columns.values)
        fdfS = list(dfS.index)
        ax[1].set_title(f"Matriz Final, tiempo = {tiempo}[s]")
        ax[1].imshow(dfS,cmap="RdBu",interpolation='nearest')
        ax[1].set_xticklabels(cdfS)
        ax[1].set_yticklabels(fdfS)
        ax[1].set_xticks([(i) for i in range(len(dfS.columns.values))])
        ax[1].set_yticks([(i) for i in range(len(np.array(dfS.index)))])

        #signaturebar(fig,"Pablo Gutiérrez")
        #plt.text(0.4, 0.05, "Pablo Gutiérrez", fontsize=14, transform=plt.gcf().transFigure)
        #plt.savefig(f"/Users/pablo/OneDrive - Universidad de Concepción/Material UdeC/Cuarto año/Septimo semestre/Diseños de sistemas de producción/Python/DCA/DCA_RESULT/dca_{i}.png")
        plt.show()

    inicial = time()
    aux = df.copy()
    dfS = paso1(df)
    dfS = ordenar_columnas(dfS)
    dfS = ordenar_filas(dfS)
    final = time()
    tiempo = final-inicial
    graficarFINAL(aux,dfS,float("%.3f"%tiempo))

def ventanas(boolean):
    datos1 = [[1,0,0,1,0,1,0,0],
            [0,1,1,0,0,1,0,0],
            [1,0,0,1,0,0,1,1],
            [0,0,1,0,0,1,0,0],
            [0,0,0,1,1,0,0,1]]

    datos2 = [[0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
            [0,1,1,0,0,0,0,0,1,0,0,0,1,0,0],
            [1,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0]]

    if boolean==True:
        sg.theme("Reddit")
        #Ventanas
        layout = [[sg.Text("Direct Clustering Algorithm",size=(30,1),font=('Helvetica', 25), justification='center')],
                [sg.Text("Pablo Gutiérrez Aguirre",size=(35,1),font=('Helvetica', 20), justification='center')],
                [sg.Text("Patricio Saez Bustos",size=(35,1),font=('Helvetica', 20), justification='center')],
                [sg.Text("Universidad de Concepción",size=(35,1),font=('Helvetica', 20), justification='center')],
                [sg.Text("_",size=(140,1),font=('Helvetica', 1)),sg.Button("Siguiente",size=(10,1),font=('Helvetica', 15))]]

        window = sg.Window('Diseño de sistemas de producción', layout)
        flag= False
        while True:
            event, values = window.read()
            if event=="Siguiente":
                break
            if event==sg.WINDOW_CLOSED:
                flag = True
                break
        window.close()

        if flag==False:
            options = ["Matriz tarea","Matriz clase","Matriz aleatoria","Crear matriz"]
            width = max(map(len, options))+1

            layout = [ 
                [sg.Text("Instrucciones: Elegir la matriz a solucionar y luego hacer click en el método deseado",font=("Helvetica",14))],
                [sg.Text('Seleccionar matriz',font=("Helvetica",15)), sg.Combo(options, size=(width, 5), enable_events=True, key='-COMBO-',font=("Helvetica",15))],
                [sg.Text("Elija el método",font=("Helvetica",15))],
                [sg.Button('DCA',font=("Helvetica",15)), sg.Button('DCA mejorado',font=("Helvetica",15))],
                [sg.Text("Crear matriz y matriz aleatoria aun no está disponible",font=("Helvetica",10))]
                ]

            window = sg.Window('Diseño de sistemas de producción', layout, finalize=True)
            combo = window['-COMBO-']
            combo.bind("<Enter>", "ENTER-")
            
            while True:
                event, values = window.read()
                if event==sg.WINDOW_CLOSED:
                    break

                elif event == "DCA":
                    if values["-COMBO-"]=="Matriz tarea":
                        df = pd.DataFrame(datos2,columns=[i for i in range(1,len(datos2[0])+1)],index=[i for i in range(1,len(datos2)+1)])
                        dca(df)
                    if values["-COMBO-"]=="Matriz clase":
                        df = pd.DataFrame(datos1,columns=[i for i in range(1,len(datos1[0])+1)],index=[i for i in range(1,len(datos1)+1)])
                        dca(df)
                    if values["-COMBO-"]=="Matriz aleatoria":
                        largo = np.random.randint(0,21)
                        alto = np.random.randint(0,21)
                        datos = []
                        for i in range(alto):
                            datos.append(np.random.binomial(n=1, p=0.2, size=largo))
                        df = pd.DataFrame(datos,columns=[i for i in range(1,len(datos[0])+1)],index=[i for i in range(1,len(datos)+1)])
                        print(df)
                        dca(df)


                elif event =="DCA mejorado":
                    if values["-COMBO-"]=="Matriz tarea":
                        df = pd.DataFrame(datos2,columns=[i for i in range(1,len(datos2[0])+1)],index=[i for i in range(1,len(datos2)+1)])
                        dca_mejorado(df)
                    if values["-COMBO-"]=="Matriz clase":
                        df = pd.DataFrame(datos1,columns=[i for i in range(1,len(datos1[0])+1)],index=[i for i in range(1,len(datos1)+1)])
                        dca_mejorado(df)
                    if values["-COMBO-"]=="Matriz aleatoria":
                        largo = np.random.randint(5,21)
                        alto = np.random.randint(5,21)
                        datos = []
                        for i in range(alto):
                            datos.append(np.random.binomial(n=1, p=0.2, size=largo))
                        df = pd.DataFrame(datos,columns=[i for i in range(1,len(datos[0])+1)],index=[i for i in range(1,len(datos)+1)])
                        dca_mejorado(df)
            window.close()

ventanas(True)

#print(np.random.binomial(n=1, p=0.3, size=[10]))