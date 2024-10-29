
python3 examples/depth_color_sync_align_viewer.py --save_filename "./test.bag"
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/cam_K.txt"
python3 examples/depth_color_sync_align_viewer.py --save_filename "./bags/rotating_checkerboard.bag"

# fps sanity checks
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_15/bags/0.bag"
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_25/bags/0.bag"
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/fps_30/bags/0.bag"

python3 examples/depth_color_sync_align_viewer.py \
--save_filename "/home/haziq/datasets/collab_ai/data/recordings/standing_rotating_wings/bags/0.bag" \
--save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/standing_rotating_wings/cam_K.txt"

# moving_occluding_objects
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects/cam_K.txt"
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects/" --threads 1
python3 examples/keep_remove_files.py --mode keep --keep "range(55, 451, 1)" --foldername "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects/" --output_folder "/home/haziq/datasets/collab_ai/data/recordings/moving_occluding_objects_filtered/"

# cooking_sample
python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample/cam_K.txt"
python3 examples/extract_bag_file.py --bag_filename "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample/bags/0.bag" --save_folder "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample/" --threads 1
python3 examples/keep_remove_files.py --mode keep --keep "range(65, 466, 1)" --foldername "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample/" --output_folder "/home/haziq/datasets/collab_ai/data/recordings/cooking_sample_filtered/"

python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/test/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/test/cam_K.txt"

python3 examples/depth_color_sync_align_viewer.py --save_filename "/home/haziq/datasets/collab_ai/data/recordings/standing_action/bags/0.bag" --save_cam_K_filename "/home/haziq/datasets/collab_ai/data/recordings/standing_action/cam_K.txt"