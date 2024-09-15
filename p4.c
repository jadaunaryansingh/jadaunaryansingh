/*WAP to input an integer,a  character,a float value from the keyboard and 
display them in different lines on the screen*/
#include<stdio.h>
void main()
{
	int a;
	char c;
	float f;
	printf("Pls enter character value\n");
	scanf("%c", &c);
	printf("Pls enter integer value\n");
	scanf("%d", &a);
	printf("Please enter float value\n");
	scanf("%f", &f);
	printf("\n");
	printf("Character is %c", c);
	printf("\n");
	printf("Integer is %d", a);
	printf("\n");
	printf("Float is %f", f);
}