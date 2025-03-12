def heap_permutation(arr, n):
    if n == 1:
        print(arr)
        return

    for i in range(n):
        heap_permutation(arr, n - 1)

        if n % 2 == 0:
            arr[i], arr[n-1] = arr[n-1], arr[i]
        else:
            arr[0], arr[n-1] = arr[n-1], arr[0]


arr = [1, 2, 3]
n = len(arr)
heap_permutation(arr, n)
