import pywt
import cv2
import numpy as np

class Images:

    # Imagen original
    img = None
    # Imagen en 256x256
    imagen = None
    # Imagen con el Haar aplicado
    imagen2 = None
    # Vector característica
    vectorC = []

    def AbrirImagen(self, name):
        #carga imagen
        self.img = cv2.imread(name)
        cv2.imshow('Imagen',self.img)
        # print("matriz:",self.img)

    def ResizeImage(self, img):
        mat = cv2.imread(img)
        self.imagen = cv2.resize(mat, (256, 256))
        cv2.imshow('Imagen 256x256',self.imagen)
        # print("matriz:",self.imagen)
        print("matriz:",self.imagen.shape)
        return self.imagen

    #                             -------------------
    #                             |        |        |
    #                             | cA(LL) | cH(LH) |
    #                             |        |        |
    # (cA, (cH, cV, cD))  <--->   -------------------
    #                             |        |        |
    #                             | cV(HL) | cD(HH) |
    #                             |        |        |
    #                             -------------------

    def HaarWavelet(self,image):
        # #convert to grayscale
        # imArray = cv2.cvtColor( img,cv2.COLOR_RGB2GRAY )

        #Usar un canal para cada uno:
        B,G,R = cv2.split(image)

        #BLUE
        #convert image to float
        fimageB =  np.float32(B)
        # print("Fimage:",fimageB)
        (b , (b1,b2,b3)) = pywt.dwt2(fimageB,"haar")
        b = np.uint8(b)
        # print("Fimage:",b)
        # cv2.imshow('haarb:',b)

        #GREEN
        fimageG =  np.float32(G)
        (g , (g1,g2,g3)) = pywt.dwt2(fimageG,"haar")
        g = np.uint8(g)

        #RED
        fimageR =  np.float32(R)
        (r , (r1,r2,r3)) = pywt.dwt2(fimageR,"haar")
        r = np.uint8(r)

        #Juntamos los haar de los tres canales, para formar una unica imagen
        self.imagen2 = cv2.merge([b,g,r])
        cv2.imshow('haar:',self.imagen2)
        print("imagen2:", self.imagen2.shape)

        # compute coefficients
        # coeffs = pywt.dwt2(fimage, "haar", level=1)
        # cA, (cH, cV, cD) = coeffs

    def Haar_level3(self,image):
        self.HaarWavelet(image)
        self.HaarWavelet(self.imagen2)
        self.HaarWavelet(self.imagen2)

    def VectorCaracterístico(self, nombre):
        resized = vect.ResizeImage(nombre)
        self.Haar_level3(resized)

        # print("Imagen con haar:",self.imagen2)

        #Minimos B,G,R
        minB = np.array(self.imagen2)[...,0].min()
        minG = np.array(self.imagen2)[...,1].min()
        minR = np.array(self.imagen2)[...,2].min()

        #Maximos B,G,R
        maxB = np.array(self.imagen2)[...,0].max()
        maxG = np.array(self.imagen2)[...,1].max()
        maxR = np.array(self.imagen2)[...,2].max()

        #Promedios B,G,R
        prom, desv = cv2.meanStdDev(self.imagen2)
        prom = prom[:3]
        print("promedios:",prom)

        #Desviacion Estandar B,G,R
        desv = desv[:3]
        print("desviaciones:",desv)

        self.vectorC.extend( (minB,minG,minR,maxB,maxG,maxR))
        self.vectorC.extend((prom[0][0],prom[1][0],prom[2][0]))
        self.vectorC.extend((desv[0][0],desv[1][0],desv[2][0]))

        print("vector carac:",self.vectorC)

vect = Images()
vect.AbrirImagen("gato1.jpg")
# vect.ResizeImage("gato1.jpg")
# vect.HaarWavelet(vect.imagen)
# vect.Haar_level3(vect.imagen)
vect.VectorCaracterístico("gato1.jpg")
