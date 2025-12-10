def sequentrial_search(target, items):
    # iterate over the list, If target is found, returns index
    for index in range(len(items)):
        if items[index] == target:
            return index
    # if target item not found returns none
    return None


items_list = [50, 10, 40, 20, 30]
target_item = 30
result = sequentrial_search(target_item, items_list)

if result is not None:
    print(f"Item {target_item} found at index {result}")
else:
    print(f"Item {target_item} not found in list.")
