from dmx import Universe
from dmx import RGBAPar


# TODO: Groups of lights
# TODO: Position information
u = Universe(1, "Studio")
floor_back_left_corner = RGBAPar(161, "Floor Back Left Corner")
u.add(floor_back_left_corner)
grid_back_left = RGBAPar(81, "Grid Back Left")
u.add(grid_back_left)
grid_front_left = RGBAPar(85, "Grid Front Left")
u.add(grid_front_left)
floor_back_right_corner = RGBAPar(33, "Floor Back Right Corner")
u.add(floor_back_right_corner)
grid_front_right = RGBAPar(37, "Grid Front Right")
u.add(grid_front_right)
grid_centre_left = RGBAPar(49, "Grid Centre Left")
u.add(grid_centre_left)
grid_centre_right = RGBAPar(97, "Grid Centre Right")
u.add(grid_centre_right)
grid_back_right = RGBAPar(113, "Grid Back Right")
u.add(grid_back_right)
floor_back_centre_left = RGBAPar(1, "Floor Back Centre Left")
u.add(floor_back_centre_left)
floor_back_centre_right = RGBAPar(129, "Floor Back Centre Right")
u.add(floor_back_centre_right)
grid_back_left_corner = RGBAPar(65, "Grid Back Left Corner")
u.add(grid_back_left_corner)

all = (
    floor_back_left_corner,
    floor_back_centre_right,
    floor_back_centre_right,
    floor_back_right_corner,
    grid_centre_left,
    grid_back_left_corner,
    grid_back_left,
    grid_back_right,
    grid_centre_right,
    grid_front_left,
    grid_front_right
)

floor = (
    floor_back_centre_left,
    floor_back_centre_right,
    floor_back_left_corner,
    floor_back_right_corner
)

grid = (
    grid_back_left,
    grid_back_left_corner,
    grid_back_right,
    grid_centre_left,
    grid_centre_right,
    grid_front_left,
    grid_front_right
)

back = (
    floor_back_centre_left,
    floor_back_centre_right,
    floor_back_left_corner,
    floor_back_right_corner,
    grid_back_left,
    grid_back_left_corner,
    grid_back_right
)

centre = (
    grid_centre_left,
    grid_centre_right
)

front = (
    grid_front_left,
    grid_front_right
)

left = (
    floor_back_centre_left,
    floor_back_left_corner,
    grid_back_left,
    grid_back_left_corner,
    grid_centre_left,
    grid_front_left
)

right = (
    floor_back_centre_right,
    floor_back_right_corner,
    grid_back_right,
    grid_centre_right,
    grid_front_right
)