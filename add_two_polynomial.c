#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int coeff;
    int power;
    struct Node *next;
};

// Create a new node
struct Node* createNode(int coeff, int power)
{
    struct Node *newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));

    newNode->coeff = coeff;
    newNode->power = power;
    newNode->next = NULL;

    return newNode;
}

// Insert a term at the end
struct Node* insert(struct Node *head, int coeff, int power)
{
    struct Node *newNode, *temp;

    newNode = createNode(coeff, power);

    if(head == NULL)
    {
        return newNode;
    }

    temp = head;

    while(temp->next != NULL)
    {
        temp = temp->next;
    }

    temp->next = newNode;

    return head;
}

// Add two polynomials
struct Node* add(struct Node *p1, struct Node *p2)
{
    struct Node *result = NULL;

    while(p1 != NULL && p2 != NULL)
    {
        if(p1->power == p2->power)
        {
            result = insert(result,
                            p1->coeff + p2->coeff,
                            p1->power);

            p1 = p1->next;
            p2 = p2->next;
        }
        else if(p1->power > p2->power)
        {
            result = insert(result, p1->coeff, p1->power);
            p1 = p1->next;
        }
        else
        {
            result = insert(result, p2->coeff, p2->power);
            p2 = p2->next;
        }
    }

    while(p1 != NULL)
    {
        result = insert(result, p1->coeff, p1->power);
        p1 = p1->next;
    }

    while(p2 != NULL)
    {
        result = insert(result, p2->coeff, p2->power);
        p2 = p2->next;
    }

    return result;
}

// Display polynomial
void display(struct Node *head)
{
    while(head != NULL)
    {
        printf("%dx^%d", head->coeff, head->power);

        if(head->next != NULL)
        {
            printf(" + ");
        }

        head = head->next;
    }

    printf("\n");
}

int main()
{
    struct Node *p1 = NULL;
    struct Node *p2 = NULL;
    struct Node *result = NULL;

    int n1, n2;
    int i, coeff, power;

    // First polynomial
    printf("Enter number of terms in first polynomial: ");
    scanf("%d", &n1);

    printf("Enter terms in descending order of power:\n");

    for(i = 0; i < n1; i++)
    {
        printf("Enter coefficient: ");
        scanf("%d", &coeff);

        printf("Enter power: ");
        scanf("%d", &power);

        p1 = insert(p1, coeff, power);
    }

    // Second polynomial
    printf("\nEnter number of terms in second polynomial: ");
    scanf("%d", &n2);

    printf("Enter terms in descending order of power:\n");

    for(i = 0; i < n2; i++)
    {
        printf("Enter coefficient: ");
        scanf("%d", &coeff);

        printf("Enter power: ");
        scanf("%d", &power);

        p2 = insert(p2, coeff, power);
    }

    // Display polynomials
    printf("\nFirst Polynomial: ");
    display(p1);

    printf("Second Polynomial: ");
    display(p2);

    // Addition
    result = add(p1, p2);

    printf("Sum: ");
    display(result);

    return 0;
}