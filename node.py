import util


class Node:
    def __init__(self, x_coor, y_coor, height, up, down, left, right, front, back):

        # to be converted to x and y via set_x_y func
        self.x_coor = x_coor
        self.y_coor = y_coor

        # normal
        self.h = height
        self.x = 0
        self.y = 0
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.front = front
        self.back = back


    def set_x_y(self, origin_x, origin_y):
        # convert to x,y coordinate
        self.x, self.y = util.convert_to_meter(origin_x, origin_y, self.x_coor, self.y_coor)





