## Removed Guizero due to conflicts with Tkinter
#from guizero import App, Text, PushButton
#Importing required libraries
import Tkinter
from Tkinter import *
import tkFileDialog as filedialog
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string

#Getting path to directory of the folder "imgs"
cwd = os.path.dirname(os.getcwd()) + "/imgs/"

#Fixing a tesseract path error by hardcoding its path 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

## Path of working folder on Disk
src_path = "C:\Users\B2M\Desktop\muntest\imageidentifier\imageidentifier\imgs/"

#Main function that extracts text from image
def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "/removed_noise.png", img)

    # Disabled GAUSSIAN as it breaks certain images and conflicts with the functionality

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "/thres.png", img)

    # Recognize text with tesseract for python
    # result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))
    result = pytesseract.image_to_string(Image.open(src_path + "/thres.png"),config='outputbase digits')

    # Remove template file
    #os.remove(temp)
    os.remove(src_path + "/thres.png")
    os.remove(src_path + "/removed_noise.png")
    return result
# Looping Over each image and combining the text in one string for the output
def loop_imgs():
    # Initializing 'final_text variable'
    final_text = ''
    # Looping over each image in the 'imgs' folder
    for filename in os.listdir(cwd):
        # Currently only accepting png & jpg extensions
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Ignoring the temp files generated in case there is an error in deletion due to permission rights
            if filename != "thres.png" and filename != "removed_noise.png":
                # Calling the main function and extracting the text
                text = get_string(cwd + filename)
                #print('--- Start recognize text from image ---') # For Debugging
                #str = text.replace("S", "5")

                # Combining Text extracted from each image
                str = filename + " : \n" + text
                final_text += str + '\n \n '
                #print("------ Done -------")  # For Debugging
    return final_text

# Callback function for the gui's button
def button_action():
    res = loop_imgs()
    # Setting the gui's text
    var.set(res)
# Initializing trinkter's gui window
window = Tk()
# Initializing Label string value
var = StringVar()

# Setting the Title and Dimensions
window.title('Image Identifier')
window.geometry("700x600+10+10")

# Button for starting the process and calling the function
btn=Button(window, text="Analyze", fg='blue', command = button_action , font=("Helvetica", 12))
btn.place(x=300, y=100)

# Just a header title
label = Label( window, text="Start the Identifing Process",  fg='red', font=("Helvetica", 16) )
#label.place(x=500, y=500)

# Output text
lbl=Label(window, textvariable=var, fg='black', font=("Helvetica", 10))
lbl.place(x=300, y=200)

# Sending the label variable to interface
label.pack()

# Starting trinkter's interface mainloop
window.mainloop()