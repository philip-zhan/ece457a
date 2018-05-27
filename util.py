# magic number
# by calculation, 10^-5 latitude or 0.00001 is 1.112 meter
#                 10^-5 longitude or 0.00001 is 0.807 meter
# since the region is pretty small comparing to the whole earth surface, we can stick to these magic number
# source https://www.movable-type.co.uk/scripts/latlong.html


def convert_to_meter(origin_x, origin_y, dest_x, dest_y):
    return (dest_x - origin_x) * 1.112, (dest_y - origin_y) * 0.807
