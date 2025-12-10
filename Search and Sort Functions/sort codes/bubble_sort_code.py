def bubble_sort(items):
    for i in range(len(items) - 1, - 1, - 1):
        for j in range(1, i + 1):
            if items[j - 1] > items[j]:
                items[j - 1], items[j] = items[j], items[j - 1]
    return items


e = [1, 3, 6, 2, 4, 7, 8]
sorted_e = bubble_sort(e)
print(sorted_e)
