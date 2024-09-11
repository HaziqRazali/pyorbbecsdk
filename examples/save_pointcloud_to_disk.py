# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.  
#  You may obtain a copy of the License at
#  
#      http:# www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import os
import cv2

import numpy as np
from plyfile import PlyData, PlyElement

from pyorbbecsdk import *

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)

"""
def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    if frames is None:
        return 0
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    
    #print(depth_data.shape) #(2073600,)
    width  = depth_frame.get_width()              # 1920
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
"""

def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    
    if frames is None:
        return 0
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
    width  = depth_frame.get_width()              # 1920
    height = depth_frame.get_height()           # 1080
    print(width, height, depth_data.shape)
    sys.exit()
        
    points = frames.get_point_cloud(camera_param)
    if len(points) == 0:
        print("no depth points")
        return 0

    # Create a structured numpy array directly from points assuming it's a list of lists
    points_array = np.array([tuple(point) for point in points], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    points_filename = os.path.join(save_points_dir, "points_{}.ply".format(depth_frame.get_timestamp()))

    el = PlyElement.describe(points_array, 'vertex')
    PlyData([el], text=True).write(points_filename)

    return 1

def save_color_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    if frames is None:
        return 0
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    #print("color_frame",color_frame.get_data().shape)
    #print("depth_frame",depth_frame.get_data().shape)
    #sys.exit()
        
    points = frames.get_color_point_cloud(camera_param)
    if len(points) == 0:
        print("no color points")
        return 0

    # Create a structured numpy array directly from color_points assuming it's a list of lists
    points_array = np.array([tuple(point) for point in points],
                            dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'u1'), ('green', 'u1'),
                                   ('blue', 'u1')])
    points_filename = os.path.join(save_points_dir, "color_points_{}.ply".format(depth_frame.get_timestamp()))

    el = PlyElement.describe(points_array, 'vertex')
    PlyData([el], text=True).write(points_filename)

    return 1


def main():
    pipeline = Pipeline()
    device = pipeline.get_device()
    device_info = device.get_device_info()
    device_pid = device_info.get_pid()
    config = Config()
    has_color_sensor = False
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, can not generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    depth_width = depth_profile.get_width()
    depth_height = depth_profile.get_height()
    print(f"Depth resolution: {depth_width} x {depth_height}") # [640, 576]
    print("depth profile: ", depth_profile) # depth profile:  <VideoStreamProfile: 640x576@15>
    
    config.enable_stream(depth_profile)
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile = profile_list.get_default_video_stream_profile()
            color_width = color_profile.get_width()
            color_height = color_profile.get_height()
            print(f"Color resolution: {color_width} x {color_height}") # [1920, 1080]
            print("color profile: ", color_profile) # color profile:  <VideoStreamProfile: 1920x1080@15>
            config.enable_stream(color_profile)
            
            if device_pid == 0x066B: 
                # goes in here
                # Femto Mega does not support hardware D2C, and it is changed to software D2C
                config.set_align_mode(OBAlignMode.SW_MODE)
            else:
                config.set_align_mode(OBAlignMode.HW_MODE)
            has_color_sensor = True
            
    except OBError as e:
        config.set_align_mode(OBAlignMode.DISABLE)
        print(e)

    #print("has_color_sensor",has_color_sensor) # True
    #sys.exit()
    
    pipeline.start(config)
    pipeline.enable_frame_sync()
    saved_color_cnt: int = 0
    saved_depth_cnt: int = 0
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            camera_param = pipeline.get_camera_param()
            
            #print(camera_param)
            """
            <OBCameraParam depth_intrinsic < fx=1123.87fy = 1123.03 cx =948.027 cy=539.649 width=1920 height=1080 > 
             depth_distortion < k1=0.0733382 k2=-0.101789 k3=0.041689 k4=0 k5=0 k6=0 p1=-0.000472246 p2=-0.00022513 > 
             rgb_intrinsic < fx=1123.87fy = 1123.03 cx =948.027 cy=539.649 width=1920 height=1080 > 
             rgb_distortion < k1=0.0733382 k2=-0.101789 k3=0.041689 k4=0 k5=0 k6=0 p1=-0.000472246 p2=-0.00022513 > 
             transform < rot=[1, 0, 0, 0, 1, 0, 0, 0, 1]
             transform=[0, 0, 0] 
            """
            
            saved_depth_cnt += save_points_to_ply(frames, camera_param)
            if has_color_sensor:
                saved_color_cnt += save_color_points_to_ply(frames, camera_param)
            if has_color_sensor:
                if saved_color_cnt >= 1 and saved_depth_cnt >= 1:
                    break
            elif saved_depth_cnt >= 1:
                break
        except OBError as e:
            print(e)
            break


if __name__ == "__main__":
    main()
