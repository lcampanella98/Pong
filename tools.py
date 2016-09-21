def is_point_within_rect(point, rect):
    r_pos = (rect[0], rect[1])
    r_width = rect[2]
    r_height = rect[3]
    return r_pos[0] <= point[0] <= r_pos[0] + r_width and r_pos[1] <= point[1] <= r_pos[1] + r_height


def are_rectangles_colliding(rect1, rect2):
    x_collide = rect2[0] <= rect1[0] <= rect2[0] + rect2[2] or rect2[0] <= rect1[0] + rect1[2] <= rect2[0] + rect2[2] \
                or rect1[0] <= rect2[0] <= rect1[0] + rect1[2] or rect1[0] <= rect2[0] + rect2[2] <= rect1[0] + rect1[2]
    if not x_collide:
        return False
    y_collide = rect2[1] <= rect1[1] <= rect2[1] + rect2[3] or rect2[1] <= rect1[1] + rect1[3] <= rect2[1] + rect2[3] \
                or rect1[1] <= rect2[1] <= rect1[1] + rect1[3] or rect1[1] <= rect2[1] + rect2[3] <= rect1[1] + rect1[3]
    if not y_collide:
        return False
    return True


def is_rect_within_other_rect(inside_rect, outside_rect):
    x_check = outside_rect[0] <= inside_rect[0] and inside_rect[0] + inside_rect[2] <= outside_rect[0] + outside_rect[2]
    if not x_check:
        return False
    y_check = outside_rect[1] <= inside_rect[1] and inside_rect[1] + inside_rect[3] <= outside_rect[1] + outside_rect[3]
    if not y_check:
        return False
    return True
