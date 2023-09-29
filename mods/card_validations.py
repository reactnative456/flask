import datetime
import re
from ultralytics import YOLO
import cv2

model = YOLO('models/best.pt')


class validations_dt:
    def extract_dates(self,txtt):
        # combine all patterns using the | operator
        combined_pattern = r'(\d{1,2})(\w{3})(\d{4})'

        # use findall method of regex to extract all matches
        matches = re.findall(combined_pattern, txtt)
        months = [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC",
        ]

        matches_copy = matches.copy()
        for match in matches_copy:
            if match[1] not in months:
                matches.remove(match)

        return matches

    def check_expiry(self,dates):
        #Extract expiry date from line
        try:
            exp_date = self.find_date_in_line(dates,'exp')
        except:
            return -1
        

        if exp_date == '': return -1

        #Check if card has expired or not
        now = datetime.date.today()
        exp_date= (exp_date-now).days

        #If expired return False
        if exp_date<=0:
            return -2
        else:
            return 0
        
    def find_age(self,dates):
        try:
            date_of_birth = self.find_date_in_line(dates,'dob')
        except:
            return -1
        
        #Subtract the current date from dob
        now = datetime.date.today()
        now -= date_of_birth
        now = now.days/365

        return now

    def find_date_in_line(self,datee, mode='exp'):
        days = []

        for d in datee:
            dayy,monthh,yearr = d
            strr = monthh+'/'+dayy+'/'+yearr
            temp = datetime.datetime.strptime(strr, "%b/%d/%Y").date()
            days.append(temp)
        

        final_date_value = ''

        if mode == 'exp':
            final_date_value = max(days)
        if mode == 'dob':
            final_date_value = min(days)

        return final_date_value

    def find_face(self):
        image = cv2.imread('temp.png')

        # Load the pre-trained Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for _ in faces:
            return True
        
        else:
            return False


    def crop_card(self):
        global model
        img = cv2.imread('temp.png')

        results = model.predict(img, conf=0.5)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                b = box.xyxy[0]

                x1,y1,x2,y2 = int(b[0].item()),int(b[1].item()),int(b[2].item()), int(b[3].item())

                img = img[y1:y2,x1:x2]

                cv2.imwrite('temp.png',img)
                return True
            
        
        return False