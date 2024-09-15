/*The population of a city is 30000.It increases by 20% in the first year  and 
30% during the second year.WAP to find the population after two years*/
#include<stdio.h>
void main()
{
	float p=30000,firstyr,secondyr;
	firstyr=30000+0.2*30000;
	secondyr=firstyr+0.3*firstyr;
	printf("The population after two years is=%f",secondyr);
}