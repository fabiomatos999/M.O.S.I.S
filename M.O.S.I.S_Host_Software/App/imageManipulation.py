import cv2
import numpy


def generateStereoscopicImage(filename: str, leftImage: str, rightImg: str):
    left_image = cv2.imread(leftImage)
    right_image = cv2.imread(rightImg)

    horizontal_intersection_pixel_count = int(0.995 * left_image.shape[1])

    right_image = cv2.resize(right_image,
                             (left_image.shape[1], left_image.shape[0]))

    left_image_roi = left_image.copy()
    left_image_roi = left_image_roi[:, left_image.shape[1] -
                                    horizontal_intersection_pixel_count:, :]

    right_image_roi = right_image.copy()
    right_image_roi = right_image_roi[:,
                                      :horizontal_intersection_pixel_count, :]

    intersection = cv2.addWeighted(left_image_roi, 0.5, right_image_roi, 0.5,
                                   0)

    left_image = left_image[:, :left_image.shape[1] -
                            horizontal_intersection_pixel_count, :]
    right_image = right_image[:, horizontal_intersection_pixel_count:, :]
    composite = numpy.concatenate((left_image, intersection, right_image),
                                  axis=1)
    return composite
