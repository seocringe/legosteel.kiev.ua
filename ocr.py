import cv2
import pytesseract
from pytesseract import Output
import pandas as pd

# Load the image from file
file_path = '/home/ars/pricemetal.png'
image = cv2.imread(file_path)

# Convert image to gray scale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use pytesseract to extract text
custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(gray_image, output_type=Output.DICT, config=custom_config, lang='rus')

# Store the text and bounding box coordinates
total_boxes = len(details['text'])
for sequence_number in range(total_boxes):
    if int(details['conf'][sequence_number]) >30:
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number], details['height'][sequence_number])
        threshold_img = cv2.rectangle(gray_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display one of the processed images to verify results before proceeding
cv2.imshow('captured text', threshold_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Organize data into a DataFrame
df = pd.DataFrame(details)
df1 = df[(df.conf != '-1') & (df.text != '') & (df.text != ' ')].groupby(['block_num', 'par_num', 'line_num', 'word_num'])['text'].apply(lambda x: ' '.join(x)).reset_index()
df1.drop(['word_num'], axis=1, inplace=True)
df1 = df1.groupby(['block_num', 'par_num', 'line_num'])['text'].apply(lambda x: ' '.join(x)).reset_index()
df1.drop(['block_num', 'par_num', 'line_num'], axis=1, inplace=True)
df1.head(50)  # Display the first 50 rows to inspect
