def instruction_list_equal(list1, list2):
    dict1 = [ins.__dict__ for ins in list1]
    dict2 = [ins.__dict__ for ins in list2]
    return dict1 == dict2
