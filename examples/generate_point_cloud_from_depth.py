import os
import cv2

import numpy as np
from plyfile import PlyData, PlyElement

from pyorbbecsdk import *

def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    if frames is None:
        return 0
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
        
    #print(depth_data.shape) #(2073600,)
    width = depth_frame.get_width()              # 1920
    height = depth_frame.get_height()           # 1080
    print(width, height)
    sys.exit()
    
    depth_data = depth_data.reshape((height, width))
    #print(depth_data.dtype) # uint16
    cv2.imwrite("./point_clouds/depth_image.png",depth_data, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    
    points = frames.get_point_cloud(camera_param)
    #print("points",points.shape) # [2073600, 3] == [1080,1920,3]
    #sys.exit()
    np.savetxt("./point_clouds/point_cloud.csv", points, fmt='%.10f', delimiter=',', header='x,y,z', comments='')
    
    # doesnt work
    #import inspect
    #source_file = inspect.getfile(frames.get_point_cloud)
    #print(source_file)
    
    if len(points) == 0:
        print("no depth points")
        return 0

    # Create a structured numpy array directly from points assuming it's a list of lists
    points_array = np.array([tuple(point) for point in points], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    points_filename = os.path.join(save_points_dir, "points_{}.ply".format(depth_frame.get_timestamp()))

    el = PlyElement.describe(points_array, 'vertex')
    PlyData([el], text=True).write(points_filename)
    
    sys.exit()

    return 1
    
if __name__ == "__main__":

    depth_image = cv2.imread("./point_clouds/depth_image.png", cv2.IMREAD_UNCHANGED)
    
    points = frames.get_point_cloud(camera_param)