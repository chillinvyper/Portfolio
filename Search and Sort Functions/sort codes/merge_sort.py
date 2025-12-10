def merge_sort(items):
    # get the length of the input list
    items_length = len(items)

    # create temporary storage for merging
    temp_storage = [None] * items_length

    # initialise the size of subsections to 1
    size_of_subsections = 1

    # iterate until the size of subsections is less than the length of the list
    while size_of_subsections < items_length:
        # iterate over the list in steps of size_of_subsections * 2
        for i in range(0, items_length, size_of_subsections * 2):
            # determine the start and end indicies of the two subsections
            # to merge
            first_section_start, first_section_end = i, min(
                i + size_of_subsections, items_length
                )
            second_section_start, second_section_end = first_section_end, min(
                first_section_end + size_of_subsections, items_length
            )
            # define the sections to merge
            sections = (first_section_start, first_section_end), (
                second_section_start, second_section_end,
            )
            # call merge function to merge the subsections
            merge(items, sections, temp_storage)

        size_of_subsections *= 2

    return items


def merge(items, sections, temp_storage):
    # unpack the sections tuple to get the start and emd indicies of
    # each section
    (first_section_start, first_section_end), (
        second_section_start, second_section_end,
    ) = sections

    # Initialise indices for the two sections and temp storage
    left_index = first_section_start
    right_index = second_section_start
    temp_index = 0

    # loop until both sections are fully merged
    while left_index < first_section_end or right_index < second_section_end:
        # check if both sections still have elements to compare
        if left_index < first_section_end and right_index < second_section_end:
            # compare elements from both sections
            if items[left_index] < items[right_index]:
                # place smaller index into temp storage
                temp_storage[temp_index] = items[left_index]
                left_index += 1
            else:  # items[right_index] <= items[left_index]
                temp_storage[temp_index] = items[right_index]
                right_index += 1
            temp_index += 1

        # if  section 1 still has elements left to merge
        elif left_index < first_section_end:
            # copy remaining elements from section 1 to temp storage
            for i in range(left_index, first_section_end):
                temp_storage[temp_index] = items[left_index]
                left_index += 1
                temp_index += 1

        # if section 2 still has elements left to merge
        else:  # right_index < second_section_end
            # Copy remaining elements from section 2 to temp storage
            for i in range(right_index, second_section_end):
                temp_storage[temp_index] = items[right_index]
                right_index += 1
                temp_index += 1

    for i in range(temp_index):
        items[first_section_start + i] = temp_storage[i]


# example_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
example_list = [33, 10, 59, 26, 41, 58, 18]
sorted_list = merge_sort(example_list)
print(sorted_list)
