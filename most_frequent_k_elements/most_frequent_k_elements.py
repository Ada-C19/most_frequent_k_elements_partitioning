def count_elements(arr):
    # could use an int defaultdict or Counter rather than a plain dict,
    frequency_map = {}

    for num in arr:
        # if using a defaultdict, these 2 lines would just be frequency_map[num] += 1
        count = frequency_map.get(num, 0)
        frequency_map[num] = count + 1

    return frequency_map

# Partition the input arr until we find the kth value. Since we don't need to
# partition both the left and right sides around the pivot (only the side that brings
# us closer to the kth value), we can do this iteratively. Use two pointers to
# track the start and end of the sub-array being partitioned, and adjust either 
# the start or end on each iteration to zero in on the area of the list where the
# kth largest value must end up (position k-1). The partitioning will occur in-place
# in arr.
#
# Time complexity: O(n). We must consider how many times we perform comparisons to
# arrive at the time complexity. The first partition pass needs to compare each value
# with the pivot (n comparisons), so there are at least O(n) comparisons. We expect
# (hope) the pivot will end up dividing the list approximately in half. If that happens,
# then in the worst case, it would take us O(log n) partition passes to get down to
# a single value to partition, so there can be no more than O(log n) iterations. Each
# iteration would operate on half the data, so n/2 + n/4 + n/8 + ... up to log n terms.
# We can factor out the n to be n * (1/2 + 1/4 + ...) and the sum of decreasing halves
# totals to 1, so all remaining iterations will perform n comparisons, for time complexity
# of O(2n) => O(n). As with any partitioning approach, there's a chance of a degenerate
# case where this actually tends towards O(n^2) but we don't expect this occur for
# arbitrary data.
#
# Space complexity: O(1). We operate in-place on the arr value and only introduce
# scalar additional values (no lists or other collections)
def partition_kth_value(arr, k, key):
    start = 0
    end = len(arr)  # 1 past the end of the range, as is typically in python

    # The range-based equivalent of checking that the length of the list is 0 or 1
    if end - start <= 1:
        return
    
    # Partition until the pivot ends up at k-1. A pivot placed at position k-1 
    # is the kth largest value. The k-1 values to the left must all be larger 
    # than the pivot, or else they would have been moved to the right of the pivot.
    while True:
        pivot_idx = end - 1  # pick the end of the range as the pivot
        pivot = arr[pivot_idx]  # the pivot value
        pivot_key = key(pivot)  # the key (count) for the pivot

        # The "end" of the left list (where we'll put the values larger than the
        # pivot count) is initially empty (the start and its end are the same index).
        # Notice by the end - start = size relationship of exclusive ranges, when
        # start is equal to end, the size works out to 0. As we find values that
        # should go to the left of the pivot, we'll swap whatever's at the end of
        # the list with the value that should go into the list, and bump up the end
        # of the list to the next index. Finally, we'll swap the pivot to the end of
        # the left list, resulting all values to the left being larger than the 
        # pivot, and all to the right being smaller.
        left_list_end = start

        # Examine each of the values in the range, and compare them to the pivot
        # (using their keys, in this case, their count). We can stop iterating just
        # before the pivot, since there's no need to compare the pivot to itself
        for i in range(start, pivot_idx):
            el = arr[i]  # the current list value
            el_key = key(el)  # the key (count) for the current list value

            # A key larger than the pivot's key should move to the left list
            if el_key > pivot_key:
                # swap the value in for the end of the list and grow the list by one
                arr[left_list_end], arr[i] = arr[i], arr[left_list_end]
                left_list_end += 1

        # After processing all values, the end of the left list designates where
        # the pivot should go, so swap it there
        arr[left_list_end], arr[pivot_idx] = arr[pivot_idx], arr[left_list_end]

        # The pivot was moved to left_list_end, so use that to check where the
        # pivot ended up relative to the location we are looking for (the kth
        # largest value should end up at k-1)
        if left_list_end == k - 1:
            break  # found the kth value, so we're done
        elif left_list_end < k - 1:
            # The pivot is to the left of the target value, so we need to partition
            # to the right (by shifting up the start) to continue our search for
            # the kth value.
            start = left_list_end + 1
        else:
            # The pivot is to the right of the target value, so we need to partition
            # to the left (by shifting down the end) to continue our search for
            # the kth value.
            end = left_list_end

# Time complexity: O(n). The time to build the count dict, read out the unique values, 
# and extract the k required values are all dependent on n. Partitioning is itself
# O(n) and hence the total time is O(4n) => O(n). As with the space complexity (which
# follows) we could break out individual components with their own variables, but as
# they all trace back to n in some way, it's sufficiently accurate to stick with O(n).
#
# Space complexity: O(n). We create a dict and a list that depend on the size of the
# input. We could introduce an additional variable to stand in for the number of
# unique values, and account for k being able to vary independently of n giving O(n + u + k),
# but as u and k are bound by n, the overall complexity remains linear, and O(n)
# captures this clearly enough.
def most_frequent_k_elements(arr, k):
    frequency_map = count_elements(arr)  # time: O(n), space: O(n)

    # Get an actual list of the unique values. We need a list for the subscripting
    # ability. Note that dict.keys() does NOT return a list, but rather an iterator,
    # which we usually use in for/in loops. When list receives an iterator, it reads
    # all the values from it into a new list. This behavior differs from using a
    # list literal [] which does not read from the iterator, but rather just would
    # make a list with one thing in it (here, the dict, or the iterator if we used
    # the explicit dict.keys() call).
    uniques = list(frequency_map)  # time: O(n), space: O(n)

    # Partition in-place, ensuring that the the kth value is the correct place. This
    # also ensures that the k-1 values to its left will be larger than the pivot value.
    # Note there is nothing special about the parameter key. We used the same name
    # as sorted for consistency. The function (lambda) we're passing in will be used
    # to retrieve the comparison key to be used during the partitioning, so key is
    # a reasonable name for it.
    partition_kth_value(uniques, k, key=lambda num: frequency_map[num])  # time: O(n), space: O(1)

    # Strip off the first k values as our return list.
    return uniques[:k]  # time: O(n), space: O(n) (really both are O(k), but k can equal n)
