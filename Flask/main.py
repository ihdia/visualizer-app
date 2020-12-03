from skimage import io
import cv2 as cv

img = io.imread("http://127.0.0.1:5000/images")
img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
cv.imshow("test",img)
cv.waitKey(0)
cv.destroyAllWindows()