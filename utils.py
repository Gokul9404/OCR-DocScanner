import cv2 
import numpy as np

import pytesseract
from pytesseract import Output as PyTe_OUT

#============================================================

def biggestContour(contours):
    """Used to find the biggest contour based on contour-area, length and approx-Shape"""
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
    return biggest

#============================================================

def reorder(myPoints):
    """Reorder of contour end-points,
    such that we have points sorted on Top->Butoom and Left->Right
    """
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    #=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
 
    return myPointsNew
 
#============================================================

def noise_removal(image):
    """Apply Blur filters and Morphological operations to reduce 'Pepper & Salt' Noise

    Args:
        image : Image for which to reduce noise [in Gray-scale]

    Returns:
        Noise reduced Image
    """
    import numpy as np
    image = cv2.bitwise_not(image)
    
    image_blured = cv2.medianBlur(image, 3)
    
    kernel = np.ones((7,3), np.uint8)
    image_final_ = cv2.dilate(image_blured, kernel, iterations=1)

    image_final = cv2.bitwise_and(image,image_final_)
    image_final = cv2.bitwise_not(image_final)
    return (image_final)

#============================================================

def thick_font(image):
    """Used for dilating the texts in the image

    Args:
        image : Image in Gray_scale for dilation

    Returns:
        Dilated Image
    """
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

#============================================================

def get_text_from_img(img):
    """Used to extract texts from image using Pytesseract

    Args:
        img : Pre-Processed Image [in Gray-Channel]

    Returns:
        Text_list : List containing all the text extracted from images [may contain unwanted text/info]
    """
    img_config = r"--psm 11 --oem 3"
    try:
        ocr_result = pytesseract.image_to_data(img, config=img_config, output_type = PyTe_OUT.DICT)

        txt = ocr_result['text']

        return txt
    except Exception:
        return []

#============================================================