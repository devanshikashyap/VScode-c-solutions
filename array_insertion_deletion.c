#include <stdio.h>

int main()
{
    int arr[100], n, i;
    int choice, pos, value;

    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter %d elements:\n", n);
    for(i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    printf("\n1. Traversal");
    printf("\n2. Insertion");
    printf("\n3. Deletion");
    printf("\nEnter your choice: ");
    scanf("%d", &choice);

    switch(choice)
    {
        case 1:
            // Traversal
            printf("\nArray elements are:\n");
            for(i = 0; i < n; i++)
            {
                printf("%d ", arr[i]);
            }
            break;

        case 2:
            // Insertion
            printf("\nEnter the position for insertion: ");
            scanf("%d", &pos);

            printf("Enter the value to insert: ");
            scanf("%d", &value);

            for(i = n; i >= pos; i--)
            {
                arr[i] = arr[i - 1];
            }

            arr[pos - 1] = value;
            n++;

            printf("\nArray after insertion:\n");
            for(i = 0; i < n; i++)
            {
                printf("%d ", arr[i]);
            }
            break;

        case 3:
            // Deletion
            printf("\nEnter the position to delete: ");
            scanf("%d", &pos);

            for(i = pos - 1; i < n - 1; i++)
            {
                arr[i] = arr[i + 1];
            }

            n--;

            printf("\nArray after deletion:\n");
            for(i = 0; i < n; i++)
            {
                printf("%d ", arr[i]);
            }
            break;

        default:
            printf("\nInvalid choice!");
    }

    return 0;
}