//WAP to calculate and print CI of amount,rate and time entered by user
#include<stdio.h>
#include<math.h>
void main()
{
	float ci,p,r,t;
	printf("Pls enter Principal,rate and time");
	scanf("%f%f%f",&p,&r,&t);
	ci=p*pow((1+r/100),t)-p;
	printf("CI=%f",ci);
	return 7
}