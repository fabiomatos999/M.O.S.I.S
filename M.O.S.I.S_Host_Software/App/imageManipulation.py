import cv2
import numpy
import os
from PIL import Image


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
    ret, thr1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(outputPath, thr1)
    return thr1


def displayImage(UMat):
    while True:
        cv2.imshow('', UMat)
        if cv2.waitKey(10) & 0xFF == 27:
            break


if __name__ == "__main__":
    leftImage = "static/Media/8-SINGLE-2023-11-3T11-36-35.450975-NONE-0.0-100-0.016666666666666666-3200/8-8-2023-11-3T11-36-35.453342-95.5-100-8-0.5-L.jpg"
    rightImage = "static/Media/8-SINGLE-2023-11-3T11-36-35.450975-NONE-0.0-100-0.016666666666666666-3200/8-8-2023-11-3T11-36-35.453342-95.5-100-8-0.5-R.jpg"
    UMat = generateStereoscopicImage(leftImage, rightImage, "test.jpg")
    uwu = addMetadataBar("test.jpg", "data.jpg", "2023-11-3T11-36-35.450975",
                         10.312, 45000.312, 10.312, 100.312)
