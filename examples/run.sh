
#################### 1) to record data to a .bag file 
# todo
# - args to set resolution and fps
# - check if align works if RGB and D have different fps / resolution
python3 examples/depth_color_sync_align_viewer.py --color_fps 30 --depth_fps 30 --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/cam_K.txt"

#################### 2) review recording
python3 examples/playback_original.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag"

#################### 3) extract rgb, depth, and point clouds to folder
# todo
# - can we skip this and have FoundationPose directly work on on the bag file ? Probably not
# - automatically progress after several messages of "[03/14 18:43:59.162066][warning][48326][Pipeline.cpp:377] Wait for frame timeout, you can try to increase the wait time! current timeout=5000" ?
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0" --threads 1

#################### 4) copy frames f1 to f2 "range(f1, f2, 1) because the first f1 frames are usually corrupted not sure why
# todo
# - do not clone folder for the final dataset
python3 examples/keep_remove_files.py --mode copy --start 1 --stop 102 --step 1 --foldername "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0" --output_folder "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0_filtered"

#################### fps sanity checks
python3 examples/depth_color_sync_align_viewer.py --color_fps 15 --depth_fps 15  --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/cam_K.txt"
python3 examples/depth_color_sync_align_viewer.py --color_fps 25 --depth_fps 25  --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_25/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_25/cam_K.txt"
python3 examples/depth_color_sync_align_viewer.py --color_fps 30 --depth_fps 30  --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/cam_K.txt"
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/fps_15/bags/0" --threads 1
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_25/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/fps_25/bags/0" --threads 1
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0" --threads 1