#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *next;
};

int main()
{
    struct Node *head = NULL, *newNode, *temp;
    int n, i, value, key, found = 0;

    printf("Enter number of nodes: ");
    scanf("%d", &n);

    // Create linked list
    for(i = 0; i < n; i++)
    {
        newNode = (struct Node *)malloc(sizeof(struct Node));

        printf("Enter value: ");
        scanf("%d", &value);

        newNode->data = value;
        newNode->next = NULL;

        if(head == NULL)
        {
            head = newNode;
        }
        else
        {
            temp = head;

            while(temp->next != NULL)
            {
                temp = temp->next;
            }

            temp->next = newNode;
        }
    }

    // Search
    printf("\nEnter value to search: ");
    scanf("%d", &key);

    temp = head;
    i = 1;

    while(temp != NULL)
    {
        if(temp->data == key)
        {
            printf("Element %d found at position %d.\n", key, i);
            found = 1;
            break;
        }

        temp = temp->next;
        i++;
    }

    if(found == 0)
    {
        printf("Element not found.\n");
    }

    return 0;
}