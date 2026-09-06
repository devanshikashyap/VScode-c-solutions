#include <stdio.h>

// Partition function
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    int j, temp;

    for (j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;

            temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // Put pivot in its correct position
    temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return i + 1;
}

// Quick Sort function
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        // Sort elements before pivot
        quickSort(arr, low, pi - 1);

        // Sort elements after pivot
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    int arr[100], n, i;

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter elements:\n");
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    quickSort(arr, 0, n - 1);

    printf("Sorted array:\n");
    for (i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}