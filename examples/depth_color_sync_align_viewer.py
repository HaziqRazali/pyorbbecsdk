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
import argparse
import sys

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27


def main(argv):
    pipeline = Pipeline()
    config = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="align mode, HW=hardware mode,SW=software mode,NONE=disable align", type=str, default='HW')
    parser.add_argument("-s", "--enable_sync", help="enable sync", action="store_false", default=True)
    parser.add_argument("--save_filename", type=str, required=True)
    args = parser.parse_args()
    align_mode  = args.mode
    enable_sync = args.enable_sync
    
    print(f"align_mode: {align_mode}, enable_sync: {enable_sync}")
    
    try:
                
        # # # # # # # # # # # # # # # # # #
        # get and set color profile list  #
        # # # # # # # # # # # # # # # # # #
        
        # get color profile_list
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        #09/12 03:20:56.596796][info][376419][VideoSensor.cpp:386]  - {type: OB_STREAM_COLOR, format: OB_FORMAT_BGRA, width: 2560, height: 1440, fps: 30}
        #09/12 03:20:56.596799][info][376419][VideoSensor.cpp:386]  - {type: OB_STREAM_COLOR, format: OB_FORMAT_BGRA, width: 2560, height: 1440, fps: 25}
        
        if 1:
            # set a different color profile list
            color_profile = profile_list.get_video_stream_profile(1280, 720, OBFormat.MJPG, 15)
            config.enable_stream(color_profile)
            
        if 0:
            # set default color profile list
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
        
        # # # # # # # # # # # # # # # # # #
        # get and set depth profile list  #
        # # # # # # # # # # # # # # # # # ##
        
        # get depth profile
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        assert profile_list is not None
        #09/12 03:20:56.597067][info][376419][VideoSensor.cpp:386]  - {type: OB_STREAM_DEPTH, format: OB_FORMAT_Y16, width: 640, height: 576, fps: 15}
        #09/12 03:20:56.597069][info][376419][VideoSensor.cpp:386]  - {type: OB_STREAM_DEPTH, format: OB_FORMAT_Y16, width: 1024, height: 1024, fps: 15}
        
        # set depth profile
        depth_profile = profile_list.get_default_video_stream_profile()
        assert depth_profile is not None
        
        # color profile : 1920x1080@15_OBFormat.MJPG
        print("color profile : {}x{}@{}_{}".format(color_profile.get_width(),
                                                   color_profile.get_height(),
                                                   color_profile.get_fps(),
                                                   color_profile.get_format()))
        # depth profile : 640x576@15_OBFormat.Y16
        print("depth profile : {}x{}@{}_{}".format(depth_profile.get_width(),
                                                   depth_profile.get_height(),
                                                   depth_profile.get_fps(),
                                                   depth_profile.get_format()))
        #sys.exit()
                                                   
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return
    
    """
    align
    """
    
    device      = pipeline.get_device()
    device_info = device.get_device_info()
    device_pid  = device_info.get_pid()
    
    if align_mode == 'HW':
        if device_pid == 0x066B:
            # Femto Mega does not support hardware D2C, and it is changed to software D2C
            config.set_align_mode(OBAlignMode.SW_MODE)
        else:
            config.set_align_mode(OBAlignMode.HW_MODE)
    elif align_mode == 'SW':
        config.set_align_mode(OBAlignMode.SW_MODE)
    else:
        print("Cannot align!")
        sys.exit()
        #pass
        #config.set_align_mode(OBAlignMode.DISABLE)
    
    """
    sync
    """
    
    if enable_sync:
        try:
            pipeline.enable_frame_sync()
        except Exception as e:
            print(e)
    
    """
    start bag
    """
    
    try:
        pipeline.start(config)
        pipeline.start_recording(args.save_filename)
    except Exception as e:
        print(e)
        return
    
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
                            
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
                
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
                
            # covert to RGB format
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("failed to convert frame to image")
                continue

            width  = depth_frame.get_width()
            height = depth_frame.get_height()
            scale  = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_data = depth_data.astype(np.float32) * scale
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            
            # overlay color image on depth image
            depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)
            cv2.imshow("SyncAlignViewer ", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                pipeline.stop_recording()
                break
        except KeyboardInterrupt:
            pipeline.stop_recording()
            break
    
    """
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
                            
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
                
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
                
            # covert to RGB format
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("failed to convert frame to image")
                continue

            width  = depth_frame.get_width()
            height = depth_frame.get_height()
            scale  = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_data = depth_data.astype(np.float32) * scale
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            # overlay color image on depth image
            #depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)
            cv2.imshow("SyncAlignViewer ", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            pipeline.stop_recording()
            break
    """
    
    pipeline.stop()


if __name__ == "__main__":
    main(sys.argv[1:])
