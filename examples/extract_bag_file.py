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
from pathlib import Path
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

def playback_state_callback(state):
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")

def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam, i) -> int:
    
    print(f"Saving frame {i} point_cloud to file")
    
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_folder", type=str, required=True)
    args = parser.parse_args()
    
    # create save folder
    Path(os.path.join(args.save_folder,"depth_raw")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(args.save_folder,"depth_image")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(args.save_folder,"color_image")).mkdir(parents=True, exist_ok=True)
    
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    playback.set_playback_state_callback(playback_state_callback)
    device_info = playback.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    pipeline.start()

    """
    store every item in the bag into a separate list
    - this prevents 
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
                pipeline.stop()
                break
    except KeyboardInterrupt:
        if pipeline:
            pipeline.stop()
    print(f"Finished loading {len(frames_list)} frames")
    pipeline.stop()
        
    """
    extract the color, depth, and cloud data of every item
    """
        
    for i in range(len(frames_list)):
        
        # extract cloud
        #save_points_to_ply(frames_list[i], camera_param, i)
        
        print(f"Processing Frame {i}")
        frames = frames_list[i]
    
        if frames is None:
            continue

        depth_frame = frames.get_depth_frame()
        if depth_frame is None:
            print(f"Frame {i} has no depth image")
            continue

        color_image = get_color_frame(frames)
        if color_image is None:
            print(f"Frame {i} has no color image")
            continue

        points = frames.get_point_cloud(camera_param)
        if len(points) == 0:
            print(f"Frame {i} has no depth points")
            continue

        # assert dimensions
        depth_width, depth_height   = depth_frame.get_width(), depth_frame.get_height()  # 1920, 1080
        color_width, color_height   = color_image.shape[0], color_image.shape[1]
        assert depth_width == color_width
        assert depth_height == color_height

        # save point cloud
        points_array = np.array([tuple(point) for point in points], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
        points_filename = os.path.join(save_points_dir, "points_{}.ply".format(depth_frame.get_timestamp()))
        el = PlyElement.describe(points_array, 'vertex')
        PlyData([el], text=True).write(points_filename)
        
        # save depth
        depth_data  = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_raw   = depth_data.reshape((height, width))         
        depth_image = depth_raw.astype(np.float32) * scale
        depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
        cv2.imwrite(os.path.join(args.save_folder, f"depth_raw_{i}.png"), depth_raw)
        cv2.imwrite(os.path.join(args.save_folder, f"depth_image_{i}.png"), depth_image)
        
        # save color
        cv2.imwrite(os.path.join(args.save_folder, f"color_image_{i}.png"), color_image)
        
    sys.exit()

if __name__ == "__main__":
    main()
