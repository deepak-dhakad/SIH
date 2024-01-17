import cv2
import easyocr
import pandas as pd
from datetime import datetime
from IPython.display import Image

harcascade = "C:\SIH\Car-Number-Plates-Detection-main\model\haarcascade_russian_plate_number.xml"
reader = easyocr.Reader(['en'])

cap = cv2.VideoCapture(0)

cap.set(3, 640)  
cap.set(4, 480) 

min_area = 500
count = 0

df = pd.DataFrame(columns=["Timestamp", "License Plate"])

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y + h, x: x + w]
            cv2.imshow("ROI", img_roi)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("C:\SIH\Car-Number-Plates-Detection-main\plates\scaned_img_" + str(count) + ".jpg", img_roi)
        image_path = "C:\SIH\Car-Number-Plates-Detection-main\plates\scaned_img_" + str(count) + ".jpg"
        output = reader.readtext(image_path)
        print(output)
        number = output[-1][1]
        print(number)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_data = {"Timestamp": timestamp, "License Plate": number}
        df = df.append(new_data, ignore_index=True)

        with pd.ExcelWriter("C:\SIH\Car-Number-Plates-Detection-main\license_plate_data.xlsx", engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)

        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results", img)
        cv2.waitKey(500)
        count += 1

    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()