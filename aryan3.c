#include<stdio.h>
/*Write a c program for calculating the price of a product after adding the sales tax 
to its original price.Where rate of tax is inputted by user*/
void main()
{
	float rate,price,intrest,Finalprice;
	printf("Please enter the cost price ");
	scanf("%f", &price);
	printf("Please enter rate ");
	scanf("%f", &rate);
	intrest=(price*rate)/100;
	Finalprice=intrest+price;
	printf("Final price is ");
	printf("%f",Finalprice);
}
