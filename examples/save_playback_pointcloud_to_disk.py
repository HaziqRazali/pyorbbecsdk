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
import sys
import cv2

import numpy as np
from plyfile import PlyData, PlyElement

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27

def get_color_frame(frames):
    color_frame = frames.get_color_frame()
    if color_frame is None:
        return None
    color_image = frame_to_bgr_image(color_frame)
    if color_image is None:
        print("failed to convert frame to image")
        return None
    return color_image

def print_methods(obj):
    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("__")]
    for method in methods:
        print(method)

def playback_state_callback(state):
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")

save_points_dir = os.path.join(os.getcwd(), "data/point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)

def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam, i) -> int:
    
    if frames is None:
        return 0

    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        print(f"Frame {i} has no depth image")
        return

    width  = depth_frame.get_width()    # 1920
    height = depth_frame.get_height()   # 1080

    color_image = get_color_frame(frames)
    if color_image is None:
        print(f"Frame {i} has no color image")
        return

    points = frames.get_point_cloud(camera_param)
    if len(points) == 0:
        print(f"Frame {i} has no depth points")
        return

    # Create a structured numpy array directly from points assuming it's a list of lists
    points_array = np.array([tuple(point) for point in points], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    points_filename = os.path.join(save_points_dir, "points_{}.ply".format(depth_frame.get_timestamp()))

    el = PlyElement.describe(points_array, 'vertex')
    PlyData([el], text=True).write(points_filename)

def main():
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    playback.set_playback_state_callback(playback_state_callback)
    device_info = playback.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    pipeline.start()

    """
    frames_list = []
     try:
        while True:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            frames_list.append(frames)
    print(len(frames_list))
    sys.exit()
    """
    
    frames_list = []
    try:
        while True:
            frames: FrameSet = pipeline.wait_for_frames(5000)
            if frames is None:
                continue
            frames_list.append(frames)
            key = cv2.waitKey(1000)
            if key == ord('q') or key == ESC_KEY:
                break
    except KeyboardInterrupt:
        if pipeline:
            pipeline.stop()
    print("Finished loading frames.")
    print(len(frames_list))
    
    # Stop the pipeline after loading frames
    pipeline.stop()
    
    """frames_list = []
    i = 0
    try:
        while True:
            frames = pipeline.wait_for_frames(5000)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                print(f"Frame {i} has missing depth")
                continue
            frames_list.append(frames)
            key = cv2.waitKey(1000)
            print(f"Loading Frame {i}")
            i += 1
            if key == ord('q') or key == ESC_KEY:
                print("Stopping pipeline.")
                break
    except KeyboardInterrupt:
        print("Loading stopped by user.")
    print("Finished loading frames.")
    print(len(frames_list))"""
    
    for i in range(len(frames_list)):
        print(f"Processing Frame {i}")
        save_points_to_ply(frames_list[i], camera_param, i)
    sys.exit()

    """
    try:
        while True:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            save_points_to_ply(frames, camera_param)
    except KeyboardInterrupt:
        print("Stopping pipeline.")
        pipeline.stop()
    """

if __name__ == "__main__":
    main()
