/*WAP  to claculate salary of an employee,given his basic pay,HRA-15% of the basic pay
  and TA-20% of the basic pay*/
#include<stdio.h>
void main()
{
	float salary,final_salary;
	printf("Please enter basic salary\n");
	scanf("%f", &salary);
	final_salary=salary+0.15*salary+0.2*salary;
	printf("Final Pay amount is=%f",final_salary);
}