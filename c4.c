/*WAP to enter two numbers from the user, Calculate and print their Sum, Product, 
  Divide*/
#include<stdio.h>
void main()
{
	float sum,product,divide,diff,a,b;
	printf("Please enter value of a\n");
	scanf("%f", &a);
	printf("Please enter value of b\n");
	scanf("%f", &b);
	sum=a+b;
	printf("Sum=");
	printf("%f",sum);
	product=a*b;
    printf("Product=");
	printf("%f",product);
	divide=a/b;
	printf("Divide is");
	printf("%f",divide);
	diff=a-b;
	printf("Difference=");
	printf("%f",diff);
}