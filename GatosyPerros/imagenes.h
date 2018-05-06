#include "CImg.h"
#include <string>
#include<vector>
#include <iostream>
#include <fstream>
//#include <jpeglib.h>

using namespace cimg_library;
using namespace std;

class imagenes{
	public:
		float minimo;
		float maximo;
		float promedio;
		float desviacion;

		int cantidad_f;

		CImg<float>    imagen;
		// vector<float>  caract;   //vector caracteristico de cada imagen
		float caract[2]       = {};   //vector caracteristico de cada imagen

		// int temp = 0;
		// int numero_imagenes = 4;         //numero de imagenes en el archivo

		//El 2 es el numero de imagenes que tendra la base de datos
		float array_imagenes[200][4];         //Aqui se guardan los vectores de las imagenes
		string         nombre_archivo;          //nombre del archivo
		vector<string> nombre_imagenes;

	public:
		imagenes();
		void insertar(string name);
		void Haar_Wavelet(int num);
		void vector_Caracteristica(int temp);
		float get_minimo();
		float get_maximo();
		float get_promedio();
		float get_desviacion();
		void generar(string archivo,int num);
		void gen(string archivo,int num);

};

imagenes ::imagenes()
{
	minimo = maximo = promedio = desviacion = 0;
	nombre_archivo ="";
}

void imagenes:: insertar(string name)
{
	nombre_archivo = name;
	imagen.load(name.c_str());  //Carga la imagen
}

void imagenes::Haar_Wavelet(int nivel)
{
	int color = imagen.spectrum(); // to check the number of color channels
	switch(color)
	{
	    case 1:
	        imagen = imagen;
	        break;
	    case 3: // RGB to grayscale
	        imagen = imagen.get_RGBtoYCbCr().get_channel(0);
	        break;
	}

	imagen.normalize(0,255);
	imagen.resize(256,256);

	//APLICAMOS HAAR
  imagen = imagen.haar(false,nivel);   //Recomendado nivel 3
  imagen = imagen.crop(0,0, 63, 63);

	minimo = imagen.min();
	maximo = imagen.max();
	promedio = imagen.mean();
	// desviacion = imagen.std();

	//imagen.display();
}

void imagenes::vector_Caracteristica(int temp)
{
	// minimo = get_minimo();
	// maximo = get_maximo();
	// promedio = get_promedio();
	desviacion = get_desviacion();

	caract[0] = minimo;
	caract[1] = maximo;
	caract[2] = promedio;
	caract[3] = desviacion;

	/*
	cout<<"Temp: "<<temp<<endl;
	for(int i=0; i<4; i++)
		cout<<caract[i]<<"  ";
	*/

	array_imagenes[temp][0] = caract[0];
	array_imagenes[temp][1] = caract[1];
	array_imagenes[temp][2] = caract[2];
	array_imagenes[temp][3] = caract[3];

	cout << "["<<caract[0] <<","<< caract[1] << "," << caract[2] << "," << caract[3] << "]" <<endl;

	 // caract[4] = {};

	// for(int i=0;i<4;i++)
	// 	cout<<caract[i]<<"  ";
}

float imagenes:: get_minimo()
{
	 float mini = imagen(0,0);
   for(int i=0; i< imagen.width(); i++)
   		for(int j=0;j< imagen.height(); j++)
        	if(imagen(i,j) < mini)
            	mini = imagen(i,j);
    return mini;
}

float imagenes:: get_maximo()
{
   float maxi = imagen(0,0);
   for(int i=0; i<=imagen.width()-1;i++)
   		for(int j=0;j<=imagen.height()-1;j++)
        	if(imagen(i,j)>maxi)
            	maxi = imagen(i,j);
    return maxi;
}

float imagenes:: get_promedio()
{
	// return imagen.mean();
	float prom = 0.0;
   for(int i=0; i<=imagen.width()-1;i++)
   		for(int j=0;j<=imagen.height()-1;j++)
            prom += imagen(i,j);
    return (prom*1.0)/(256);
}

float imagenes:: get_desviacion()
{
	float prom = promedio;
	float count=0.0;
	for(int i=0; i<=imagen.width()-1;i++)
   		for(int j=0;j<=imagen.height()-1;j++)
            count +=pow(imagen(i,j)-prom,2);
    return sqrt(count/256);
}

void imagenes:: generar(string archivo,int nivel)
{
	int temp = 0;
	ifstream file(archivo.c_str());
	char buffer[1000];
	while(!file.eof()){
		file.getline(buffer,1000);
		nombre_imagenes.push_back(buffer);
		temp++;
	}
	file.close();
	cantidad_f = temp;
	//cout << cantidad_f;

	for (int i = 0; i < nombre_imagenes.size()-1; ++i)
	{
		insertar(nombre_imagenes[i]);
		Haar_Wavelet(nivel);
		// temp++;
		vector_Caracteristica(i);
	}


}

void imagenes:: gen(string archivo,int nivel)
{

	nombre_imagenes.push_back(archivo);

	for (int i = 0; i < nombre_imagenes.size(); ++i)
	{
		insertar(nombre_imagenes[i]);
		Haar_Wavelet(nivel);
		// temp++;
		vector_Caracteristica(i);
	}
}
