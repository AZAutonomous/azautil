import sys
sys.path.append('..')
import jsonify

try:
    import cv2
    OPENCV_ENABLED = True

except ImportError:
    print("OpenCV not found.")
    OPENCV_ENABLED = False

data = {}
data["meta"] = "Some metadata"

if (OPENCV_ENABLED):
    image = cv2.imread("res/image.png")
    cv2.imshow("Original", image)
    data["image"] = image

jsonify.save(data, 'output.json')
loaded = jsonify.load('output.json')
meta_loaded = loaded["meta"]
print 'Loaded metadata:', meta_loaded

if (OPENCV_ENABLED):
    im_loaded = loaded["image"]
    cv2.imshow("Loaded", im_loaded)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



