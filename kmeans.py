import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Copied from the linked tutorial
def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

cap = cv.VideoCapture(0)
width = cap.get(3)
height = cap.get(4)

x = int(width/5)
y = int(height/5)

while(1):
	#Take each frame
	_,frame = cap.read()

	#Draw rectangle to indicate region of interest
	cv.putText(frame, "Region of Interest", (x,y-15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
	cropped_frame = frame[x:x+x, y:y+y].copy()
	cv.rectangle(frame,(x,y),(x+x,y+y),(255,0,0),2)

	#Use the linked Kmeans algorithm
	cropped_frame = cropped_frame.reshape((cropped_frame.shape[0] * cropped_frame.shape[1],3)) #represent as row*column,channel number
	clt = KMeans(n_clusters=3, n_init=5, max_iter=5) #cluster number
	clt.fit(cropped_frame)

	#Determine dominant color from histogram
	hist = find_histogram(clt)
	max_index = np.argmax(hist)
	dominant_color = clt.cluster_centers_[max_index]

	#Draw rectangle to indicate output
	cv.putText(frame,"Dominant Color", (3*x,y-15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
	cv.rectangle(frame,(3*x,y),(3*x+x,y+y),dominant_color.astype("uint8").tolist(), -1)

	cv.imshow('frame',frame)
	k = cv.waitKey(5) & 0xFF
	if k ==27:
		break

cv.destroyAllWindows()

