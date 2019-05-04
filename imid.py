#from guizero import App, Text, PushButton
import Tkinter
from Tkinter import *
import tkFileDialog as filedialog
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string

#cwd = os.getcwd() + "/imgs/"
cwd = os.path.dirname(os.getcwd()) + "/imgs/"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
## Path of working folder on Disk
src_path = "C:\Users\B2M\Desktop\muntest\imageidentifier\imageidentifier\imgs/"

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
def loop_imgs():
    final_text = ''
    for filename in os.listdir(cwd):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            if filename != "thres.png" and filename != "removed_noise.png":
                text = get_string(cwd + filename)
                print('--- Start recognize text from image ---')
                #str = text.replace("S", "5")
                str = filename + " : \n" + text
                final_text += str + '\n \n '
                print("------ Done -------")
    return final_text

def button_action():
    res = loop_imgs()
    var.set(res)

window = Tk()
var = StringVar()

window.title('Image Identifier')
window.geometry("700x600+10+10")

btn=Button(window, text="Analyze", fg='blue', command = button_action , font=("Helvetica", 12))
btn.place(x=300, y=100)

label = Label( window, text="Start the Identifing Process",  fg='red', font=("Helvetica", 16) )
#label.place(x=500, y=500)

lbl=Label(window, textvariable=var, fg='black', font=("Helvetica", 10))
lbl.place(x=300, y=200)



#label = Label( window, textvariable=var, relief=RAISED )
#label.place(x=50, y=400)
label.pack()
window.mainloop()