from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from PIL import ImageTk, Image
import os
import ast
from sklearn import svm

class Clasificador:

    ventana = None
    clf = None

    entrenar = None
    predecir = None

    abrir_label = None
    abrir_enty = None
    abrir = None

    abrirf_label = None
    abrirf_enty = None
    abrirf = None


    tipo = None
    tipo_l = None
    imagen = None

    directorio = None
    directoriof = None

    x=[]
    y=[]

    predecir=[]

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Perros vs Gatos")
        self.ventana.geometry("800x600")

        self.abrir_label = Label(self.ventana, text="Entrenamiento").place(x=10,y=10)
        self.directorio = StringVar()
        self.abrir_enty = Entry(self.ventana,textvariable=self.directorio, state='readonly',width=60).place(x=120,y=10)
        self.abrir = Button(self.ventana,text="Seleccionar",command=self.abrirArchivo)
        self.abrir.place(x=680,y=10)


        self.abrirf_label = Label(self.ventana, text="Foto").place(x=10,y=40)
        self.directoriof = StringVar()
        self.abrirf_enty = Entry(self.ventana,textvariable=self.directoriof, state='readonly',width=60).place(x=120,y=40)
        self.abrirf = Button(self.ventana,text="Seleccionar",command=self.abrirfoto)
        self.abrirf.place(x=680,y=40)



        self.tipo_l = Label(self.ventana, text="Tipo")
        self.tipo_l.place(x=10,y=70)
        self.tipo = Spinbox(values=(-1, 1),width=10)
        self.tipo.place(x=120,y=70)

        self.entrenar = Button(self.ventana,text="Entrenar",command=self.entrenar)
        self.entrenar.place(x=10,y=550)
        self.predecir = Button(self.ventana,text="Predecir",command=self.predecir)
        self.predecir.place(x=120,y=550)
        self.ventana.mainloop()


    def caracteristicas(self,archivo,valor):
        arch = open(archivo,"r")
        lineas = arch.readlines()

        for i in lineas:
            self.x.append(ast.literal_eval(i))
            self.y.append(valor)

    def caracteristicasFoto(self,archivo):
        arch = open(archivo,"r")
        lineas = arch.readlines()
        #for i in lineas:
        #    self.predecir.append(ast.literal_eval(i))
        print(lineas)
        car = ast.literal_eval(lineas[0])
        print([car])
        self.predecir = [car]

    def entrenar(self):
        self.clf = svm.SVC()
        self.clf.fit(self.x, self.y)
        print(self.clf)

    def predecir(self):
        print(self.clf.predict(self.predecir))

    def abrirArchivo(self):
        self.ventana.withdraw()
        #self.ventana.iconify() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename( filetypes=(
                                            ("Archivos de Texto", "*.txt"),
                                            ("Archivos de Imagen", "*.jpg"),
                                            ("All files", "*.*")
                                           )
        ) # show an "Open" dialog box and return the path to the selected file

        if filename:
            try:
                print(filename)
                self.directorio.set( filename )
                self.caracteristicas(filename, int(self.tipo.get()) )

            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % filename)
                #return
        self.ventana.deiconify()


    def abrirfoto(self):
        self.ventana.withdraw()
        #self.ventana.iconify() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename( filetypes=(
                                            ("Archivos de Texto", "*.txt"),
                                            ("Archivos de Imagen", "*.jpg"),
                                            ("All files", "*.*")
                                           )
        ) # show an "Open" dialog box and return the path to the selected file

        if filename:
            try:
                print(filename)
                self.directoriof.set( filename )
                self.caracteristicasFoto(filename)

            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % filename)
                #return
        self.ventana.deiconify()


            #


    def mostrarImagen(self):
        img = ImageTk.PhotoImage(Image.open(self.filename))
        panel = Label(self.ventana, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")

if __name__ == '__main__':

    comp = Clasificador()
