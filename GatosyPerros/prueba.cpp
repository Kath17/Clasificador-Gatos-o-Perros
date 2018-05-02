#include "CImg.h"
#include "imagenes.h"
//Para compilar: g++ -std=c++11 prueba.cpp -o main -L/usr/X11R6/lib -lm -lpthread -lX11


int main()
{
  // CImg<float> imagen("gat.jpg");
  // imagen.resize(256,256);
  // imagen = imagen.haar(false,2);
  // imagen = imagen.crop(0,0, 63, 63);
  // imagen.display();

  imagenes imgs;
  imgs.generar("Imagenes.txt",2);

  return 0;
}
