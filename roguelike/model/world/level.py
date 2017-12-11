import random


class Level:
    level_no = 0
    obj_no = 0
    a_count = [10, 15, 20, 25, 30, 25, 20, 15, 10, 30]
    b_count = [3, 5, 10, 10, 15, 15, 20, 20, 20, 25, 25]
    c_count = [2, 3, 5, 10, 10, 10, 15, 15, 20, 25]
    d_count = [1, 2, 2, 2, 3, 3, 3, 4, 5, 5]
    room_count = [5, 10, 10, 15, 15, 10, 15, 15, 10]
    random_connections_count = [0, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, level_no):
        self.level_no = level_no
        self.obj_no = random.randint(1, 3)
