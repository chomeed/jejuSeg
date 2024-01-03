import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.features import geometry_mask
from shapely.geometry import Polygon

# Define the polygon coordinates
polygon_coords = [[(1553, 1787), (1570, 1773), (1590, 1791), (1539, 1791), (1549, 1785), (1553, 1787)], [(1596, 1791), (1596, 1791), (1619, 1770), (1629, 1760), (1657, 1788), (1654, 1791), (1596, 1791)]]
# Create a Shapely Polygon from the coordinates
polygon = Polygon(polygon_coords)

# Specify the TIFF image path
tif_image_path = "LC_JJ_AP25_33606070_014_2019_FGT_1024.tif"

# Open the TIFF image using rasterio
with rasterio.open(tif_image_path) as src:
    # Read the image as an array
    image = src.read(1)

    # Create a mask from the polygon
    mask = geometry_mask([polygon], out_shape=image.shape, transform=src.transform, invert=True)

    # Get the coordinates of the points inside the polygon
    ys, xs = np.where(mask)

    # Plot the original image
    plt.subplot(1, 2, 1)
    plt.imshow(src.read(1), cmap='gray')
    plt.title("Original Image")

    # Plot the points in blue
    plt.subplot(1, 2, 2)
    plt.imshow(image, cmap='gray')
    plt.scatter(xs, ys, c='blue', s=0.1)  # Adjust marker size (s) as needed
    plt.title("Image with Blue Polygon Points")

    plt.show()
