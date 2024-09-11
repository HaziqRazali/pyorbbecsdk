import sys
from pyorbbecsdk import Pipeline, Config, FrameSet

def count_frames_in_bag(bag_file):
    pipeline = Pipeline("./test.bag")
    pipeline.start()
    
    try:
        frame_count = 0
        
        while True:
            frames: FrameSet = pipeline.wait_for_frames(5000)
            if frames is None:
                break
            frame_count += 1
        
        pipeline.stop()
        return frame_count
    
    except Exception as e:
        print(e)
        pipeline.stop()
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_frames.py <path_to_bag_file>")
        sys.exit(1)
    
    bag_file = sys.argv[1]
    total_frames = count_frames_in_bag(bag_file)
    
    if total_frames is not None:
        print(f"Total number of frames in {bag_file}: {total_frames}")
    else:
        print(f"Failed to count frames in {bag_file}")
