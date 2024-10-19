
python keep_remove_files.py --mode keep --keep "range(40, 170, 5)" \
--foldername "/home/haziq/datasets/collab_ai/data/recordings/camera1/rotating_checkerboard/" \
--output_folder "/home/haziq/datasets/collab_ai/data/recordings/camera1/rotating_checkerboard_filtered/"

python keep_remove_files.py --mode keep --keep "range(40, 120, 1)" \
--foldername "/home/haziq/datasets/collab_ai/data/recordings/camera1/soya_milk_test/" \
--output_folder "/home/haziq/datasets/collab_ai/data/recordings/camera1/soya_milk_test_filtered/"

python examples/keep_remove_files.py --mode keep --keep "range(20, 62, 1)" \
--foldername "/home/haziq/datasets/collab_ai/data/recordings/camera1/soya_milk_on_table/" \
--output_folder "/home/haziq/datasets/collab_ai/data/recordings/camera1/soya_milk_on_table_filtered/"

python examples/keep_remove_files.py --mode keep --keep "range(20, 51, 1)" \
--foldername "/home/haziq/datasets/collab_ai/data/recordings/camera1/cup_on_table/" \
--output_folder "/home/haziq/datasets/collab_ai/data/recordings/camera1/cup_on_table_filtered/"

python examples/keep_remove_files.py --mode keep --keep "range(20, 57, 1)" \
--foldername "/home/haziq/datasets/collab_ai/data/recordings/camera1/final_test_seq/" \
--output_folder "/home/haziq/datasets/collab_ai/data/recordings/camera1/final_test_seq_filtered/"