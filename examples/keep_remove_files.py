import os
import ast
import shutil
import argparse

from glob import glob
from pathlib import Path
#from natsort import natsorted

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--foldername", type=str, required=True, help="Folder name where the files are located")
    parser.add_argument("--mode", choices=["keep", "remove"], type=str, required=True)
    parser.add_argument("--keep", type=str, required=True, help="Provide a list of integers or a range, e.g., 'range(40, 170, 5)' or '[114, 116]'")
    parser.add_argument("--output_folder", type=str, default="output", help="Folder where filtered files will be copied")
    args = parser.parse_args()
    
    rgb         = sorted(glob(os.path.join(args.foldername, "rgb", "*")))
    depth_image = sorted(glob(os.path.join(args.foldername, "depth_image", "*")))
    depth       = sorted(glob(os.path.join(args.foldername, "depth", "*")))
    point_cloud = sorted(glob(os.path.join(args.foldername, "point_cloud", "*")))
    
    # Create output folder if it doesn't exist
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)
    
    # Check if --keep is a range expression
    if args.keep.startswith("range"):
        try:
            # Manually evaluate the range string (e.g., "range(40, 170, 5)")
            keep = list(eval(args.keep))  # Convert range to list
        except Exception as e:
            print(f"Error processing range: {e}")
            exit(1)
    else:
        # Parse the --keep argument as a list using ast.literal_eval
        try:
            keep = list(ast.literal_eval(args.keep))
        except (ValueError, SyntaxError):
            print("Invalid format for --keep. Please input a valid list or range.")
            exit(1)
        
    if args.mode == "keep":
        
        # Get the indices corresponding to the filenames based on the parsed keep list        
        idxs = [i for i, img in enumerate(rgb) if int(os.path.basename(img).split('-')[0].lstrip('0')) in keep]
        
        print(f"Keeping files at indices: {idxs}")
        
        # Copy selected files from each folder (rgb, depth_image, depth, point_cloud)
        for i in idxs:
            # Copy color image
            color_src = rgb[i]
            color_dst = os.path.join(args.output_folder, "rgb", os.path.basename(color_src))
            Path(os.path.dirname(color_dst)).mkdir(parents=True, exist_ok=True)  # Create directory if not exists
            shutil.copy(color_src, color_dst)
            print(f"Copied {color_src} to {color_dst}")
            
            # Copy depth image
            depth_src = depth_image[i]
            depth_dst = os.path.join(args.output_folder, "depth_image", os.path.basename(depth_src))
            Path(os.path.dirname(depth_dst)).mkdir(parents=True, exist_ok=True)  # Create directory if not exists
            shutil.copy(depth_src, depth_dst)
            print(f"Copied {depth_src} to {depth_dst}")
            
            # Copy depth raw data
            raw_src = depth[i]
            raw_dst = os.path.join(args.output_folder, "depth", os.path.basename(raw_src))
            Path(os.path.dirname(raw_dst)).mkdir(parents=True, exist_ok=True)  # Create directory if not exists
            shutil.copy(raw_src, raw_dst)
            print(f"Copied {raw_src} to {raw_dst}")
            
            # Copy point cloud
            cloud_src = point_cloud[i]
            cloud_dst = os.path.join(args.output_folder, "point_cloud", os.path.basename(cloud_src))
            Path(os.path.dirname(cloud_dst)).mkdir(parents=True, exist_ok=True)  # Create directory if not exists
            shutil.copy(cloud_src, cloud_dst)
            print(f"Copied {cloud_src} to {cloud_dst}")
            print()