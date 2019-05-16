from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import cv2

from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches

i = 1
filename = './wagonr.mp4'
camera = cv2.VideoCapture(filename)

while (i != 0):
    reqd_path = []
    return_value, image = camera.read()
    cv2.imwrite('opencv' + str(i) + '.jpg', image)
    reqd_path.append('opencv' + str(i) + '.jpg')

    car_image = imread(reqd_path[0], as_grey=True)

    gray_car_image = car_image
    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image > threshold_value

    # this gets all the connected regions and groups them together
    label_image = measure.label(binary_car_image)

    # getting the maximum width, height and minimum width and height that a license plate can be
    plate_dimensions = (
    0.04 * label_image.shape[0], 0.5 * label_image.shape[0], 0.05 * label_image.shape[1], 0.6 * label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        if region.area < 50:
            # if the region is so small then it's likely not a license plate
            continue

        # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col
        # ensuring that the region identified satisfies the condition of a typical license plate
        if region_width / region_height < 7 and max_row < car_image.shape[0] and min_row > car_image.shape[
            0] / 2 and min_col > car_image.shape[1] / 4 and max_col < 3 * car_image.shape[
            1] / 4 and region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            plate_like_objects.append(binary_car_image[min_row:max_row, min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col, max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            i = 0
            fig, (ax1) = plt.subplots(1)
            ax1.imshow(gray_car_image, cmap="gray")
            ax1.add_patch(rectBorder)

            plt.show()

            del (camera)
        # let's draw a red rectangle over those regions
