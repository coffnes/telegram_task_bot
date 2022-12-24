from save_to_database import save_photo
import cv2


def check(user_id, img_path):
    net = cv2.dnn.readNetFromCaffe("model/weights-prototxt.txt", "model/res_ssd_300Dim.caffeModel")
    image = cv2.imread(img_path)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    temp = 0
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            temp += 1
    if temp > 0:
        save_photo(user_id, img_path)
        return True
    return False