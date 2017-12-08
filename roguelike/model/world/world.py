import random
from typing import List

from roguelike.model.world.tile import Tile
from roguelike.utils import pathfinding


class World:
    def __init__(self, width, height, default_tile_type='V'):
        """
        :param width: amount of tiles in x axis
        :param height: amount of tiles in y axis
        """
        self.width = width
        self.height = height
        self.room_list = []
        self.is_room_connected = []
        self.corridor_list = []
        self.tiles: List[List[Tile]] = [[Tile.on_position(w, h, default_type=default_tile_type)
                                         for h in range(height)] for w in range(width)]

    def gen_empty_world(self):
        for w in range(self.width):
            for h in range(self.height):
                self.tiles[w][h].type = "V"

    def gen_room(self, minroomw, minroomh, maxroomw, maxroomh):
        roomw = random.randint(minroomw, maxroomw)
        roomh = random.randint(minroomh, maxroomh)
        x = random.randint(1, self.width - roomw - 1)
        y = random.randint(1, self.height - roomh - 1)

        return [roomw, roomh, x, y]

    def is_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:

            if (x < (current_room[2] + current_room[0]) and
                        current_room[2] < (x + w) and
                        y < (current_room[3] + current_room[1]) and
                        current_room[3] < (y + h)):
                return True

        return False

    def gen_rooms(self, maxrooms, overlapping):
        self.room_list = []
        self.is_room_connected = []
        if (overlapping == True):
            for i in range(maxrooms):
                self.room_list.append(self.gen_room(5, 5, max(5, self.width / 10), max(5, self.height / 10)))
                self.is_room_connected.append(False)
        else:
            i = 0
            count = 0
            while (count < 5 * maxrooms):
                room = self.gen_room(5, 5, max(5, self.width / 10), max(5, self.height / 10))
                ol = False
                if (i > 0):
                    ol = self.is_overlapping(room, self.room_list)
                    count = count + 1
                    print(ol)
                if (ol == False):
                    self.room_list.append(room)
                    self.is_room_connected.append(False)
                    i = i + 1
                if (i >= maxrooms):
                    break
        for r in self.room_list:
            for x in range(r[2], r[2] + r[0]):
                for y in range(r[3], r[3] + r[1]):
                    self.tiles[x][y].type = "R"

    def gen_corridor_between_points(self, x1, x2, y1, y2, join='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        if join is 'either' and {0, 1}.intersection({x1, x2, y1, y2}):
            join_type = 'bottom'
        elif join is 'either' and {self.width - 1, self.width - 2}.intersection({x1, x2}) or {self.height - 1,
                                                                                              self.height - 2}.intersection(
                {y1, y2}):
            join_type = 'top'
        elif join is 'either':
            join_type = random.choice(['top', 'bottom'])
        else:
            join_type = join
        if join_type is 'top':
            return [(x1, y1), (x1, y2), (x2, y2)]
        elif join_type is 'bottom':
            return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room1, room2, join='either'):
        sorted_rooms = [room1, room2]
        sorted_rooms.sort(key=lambda x_y: x_y[0])

        x1 = sorted_rooms[0][2]
        y1 = sorted_rooms[0][3]
        w1 = sorted_rooms[0][0]
        h1 = sorted_rooms[0][1]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_rooms[1][2]
        y2 = sorted_rooms[1][3]
        w2 = sorted_rooms[1][0]
        h2 = sorted_rooms[1][1]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
            corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2)
            self.corridor_list.append(corridors)

        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1

            corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2)
            self.corridor_list.append(corridors)

        else:
            if join is 'either':
                join_type = random.choice(['top', 'bottom'])
            else:
                join_type = join

            if join_type is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.gen_corridor_between_points(jx1, jx2, jy1, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_corridors(self, random_connections):
        self.corridor_list = []

        for i in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[i], self.room_list[i + 1])

        for i in range(random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        for c in self.corridor_list:
            x1, y1 = c[0]
            x2, y2 = c[1]
            for w in range(abs(x1 - x2) + 1):
                for h in range(abs(y1 - y2) + 1):
                    self.tiles[min(x1, x2) + w][min(y1, y2) + h].type = "C"
                    if abs(x2 - x1) == 0:
                        self.tiles[min(x2, x1) + w - 1][min(y2, y1) + h].type = "C"
                        self.tiles[min(x2, x1) + w + 1][min(y2, y1) + h ].type = "C"
                    elif abs(y2 - y1) == 0:
                        self.tiles[min(x2, x1) + w][min(y2, y1) + h -1].type = "C"
                        self.tiles[min(x2, x1) + w][min(y2, y1) + h +1].type = "C"

            if len(c) == 3:
                x3, y3 = c[2]
                for w in range(abs(x2 - x3) + 1):
                    for h in range(abs(y2 - y3) + 1):
                        self.tiles[min(x2, x3) + w][min(y2, y3) + h].type = "C"
                        if abs(x2-x3)==0:
                            self.tiles[min(x2, x3) + w -1][min(y2, y3) + h].type = "C"
                            self.tiles[min(x2, x3) + w +1][min(y2, y3) + h].type = "C"
                        elif abs(y2-y3)==0:
                            self.tiles[min(x2, x3) + w ][min(y2, y3) + h -1].type = "C"
                            self.tiles[min(x2, x3) + w][min(y2, y3) + h +1].type = "C"

    def gen_walls(self):
        for col in range(1, self.width - 1):
            for row in range(1, self.height - 1):
                if self.tiles[col][row].type == "R" or self.tiles[col][row].type == "C":
                    if self.tiles[col - 1][row - 1].type == "V":
                        self.tiles[col - 1][row - 1].type = "W"

                    if self.tiles[col - 1][row].type == "V":
                        self.tiles[col - 1][row].type = "W"

                    if self.tiles[col - 1][row + 1].type == "V":
                        self.tiles[col - 1][row + 1].type = "W"

                    if self.tiles[col][row - 1].type == "V":
                        self.tiles[col][row - 1].type = "W"

                    if self.tiles[col][row + 1].type == "V":
                        self.tiles[col][row + 1].type = "W"

                    if self.tiles[col + 1][row - 1].type == "V":
                        self.tiles[col + 1][row - 1].type = "W"

                    if self.tiles[col + 1][row].type == "V":
                        self.tiles[col + 1][row].type = "W"

                    if self.tiles[col + 1][row + 1].type == "V":
                        self.tiles[col + 1][row + 1].type = "W"

    def check_room_connection(self, r):
        for x in range(r[2] - 1, r[2] + r[0] + 1):
            for y in range(r[3] - 1, r[3] + r[1] + 1):
                if self.tiles[x][y].type == "C":
                    if(self.is_corner(r,x,y)):
                        if self.tiles[x+1][y].type=="V" and self.tiles[x][y+1].type=="V" and self.tiles[x+1][y+1].type=="R":
                            self.tiles[x+1][y].type = "C"
                            self.tiles[x][y+1].type = "C"
                        elif self.tiles[x-1][y].type=="V" and self.tiles[x][y+1].type=="V" and self.tiles[x-1][y+1].type=="R":
                            self.tiles[x-1][y].type = "C"
                            self.tiles[x][y+1].type = "C"
                        elif self.tiles[x-1][y].type=="V" and self.tiles[x][y-1].type=="V" and self.tiles[x-1][y-1].type=="R":
                            self.tiles[x-1][y].type = "C"
                            self.tiles[x][y-1].type = "C"
                        elif self.tiles[x+1][y].type=="V" and self.tiles[x][y-1].type=="V" and self.tiles[x+1][y-1].type=="R":
                            self.tiles[x+1][y].type = "C"
                            self.tiles[x][y-1].type = "C"
                    return True
        return False

    def check_connections(self):
        i = 0
        for r in self.room_list:
            self.is_room_connected[i] = self.check_room_connection(r)
            i = i + 1

        for i in range(0, len(self.room_list)):
            false_count = 0
            while self.is_room_connected[i] == False:
                false_count = false_count + 1
                r2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
                self.join_rooms(self.room_list[i], r2, 'either')
                self.is_room_connected[i] = self.check_room_connection(r)
                if false_count > 10:
                    for i in range(0, len(self.room_list)):
                        false_count = 0
                        while self.is_room_connected[i] == False:
                            false_count = false_count + 1
                            r2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
                            self.join_rooms(self.room_list[i], r2, 'either')
                            self.is_room_connected[i] = self.check_room_connection(r)
                            if false_count > 10:
                                for r in self.room_list:
                                    if r != self.room_list[i]:
                                        self.join_rooms(self.room_list[i], r, 'either')
                                        self.is_room_connected[i] = self.check_room_connection(r)
                                        if self.is_room_connected[i] == True:
                                            break
                                break

    def repaint_corridors(self):
        for c in self.corridor_list:
            x1, y1 = c[0]
            x2, y2 = c[1]
            for w in range(abs(x1 - x2) + 1):
                for h in range(abs(y1 - y2) + 1):
                    self.tiles[min(x1, x2) + w][min(y1, y2) + h].type = "C"
                    if abs(x2 - x1) == 0:
                        self.tiles[min(x2, x1) + w - 1][min(y2, y1) + h].type = "C"
                        self.tiles[min(x2, x1) + w + 1][min(y2, y1) + h ].type = "C"
                    elif abs(y2 - y1) == 0:
                        self.tiles[min(x2, x1) + w][min(y2, y1) + h -1].type = "C"
                        self.tiles[min(x2, x1) + w][min(y2, y1) + h +1].type = "C"

            if len(c) == 3:
                x3, y3 = c[2]
                for w in range(abs(x2 - x3) + 1):
                    for h in range(abs(y2 - y3) + 1):
                        self.tiles[min(x2, x3) + w][min(y2, y3) + h].type = "C"
                        if abs(x2-x3)==0:
                            self.tiles[min(x2, x3) + w -1][min(y2, y3) + h].type = "C"
                            self.tiles[min(x2, x3) + w +1][min(y2, y3) + h].type = "C"
                        elif abs(y2-y3)==0:
                            self.tiles[min(x2, x3) + w ][min(y2, y3) + h -1].type = "C"
                            self.tiles[min(x2, x3) + w][min(y2, y3) + h +1].type = "C"


    def is_corner(self, r, x, y):
        return (x == r[2] - 1 and y == r[3] - 1) or (x == r[2] - 1 and y == r[3] + r[1] + 1) or (x == r[2] + r[0] + 1 and y == r[3] + r[1] + 1) or (x == r[2] + r[0] + 1 and y == r[3] - 1)

    def check_for_modules(self):
        is_connected = [[False for i in range(len(self.room_list)-1)] for j in range(len(self.room_list)-1)]
        for i in range (0, len(self.room_list)-1):
            for j in range (i,len(self.room_list)-1):
                try:
                    r1=self.room_list[i]
                    r2=self.room_list[j]
                    for k in range (0,i-1):
                        if is_connected[k][i]==True and is_connected[k][j]==True:
                            is_connected[i][j]=True
                    if is_connected[i][j] == False:
                        pathfinding.A_star_pathfinding(self.tiles[r1[2]][r1[3]],self.tiles[r2[2]][r2[3]],self)
                        is_connected[i][j]=True
                except pathfinding.PathNotFound as e:
                    self.join_rooms(self.room_list[i], self.room_list[j], 'either')
                    is_connected[i][j]=True
                    pass

    def gen_level(self, maxrooms, overlapping, random_connections):
        self.gen_empty_world()
        self.gen_rooms(maxrooms, overlapping)
        self.gen_corridors(random_connections)
        self.check_connections()
        self.repaint_corridors()
        self.check_for_modules()
        self.repaint_corridors()
        self.gen_walls()

    def get_room(self,x,y):
        for i in range(0, len(self.room_list) - 1):
            r = self.room_list[i]
            if x>=r[2] and x<=r[2]+r[0] and y>=r[3] and y<=r[3]+r[1]:
                return i
        return -1
