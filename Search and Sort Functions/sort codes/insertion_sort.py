def insertion_sort(item):
    n = len(item)
    if n <= 1:
        return
    # if the array has 0 or 1 element, it is already sorted, so return
    for i in range(1, n):
        # Iterate over the array starting from the second element
        key = item[i]
        # store the current element as the key to be inserted in the
        # right position
        j = i - 1
        while j >= 0 and key < item[j]:
            # move elements greater than key one position ahead
            item[j + 1] = item[j]
            j -= 1
        item[j + 1] = key
