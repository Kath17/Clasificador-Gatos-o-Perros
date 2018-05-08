from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror

from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import glob
import ast
from sklearn import svm

from itertools import repeat

from images import Images


class Clasificador:

    #Interfaz
    ventana = None

    canvas = None

    entrenar = None
    predecir = None
    predecir_batch = None

    abrir_label = None
    abrir_enty = None
    abrir = None

    abrirf_label = None
    abrirf_enty = None
    abrirf = None

    imagen = None

    directorio = None
    directoriof = None
    directorio_tanda = "tanda/"
    fnt = ImageFont.truetype("arial.ttf", 30)

    animal1_str = None
    animal1_label = None
    animal1_entry = None

    animal2_str = None
    animal2_label = None
    animal2_entry = None

    guardar = None

    #Datos
    clf = None
    x=[]
    y=[]

    entrenado = False
    paraPredecir=[]
    predicho=[]

    ImagenVC = Images()
    animales=[]
    vals = [-1,1]
    pos_vals = 0
    cant_max = 2

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Perros vs Gatos")
        self.ventana.geometry("800x600")

        self.abrir_label = Label(self.ventana, text="Entrenamiento").place(x=10,y=10)
        self.directorio = StringVar()
        self.abrir_enty = Entry(self.ventana,textvariable=self.directorio, state='readonly',width=60).place(x=120,y=10)
        self.abrir = Button(self.ventana,text="Seleccionar",command=self.abrirArchivo,state='disabled')
        self.abrir.place(x=680,y=10)


        self.abrirf_label = Label(self.ventana, text="Foto").place(x=10,y=40)
        self.directoriof = StringVar()
        self.abrirf_enty = Entry(self.ventana,textvariable=self.directoriof, state='readonly',width=60).place(x=120,y=40)
        self.abrirf = Button(self.ventana,text="Seleccionar",command=self.abrirfoto,state='disabled')
        self.abrirf.place(x=680,y=40)

        self.entrenar = Button(self.ventana,text="Entrenar",command=self.entrenarSVM,state='disabled')
        self.entrenar.place(x=10,y=550)
        self.predecir = Button(self.ventana,text="Predecir",command=self.predecirSVM,state='disabled')
        self.predecir.place(x=120,y=550)

        self.predecir_batch = Button(self.ventana,text="Predecir Tandas",command=self.predecirBatch,state='disabled')
        self.predecir_batch.place(x=230,y=550)

        self.animal1_str = StringVar()
        self.animal1_label = Label(self.ventana,text="Animal 1").place(x=10,y=70)
        self.animal1_entry = Entry(self.ventana,textvariable=self.animal1_str,width=20)
        self.animal1_entry.place(x=120,y=70)

        self.animal2_str = StringVar()
        self.animal2_label = Label(self.ventana,text="Animal 2").place(x=390,y=70)
        self.animal2_entry = Entry(self.ventana,textvariable=self.animal2_str,width=20)
        self.animal2_entry.place(x=480,y=70)

        self.guardar = Button(self.ventana,text="Guardar",command=self.nombres)
        self.guardar.place(x=680,y=70)


        # create the canvas, size in pixels
        self.canvas = Canvas(self.ventana,width=400, height=400)
        self.canvas.place(x=200,y=120 )


        self.ventana.mainloop()

    def nombres(self):
        if(self.animal1_str.get()!="" and self.animal2_str.get()!=""):
            self.animales.append(self.animal1_str.get())
            self.animales.append( self.animal2_str.get() )
            self.animal1_entry.config(state='readonly')
            self.animal2_entry.config(state='readonly')
            print(self.animales)
            self.abrir.config(state="normal")
            self.abrir.config(text="Abrir "+self.animales[self.pos_vals])
            self.guardar.config(text="Guardado")
            self.guardar.config(state="disabled")

        else:
            showerror("Nombre de animales","Ingrese nombres correctos.")

    def caracteristicas(self,directorio):
        print(self.imagenesDirectorio(directorio))
        FV = self.ImagenVC.FeatureVectors(self.imagenesDirectorio(directorio))
        self.x.extend(FV)
        self.y.extend( repeat( self.vals[self.pos_vals]  , len(FV) ) )
        self.pos_vals = self.pos_vals+1
        if( self.pos_vals < self.cant_max):
            self.abrir.config(text="Abrir "+self.animales[self.pos_vals])
        else:
            self.abrir.config(text="Listo")
            self.entrenar.config(state="normal")



    def caracteristicasFoto(self,archivo):
        self.ImagenVC.VectorCaracteristico(archivo)
        self.paraPredecir.append([self.ImagenVC.vectorC])

    def entrenarSVM(self):
        if(len(self.x) > 0 and len(self.y) > 0 and len(self.animales) > 0):
            self.clf = svm.SVC()
            self.clf.fit(self.x, self.y)
            print(self.clf)
            self.abrirf.config(state="normal")
            self.predecir.config(state="normal")
            self.predecir_batch.config(state="normal")
            self.entrenado = True
        else:
            showerror("Entrenar","Seleccione los directorios")

    def predecirSVM(self):
        if( len(self.paraPredecir) > 0 ):
            #Ultimo elemento de paraPredecir
            predicho = self.clf.predict( self.paraPredecir[-1] )[0]
            self.predicho.append( predicho  )
            self.printPredichoLabel(predicho)
        else:
            showerror("Predecir","Primero Ingrese una foto para entrenar.")

    def paraPredecirBatch(self,directory):
        nomb=0
        if not os.path.exists(self.directorio_tanda):
            os.makedirs(self.directorio_tanda)
        imagenes = self.imagenesDirectorio(directory)
        for i in imagenes:
            self.caracteristicasFoto(i)
            self.predecirSVM()
            self.guardarImagen(i,self.directorio_tanda,nomb)
            nomb+=1

    def predecirBatch(self):
        if( self.entrenado == True ):
            self.ventana.withdraw()
            directory = askdirectory()
            self.ventana.deiconify()
            if directory:
                try:
                    print(directory)
                    self.directoriof.set(directory)


                except:
                    showerror("Abrir Directorio","No se puede abrir el directorio\n'%s'"%directory)
            self.paraPredecirBatch(directory)
        else:
            showerror("Predicir en tanda","Primero entrene.")



    def printPredichoLabel(self,predicho):
        for an in range(0, len(self.vals)):
            if( predicho == self.vals[an]):
                clasif = "Es un "+self.animales[an]
                self.canvas.create_text(120,330,text=clasif,font=("Arial",30))
                break

    def printPredicho(self):
        for i in self.predicho:
            for an in range (0, len(self.vals) ):
                if( i == self.vals[an]):
                    print(i,": Es un ", self.animales[an])
                    break


    def guardarImagen(self,imagen,directorio,nombre):
        im = Image.open(imagen)
        draw = ImageDraw.Draw(im)
        for an in range(0, len(self.vals)):
            if( self.predicho[-1] == self.vals[an]):
                clasif = "Es un "+self.animales[an]
                #self.canvas.create_text(120,330,text=clasif,font=("Arial",30))
                draw.text((0,0),text=clasif,font=self.fnt,fill="black")
                break
        path=directorio+str(nombre)+".jpg"
        im.save(path)


    def abrirArchivo(self):

        if( self.pos_vals < self.cant_max and len(self.animales)>0):
            self.ventana.withdraw()
            directory = askdirectory()
            self.ventana.deiconify()
            if directory:
                try:
                    print(directory)
                    self.directorio.set(directory)
                    self.caracteristicas(directory)

                except:
                    showerror("Abrir Directorio","No se puede abrir el directorio\n'%s'"%directory)
        else:
            showerror("Nombres de los animales","Ingrese el nombre de los animales")



    def abrirfoto(self):
        self.ventana.withdraw()
        #self.ventana.iconify() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename( filetypes=(
                                            ("Archivos de Imagen", "*.jpg"),
                                            ("All files", "*.*")
                                           )
        ) # show an "Open" dialog box and return the path to the selected file
        self.ventana.deiconify()
        if filename:
            try:
                print(filename)
                self.directoriof.set(filename)
                self.caracteristicasFoto(filename)

            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % filename)
                #return

        self.mostrarFoto(filename)

    def mostrarFoto(self,archivo):
        # load the .gif image file
        image = Image.open(archivo)
        image = image.resize((400, 400), Image.ANTIALIAS)
        imag = ImageTk.PhotoImage(image)

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.image = imag
        self.canvas.create_image(0, 0, image=imag, anchor=NW)


    def imagenesDirectorio(self,dir):
        return glob.glob(dir+"/*.jpg")


if __name__ == '__main__':

    comp = Clasificador()
