import cv2
import argparse

# Function to display pixel value at mouse hover location
def show_pixel_value(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Pixel value at ({x}, {y}): {depth_image[y, x]}")

# Argument parser to get the file path from the command line
parser = argparse.ArgumentParser(description="Display pixel values of a depth image.")
parser.add_argument('--filename', type=str, required=True, help="Path to the depth image file")

# Parse the arguments
args = parser.parse_args()

# Read the depth image using the provided file path
depth_image = cv2.imread(args.filename, -1)  # Read image with original depth

# Check if the image was loaded properly
if depth_image is None:
    print(f"Error: Unable to load the image from {args.filename}")
else:
    # Display the image and set the mouse callback to show pixel values
    cv2.imshow('Depth Image', depth_image)
    cv2.setMouseCallback('Depth Image', show_pixel_value)

    # Wait indefinitely until a key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()
