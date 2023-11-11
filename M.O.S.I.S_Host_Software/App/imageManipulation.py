"""Image manipulation module for M.O.S.I.S host software.

Provides functionality to generate stereoscopic images,
add metadata bar to stereoscopic image,
GIF generation,
threshold image generation,
focus stack and video generation.
"""
import cv2
import numpy
import os
from PIL import Image
import re
import subprocess


@staticmethod
def findImagePairs(folder: str) -> [(str, str)]:
    files = os.listdir(os.path.join(folder))
    files = list(filter(lambda x: not re.match(r"^.*\.json$", x), files))
    leftImages = list(filter(lambda x: re.match(r".*-L\..*$", x), files))
    rightImages = list(filter(lambda x: re.match(r".*-R\..*$", x), files))
    leftImages.sort()
    rightImages.sort()
    return list(zip(leftImages, rightImages))


def generateStereoscopicImage(leftImage: str, rightImage: str, path: str):
    left_image = cv2.imread(leftImage)
    right_image = cv2.imread(rightImage)

    composite = numpy.concatenate((left_image, right_image), axis=1)
    cv2.imwrite(path, composite)
    return composite


def addMetadataBar(path: str, output: str, time: str, temperature: float,
                   pressure: float, ph: float, dissolvedOxygen: float):
    stereoImage = cv2.imread(path)
    black_bar = numpy.zeros(
        (int(0.30 * stereoImage.shape[0]), int(stereoImage.shape[1]), 3),
        dtype=numpy.int32)
    composite = numpy.concatenate((stereoImage, black_bar))

    def insertText(UMat, xOffSet: int, yOffSet: int, text: str):
        image = cv2.putText(UMat,
                            text="{}".format(text),
                            org=(int(xOffSet), int(yOffSet) - 100),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=7,
                            color=(255, 255, 255),
                            thickness=3,
                            lineType=cv2.LINE_AA)
        return image

    infoImage = insertText(composite, 0, 0.9 * composite.shape[0], time)
    infoImage = insertText(infoImage, 0.72 * composite.shape[1],
                           0.9 * composite.shape[0],
                           "T:{}C".format(round(temperature, 3)))
    infoImage = insertText(infoImage, 0.0 * composite.shape[1],
                           composite.shape[0],
                           "P:{}mbar".format(round(pressure, 3)))
    infoImage = insertText(infoImage, 0.4 * composite.shape[1],
                           composite.shape[0], "pH:{}".format(round(ph, 3)))
    infoImage = insertText(infoImage, 0.63 * composite.shape[1],
                           composite.shape[0],
                           "DO:{}mg/L".format(round(dissolvedOxygen, 3)))
    cv2.imwrite(output, infoImage)

    return infoImage


def generateGif(path: str, imagePairs: [(str, str)]):
    if os.path.exists(os.path.join(path, "stereo.gif")):
        return
    frames = []
    for pair in imagePairs:
        leftImage = os.path.join(path, pair[0])
        rightImage = os.path.join(path, pair[1])
        generateStereoscopicImage(leftImage, rightImage,
                                  os.path.join(path, "stereoFrame.jpg"))
        frame = Image.open(os.path.join(path, "stereoFrame.jpg"))
        frames.append(frame)
    frames[0].save(os.path.join(path, 'stereo.gif'),
                   save_all=True,
                   append_images=frames[1:],
                   optimize=False,
                   duration=3,
                   loop=0)
    os.remove(os.path.join(path, "stereoFrame.jpg"))


def generateWhiteScaleImage(imagePath: str, outputPath: str):
    image = cv2.imread(imagePath, 0)
    image = cv2.equalizeHist(image)
    ret, thr1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(outputPath, thr1)
    return thr1


def generateFocusStackImage(folderPath: str):
    def callFocusStackExecutable(images: [str], outputPath: str):
        threads = os.cpu_count()
        args = list()
        if os.name == 'nt':
            args.append(os.path.join(os.getcwd(), "focus-stack/focus-stack.exe"))
        else:
            args.append("focus-stack")
        args.append("--threads={}".format(str(threads)))
        for image in images:
            args.append(os.path.join(folderPath, image))
        args.append("--output={}".format(
            os.path.join(folderPath, outputPath)))
        subprocess.check_call(args)
    images = findImagePairs(folderPath)
    images.sort()
    callFocusStackExecutable(list(map(lambda x: x[0], images)), "focusStack-L.jpg")
    callFocusStackExecutable(list(map(lambda x: x[1], images)), "focusStack-R.jpg")
    generateStereoscopicImage(os.path.join(folderPath, "focusStack-L.jpg"),
                                  os.path.join(folderPath, "focusStack-R.jpg"),
                                  os.path.join(folderPath, "focusStack-S.jpg"))


def displayImage(UMat):
    while True:
        cv2.imshow('', UMat)
        if cv2.waitKey(10) & 0xFF == 27:
            break
