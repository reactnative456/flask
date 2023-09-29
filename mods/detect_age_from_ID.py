import cv2
from mods.card_validations import validations_dt
import easyocr

reader = easyocr.Reader(["en"])


def calculate_age(img):
    valid_obj = validations_dt()

    #Write image as temp file
    cv2.imwrite('temp.png',img)
    
    if not valid_obj.crop_card():
        return -1
    
    counter = 1

    while counter<=4:
        img = cv2.imread('temp.png')

        if not valid_obj.find_face():
            if counter>4:
                return 0
            else:
                counter+=1
                cv2.imwrite('temp.png',cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
                continue
            
        extracted_text = reader.readtext('temp.png', detail=0)
        print(extracted_text)
        
        txtt = ''
        for text in extracted_text:
            txtt+=text.replace(' ','')

        #Extracting all dates from the text
        dates = valid_obj.extract_dates(txtt)

        print(dates)
        if dates == []:
            if counter >4:
                return -1
            counter+=1
            cv2.imwrite('temp.png',cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
            continue
        
        expired = valid_obj.check_expiry(dates)
        #Check if card has expired
        
        if expired == 0:
            return valid_obj.find_age(dates)
        else:
            if counter>4:
                return expired
            else:
                counter+=1
                cv2.imwrite('temp.png',cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
                continue
    
    return -1
