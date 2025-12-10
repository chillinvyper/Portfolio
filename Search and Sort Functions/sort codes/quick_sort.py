def quick_sort(items, low, high):
    if low < high:
        # partition the list to get the pivot index
        mid = partition(items, low, high)
        # recursivly sort the left partition
        items = quick_sort(items, low, high - 1)
        # recursivly sort the right partition
        items = quick_sort(items, mid + 1, high)
    return items


def partition(items, low, high):
    # pivot point is the first item in the sublist
    pivot = items[low]
    # loop through the list. Move items up or dpwn the list so that they
    # are in the proper spot with regard to the pivot point
    while low < high:
        # can we find a number smaller than the pivot point:
        # keep moving the high marker down the list until we find this
        # or until high == low
        while low < high and items[high] >= pivot:
            high -= 1
        if low < high:
            # found a smaller number, swap it into position
            items[low] = items[high]
            # now look for a number larger than the piovt point
            while low < high and items[low] <= pivot:
                low += 1
            if low < high:
                # found one! move it into position
                items[high] = items[low]
    # move the pivot back into the list and return its index
    items[low] = pivot
    return low
