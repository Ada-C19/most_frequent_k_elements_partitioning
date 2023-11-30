from most_frequent_k_elements.most_frequent_k_elements import most_frequent_k_elements

def test_most_frequent_k_elements_nominal():
    # Arrange
    arr = [1,1,1,2,2,3]
    k = 2

    # Act
    result = most_frequent_k_elements(arr, k)

    # Assert
    assert set(result) == set([1,2])

def test_most_frequent_k_elements_single_arr():
    # Arrange
    arr = [1]
    k = 1 


    # Act
    result = most_frequent_k_elements(arr, k)

    # Act
    assert result == [1]

def test_most_frequent_k_elements_negative_number_case():
    # Arrange
    arr = [-1,-1,-1,-2,-5,-5,3,3,3,3,4]
    k = 3

    # Act
    result = most_frequent_k_elements(arr, k)

    # Assert
    assert set(result) == set([3,-1,-5])
