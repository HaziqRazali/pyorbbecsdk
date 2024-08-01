import os
import cv2
import numpy as np
import open3d as o3d

from glob import glob

import sys
sys.path.insert(0, "/home/haziq/datasets/collab_ai/my_scripts/")
from utils import *

def undistort_depth_image(depth_image, intrinsic, dist_coeffs):
    # Camera matrix
    K = np.array([[intrinsic['fx'], 0, intrinsic['cx']],
                  [0, intrinsic['fy'], intrinsic['cy']],
                  [0, 0, 1]])
    
    # Distortion coefficients
    dist_coeffs = np.array([dist_coeffs['k1'], dist_coeffs['k2'], dist_coeffs['p1'], dist_coeffs['p2'], dist_coeffs['k3']])
    
    # Undistort
    undistorted_image = cv2.undistort(depth_image, K, dist_coeffs)
    return undistorted_image

def depth_to_point_cloud(depth_image, fx, fy, cx, cy):
    height, width = depth_image.shape
    i, j = np.meshgrid(np.arange(width), np.arange(height), indexing='xy')
    z = depth_image
    #z = depth_image / 1000.0  # Convert from millimeters to meters if necessary
    x = (i - cx) * z / fx
    y = (j - cy) * z / fy
    points = np.stack((x, y, z), axis=-1)
    return points

def visualize_point_cloud(points):

    # Convert numpy array to open3d point cloud
    points_reshaped = points.reshape(-1, 3)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_reshaped)
    
    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

if __name__ == "__main__":
    
    """
    # load depth image
    depth_image = cv2.imread("./point_clouds/depth_image.png", cv2.IMREAD_UNCHANGED)
    assert depth_image.dtype == np.uint16
    depth_image = depth_image.astype(np.float32)
    print(depth_image.shape)
    
    # clean up depth image
    depth_image = erode_depth(depth_image, radius=2, device='cuda')
    #depth_image = bilateral_filter_depth(depth_image, radius=2, device='cuda') # [1080, 1920]
            
    # Camera intrinsic parameters
    intrinsic = {
        'fx': 1123.87,
        'fy': 1123.03,
        'cx': 948.027,
        'cy': 539.649
    }
    
    # Camera distortion coefficients
    dist_coeffs = {
        'k1': 0.0733382,
        'k2': -0.101789,
        'p1': -0.000472246,
        'p2': -0.00022513,
        'k3': 0.041689
    }
    
    # Undistort depth image
    undistorted_depth_image = undistort_depth_image(depth_image, intrinsic, dist_coeffs)
    
    # Project depth image to 3D point cloud
    generated_points = depth_to_point_cloud(undistorted_depth_image, intrinsic['fx'], intrinsic['fy'], intrinsic['cx'], intrinsic['cy'])
    print("Generated points shape:", generated_points.shape)
    """
    
    # load point cloud
    point_cloud_filenames = sorted(glob(os.path.join("./point_clouds","*")))
    point_cloud = o3d.io.read_point_cloud(point_cloud_filenames[80])
    o3d.visualization.draw_geometries([point_cloud])
    
    #loaded_points = np.loadtxt("./point_clouds/point_cloud.csv", delimiter=',', skiprows=1)
    #loaded_points = np.reshape(loaded_points,[-1,3])
    #loaded_points = np.reshape(loaded_points,[1080,1920,3])
    
    #visualize_point_cloud(generated_points)
    #visualize_point_cloud_pyvista(generated_points)
    #save_point_cloud_to_ply(generated_points, "./point_clouds/generated_points.ply")
    
    """
    # Verify with loaded points
    for i in range(300, 1080, 1):  # 360
        for j in range(300, 1920, 1): # 640
            print(f"Loaded point ({i}, {j}): {points[i, j]}")
            print(f"Generated point ({i}, {j}): {generated_points[i, j]}")
            if np.sum(points[i, j] - generated_points[i, j]) != 0:
                input()
            #assert np.allclose(points[i, j], generated_points[i, j], atol=1e-2)
    """
    
    """
    # Verify with loaded points
    for i in range(0, 1080, 1):  # Sample some points for verification
        for j in range(0, 1920, 1):
            print(f"Loaded point ({i}, {j}): {points[i, j]}")
            print(f"Generated point ({i}, {j}): {generated_points[i, j]}")
            if np.sum(points[i, j] - generated_points[i, j]) != 0:
                input()
            #assert np.allclose(points[i, j], generated_points[i, j], atol=1e-2)
    """
    