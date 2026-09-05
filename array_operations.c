#include <stdio.h>

void traverse(int arr[], int n)
{
    int i;

    printf("Array elements are: ");

    for (i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");
}

void insertElement(int arr[], int *n, int position, int value)
{
    int i;

    if (position < 1 || position > *n + 1)
    {
        printf("Invalid position!\n");
        return;
    }

    for (i = *n; i >= position; i--)
    {
        arr[i] = arr[i - 1];
    }

    arr[position - 1] = value;
    (*n)++;

    printf("Element inserted successfully!\n");
}

void deleteElement(int arr[], int *n, int position)
{
    int i;

    if (position < 1 || position > *n)
    {
        printf("Invalid position!\n");
        return;
    }

    for (i = position - 1; i < *n - 1; i++)
    {
        arr[i] = arr[i + 1];
    }

    (*n)--;

    printf("Element deleted successfully!\n");
}

int main()
{
    int arr[100];
    int n, choice, position, value;
    int i;

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d elements:\n", n);

    for (i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    do
    {
        printf("\n===== 1D ARRAY OPERATIONS =====\n");
        printf("1. Traversal\n");
        printf("2. Insertion\n");
        printf("3. Deletion\n");
        printf("4. Exit\n");

        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
            case 1:
                traverse(arr, n);
                break;

            case 2:
                printf("Enter position for insertion: ");
                scanf("%d", &position);

                printf("Enter value: ");
                scanf("%d", &value);

                insertElement(arr, &n, position, value);
                break;

            case 3:
                printf("Enter position for deletion: ");
                scanf("%d", &position);

                deleteElement(arr, &n, position);
                break;

            case 4:
                printf("Exiting program...\n");
                break;

            default:
                printf("Invalid choice!\n");
        }

    } while (choice != 4);

    return 0;
}

