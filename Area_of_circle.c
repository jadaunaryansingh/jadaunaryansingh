//WAP to print area of circle
#include<stdio.h>
#define PI 3.1415
void main()
{
	float area,r;
	printf("Please enter radius\n");
	scanf("%f",&r);
	area=PI*r*r;
	printf("Area=%f",area);
}