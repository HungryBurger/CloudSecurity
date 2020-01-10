#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <direct.h>

#define MIN 10*1024
#define MAX 15*1024

void insert(FILE * fp)
{
	int q, data, er;
	char ch;

	data = rand() % (MAX - MIN + 1) + MIN;
	data = data * 1000;//kb
	for (q = 0; q < data; q++)
	{
		er = rand() % 2;
		if (er == 0)//uppercase
			ch = rand() % ('Z' - 'A' + 1) + 'A';

		else//lowcase
			ch = rand() % ('z' - 'a' + 1) + 'a';

		fputc(ch, fp);
	}

}

void main(void)
{
	char stream[100], ii[10], fileName[10];
	int create, i, result;
	FILE* fp;

	srand(time(NULL));

	printf("fileName : ");
	scanf("%s", fileName);

	result = mkdir(fileName);//make a dir

	printf("Create : ");
	scanf("%d", &create);

	for (i = 1; i <= create; i++) {

		stream[0] = NULL;//clear buffer

		sprintf(ii, "%d", i);//integer to character

		strcat(stream, fileName);
		strcat(stream, "\\");
		strcat(stream, ii);
		strcat(stream, ".txt");

		fp = fopen(stream, "w");

		insert(fp);

		fclose(fp);
		printf("%3d is success\n", i);
	}
}