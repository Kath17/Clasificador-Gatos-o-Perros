#include "CImg.h"
#include "imagenes.h"
//Para compilar: g++ -std=c++11 prueba.cpp -o main -L/usr/X11R6/lib -lm -lpthread -lX11


int main(int argc, char *argv[])
{
  // CImg<float> imagen("gat.jpg");
  // imagen.resize(256,256);
  // imagen = imagen.haar(false,2);
  // imagen = imagen.crop(0,0, 63, 63);
  // imagen.display();

  imagenes imgs;
  std::string tipo( argv[1] );
  std::string archivo( argv[2] );
  if(tipo == "f")
  {
    //cout << "foto" << endl;
    imgs.gen(archivo,2);
  }
  else if(tipo == "c")
  {
    //cout << "archivo" << endl;
    imgs.generar(archivo,2);
  }

  return 0;


}
