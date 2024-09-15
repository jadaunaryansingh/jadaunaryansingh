//WAP to accept height and base of a triangle and calculate the area of the triangle
#include<stdio.h>
void main()
{
	float h,b,area;
	printf("Please enter height and base\n");
	scanf("%f\n",&h);
	scanf("%f",&b);
	area=(h*b)/2;
	printf("\nArea is=%f",area);
}