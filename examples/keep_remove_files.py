import os
import shutil
import argparse
from glob import glob
from pathlib import Path

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--foldername", type=str, required=True, help="Folder name where the files are located")
    parser.add_argument("--mode", choices=["copy", "remove"], type=str, required=True)
    parser.add_argument("--start", type=int, required=True, help="Start index of the range")
    parser.add_argument("--stop", type=int, required=True, help="Stop index of the range (exclusive)")
    parser.add_argument("--step", type=int, required=True, help="Step size for the range")
    parser.add_argument("--output_folder", type=str, default="output", help="Folder where filtered files will be copied")
    args = parser.parse_args()
    
    # Load and sort the files (no need to parse filename!)
    rgb         = sorted(glob(os.path.join(args.foldername, "rgb", "*")))
    depth_image = sorted(glob(os.path.join(args.foldername, "depth_image", "*")))
    depth       = sorted(glob(os.path.join(args.foldername, "depth", "*")))
    point_cloud = sorted(glob(os.path.join(args.foldername, "point_cloud", "*")))
    
    # Create output folder if it doesn't exist
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)
    
    # Get the list of indices to copy/remove based on the range
    idxs = list(range(args.start, args.stop, args.step))
    
    if args.mode == "copy":
        print(f"Keeping files at indices: {idxs}")
        
        for i in idxs:
            if i < len(rgb):  # Safety check to avoid out-of-bounds errors
                # Copy RGB file
                color_dst = os.path.join(args.output_folder, "rgb", os.path.basename(rgb[i]))
                Path(os.path.dirname(color_dst)).mkdir(parents=True, exist_ok=True)
                shutil.copy(rgb[i], color_dst)

                # Copy depth image
                depth_dst = os.path.join(args.output_folder, "depth_image", os.path.basename(depth_image[i]))
                Path(os.path.dirname(depth_dst)).mkdir(parents=True, exist_ok=True)
                shutil.copy(depth_image[i], depth_dst)

                # Copy depth raw data
                raw_dst = os.path.join(args.output_folder, "depth", os.path.basename(depth[i]))
                Path(os.path.dirname(raw_dst)).mkdir(parents=True, exist_ok=True)
                shutil.copy(depth[i], raw_dst)

                # Copy point cloud
                cloud_dst = os.path.join(args.output_folder, "point_cloud", os.path.basename(point_cloud[i]))
                Path(os.path.dirname(cloud_dst)).mkdir(parents=True, exist_ok=True)
                shutil.copy(point_cloud[i], cloud_dst)

                print(f"Copied files at index {i}")

    elif args.mode == "remove":
        print(f"Removing files at indices: {idxs}")
        
        for i in idxs:
            if i < len(rgb):  # Safety check to avoid out-of-bounds errors
                os.remove(rgb[i])
                os.remove(depth_image[i])
                os.remove(depth[i])
                os.remove(point_cloud[i])
                print(f"Removed files at index {i}")

