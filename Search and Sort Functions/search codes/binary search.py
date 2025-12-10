def binary_search(target, items):
    low, high = 0, len(items) - 1
    # keep itereating until low and high cross
    while high >= low:
        # find midpoint
        mid = (low + high) // 2

        # if found at midpoint, return index
        if items[mid] == target:
            return mid
        # else, if item at midpoint  is less than target,
        # search the second half of the list
        elif items[mid] < target:
            low = mid + 1
        # else, search the first half
        else:
            high = mid - 1

    # returns none is notghing found
    return None


sorted_items = [10, 20, 30, 40, 50]
target_item = 20
result = binary_search(target_item, sorted_items)
print(result)
