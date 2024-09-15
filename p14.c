#include <stdio.h>
void main() 
{
    char name;
	int productID;
    float price, discountPercentage, finalPrice;
    printf("Enter Product name: ");
    scanf("%c",&name);
	printf("Enter product ID: ");
    scanf("%d", &productID);
    printf("Enter price of the product: ");
    scanf("%f", &price);
    printf("Enter discount percentage: ");
    scanf("%f", &discountPercentage);
    finalPrice = price - (price * discountPercentage / 100);
    printf("Product name: %c\n", name);
	printf("Product ID: %d\n", productID);
    printf("Final price after %.2f%% discount: %.2f\n", discountPercentage, finalPrice);
}