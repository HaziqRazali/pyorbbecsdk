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

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27


def playback_state_callback(state):
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")


def get_color_frame(frames):
    color_frame = frames.get_color_frame()
    if color_frame is None:
        return None
    color_image = frame_to_bgr_image(color_frame)
    if color_image is None:
        print("failed to convert frame to image")
        return None
    return color_image


def main():
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    playback.set_playback_state_callback(playback_state_callback)
    device_info = playback.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    pipeline.start()
    
    i = 0
    try:
        while True:
            
            # get frame from bag
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            # convert to rgb
            color_image = get_color_frame(frames)
            
            # save
            filename = f"./examples/data/camera1/{i:04d}.png"
            print(f"Writing frame {filename}")
            cv2.imwrite(filename, color_image)
            
            # increment count
            i += 1
            
            # wait
            key = cv2.waitKey(1)
                        
            if key == ord('q') or key == ESC_KEY:
                break
            
    except KeyboardInterrupt:
        if pipeline:
            pipeline.stop()
            
if __name__ == "__main__":
    main()
