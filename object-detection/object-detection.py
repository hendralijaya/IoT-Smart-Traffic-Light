import cv2
import cvlib as cv
import numpy as np
import urllib.request

url = 'http://localhost:3000/download/car-motorcycle.png'

def count_objects(im):
    # Remove alpha channel if present
    if im.shape[2] == 4:
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
    bbox, label, conf = cv.detect_common_objects(im)
    counts = {'car': 0, 'motorcycle': 0}
    for l in label:
        if l == 'car':
            counts['car'] += 1
        elif l == 'motorcycle':
            counts['motorcycle'] += 1
    return counts

def run():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        counts = count_objects(im)
        # sent to esp32cam
        print(counts['car'], counts['motorcycle'])
        text = f"cars: {counts['car']}, motorcycles: {counts['motorcycle']}"
        im = cv2.putText(im, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('detection',im)
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()
 
 
if __name__ == '__main__':
    print("started")
    run()