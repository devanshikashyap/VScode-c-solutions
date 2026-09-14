#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *prev;
    struct Node *next;
};

struct Node *head = NULL;

// Insert at the end
void insert()
{
    int value;
    struct Node *newNode, *temp;

    newNode = (struct Node *)malloc(sizeof(struct Node));

    printf("Enter value: ");
    scanf("%d", &value);

    newNode->data = value;
    newNode->prev = NULL;
    newNode->next = NULL;

    // If list is empty
    if (head == NULL)
    {
        head = newNode;
    }
    else
    {
        temp = head;

        while (temp->next != NULL)
        {
            temp = temp->next;
        }

        temp->next = newNode;
        newNode->prev = temp;
    }

    printf("Node inserted successfully.\n");
}

// Display the list
void display()
{
    struct Node *temp = head;

    if (head == NULL)
    {
        printf("List is empty.\n");
        return;
    }

    printf("Doubly Linked List: ");

    while (temp != NULL)
    {
        printf("%d <-> ", temp->data);
        temp = temp->next;
    }

    printf("NULL\n");
}

int main()
{
    int choice;

    while (1)
    {
        printf("\n--- Doubly Linked List ---\n");
        printf("1. Insertion\n");
        printf("2. Display\n");
        printf("3. Exit\n");

        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
            case 1:
                insert();
                break;

            case 2:
                display();
                break;

            case 3:
                exit(0);

            default:
                printf("Invalid choice.\n");
        }
    }

    return 0;
}