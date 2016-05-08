import glob
import os
import cv2
from Tkinter import *

class MyDialog:

    name = ""
    def __init__(self, parent):

        top = self.top = Toplevel(parent)
        Label(top, text="IMAGE NAME").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()
        self.name = self.e.get();
        self.top.destroy()

    def getName(self):
        return self.name

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)
        # construct the argument parser and parse the arguments


# code to change size of cropped image
def resize():
    root = Tk()
    # Button(root, text="Hello!").pack()
    # root.update()
    d = MyDialog(root)
    root.wait_window(d.top)
    str = d.getName()
    # str = raw_input("enter name of last cropped image")
    # os.rename("cropped.png", str)
    croppedImage = cv2.imread("cropped.png")
    gray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    size = 125, 150
    im_resized = cv2.resize(gray, size)
    # if not os.path.exists("db"):
    #     os.mkdir("db")
    cv2.imwrite(os.path.join("E:\POP project\images\Basedatabase", str+".png"), im_resized)
    os.remove("cropped.png")


files = glob.glob("*.jpg")    #check whether images are .jpg or .png
for file in files:
    refPt = []
    cropping = False
    image = cv2.imread(file)
    # size1 = 1000,1000
    # img = cv2.resize(image,size1)
    # image=cv2.imwrite(file,img)
    clone = image.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            img = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imwrite("cropped.png", roi)
        cv2.imshow("ROI", roi)

        cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()
    resize()








