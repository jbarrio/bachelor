#include <stdio.h> // necesario para FILE, fopen/fclose, fprintf, perror y stderr
#include <stdlib.h> // necesario para la syscall exit()
#include <windows.h> // necesario para el acceso minimo a la API de Windows

#define SALIDA "C:\\tmp\\lista_sz.txt" // asumo que la extension es .txt aunque la actividad no lo aclara

int main(void) // no utilizo argc/argv porque la actividad no pide argumentos
{
	WIN32_FIND_DATAA fd; // el equivalente a un file descriptor en Linux
	HANDLE h; // el handle sobre el que iteraremos
	FILE *fp; // puntero a fichero
	unsigned long long size; // equivalente u_long64_t en Linux, para poder sacar tamanos grandes

	fp = fopen(SALIDA, "w");
	if (fp == NULL) { // control de errores si no podemos crear para escritura el fichero de destino
		perror(SALIDA);
		exit(1); // vengo de POSIX, por tanto 1 = ERROR, 0 = EXITO
	}

	/* en Windwos no hay opendir(), se usa FindFirstFile con comodin */
	h = FindFirstFileA("*", &fd);
	if (h == INVALID_HANDLE_VALUE) {
		fprintf(stderr, "FindFirstFile: error %lu\n", GetLastError());
		fclose(fp);
		exit(1);
	}

	do {
		/* 
         * los directorios (incluidos . y ..) los salto porque
         * la actividad pide extrictamente listar ficheros
         */
		if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
			continue;

		/* el tamano viene partido en dos mitades de 32 bits por compatibilidad con FS viejos */
        /* el cast lo hago para no tener warnings y asegurar el tamano para la suma */
		size = ((unsigned long long)fd.nFileSizeHigh << 32) | fd.nFileSizeLow;
        // pongo el el texto en formato "nombre:tamano" para que me ayude luego a parsear en PowerShell
		if (fprintf(fp, "%s:%llu\n", fd.cFileName, size) < 0) {
			perror("fprintf");
			break;
		}
	} while (FindNextFileA(h, &fd)); // uso do-while para no tener que forzar el break

	/* FindNextFile devuelve 0 al acabar, pero tambien si falla y quiero capturar ese error */
	if (GetLastError() != ERROR_NO_MORE_FILES)
		fprintf(stderr, "FindNextFile: error %lu\n", GetLastError());

	FindClose(h); // cierro el handle, aunque tecnicamente Windows deberia cerrarlo al acabar la ejecucion

	if (fclose(fp) != 0) { // lo mismo, lo cierro por elegancia/seguridad, pero el SO debe ser capaz de cerrarlo
		perror("fclose");
		exit(1);
	}

	return 0;
}
