/*In a school of three subjects (Maths,Science and english) for each subject are 
recorded as integer.The school wants to calculate the total and average marks of each 
student The average should be a floating point number with two decimal places.
Additionally the school wants to assign an identifier to each student based on
 their roll no(an integer)*/
 #include<stdio.h>
 void main()
 {
 	int m,s,e,id;
 	float avg,total;
 	printf("Please enter marks of Maths\n");
 	scanf("%d",&m);
 	printf("Please enter marks of Science\n");
 	scanf("%d",&s);
 	printf("Please enter marks of English\n");
 	scanf("%d",&e);
 	printf("Please enter identifier\n");
 	scanf("%d",&id);
 	total=m+s+e;
 	avg=total/3;
 	printf("Id=%d\n",id);
 	printf("Maths=%d\n",m);
 	printf("Science=%d\n",s);
 	printf("English=%d\n",m);
 	printf("Maths=%d\n",m);
 	printf("Average=%f\n",avg);
 }