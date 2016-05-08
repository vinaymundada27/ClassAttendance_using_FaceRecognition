import os

from pyfaces import pyfaces
import sys, time
import cv2
import glob
import sys
import time
import Tkinter as tk
import os
import PIL.Image
import PIL.ImageTk
import cStringIO
import winsound


class Main:
    Freq = 2500  # Set Frequency To 2500 Hertz
    Dur = 1000  # Set Duration To 1000 ms == 1 second

    dict = {}  # a dictionary to store attendance status
    matches = {}  # a dictionary to store input file name and matched file name
    count = 0  # Stores the count of faces recognized
    rightFrame = None
    leftFrame = None

    def createGui(self):
        root = tk.Tk()
        root.wm_title("Attendance Updater")

        root.configure(bg="black")

        w = 800 # width for the Tk root
        h = 650 # height for the Tk root

        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.leftFrame = tk.Frame(root, width=400, bg="black", height=650, borderwidth=3, relief=tk.FLAT)
        self.rightFrame = tk.Frame(root, width=400, bg="black", height=650)

        mainLabel = tk.Label(self.leftFrame, text="Recognizing Faces..", fg="white", bg="black", font=('Comic Sans MS', 18, 'bold'))
        mainLabel.grid(row=0, columnspan=3)

        path = "E:\\POP project\\images\\input"

        attendanceLabel = tk.Label(self.rightFrame, text="Attendance Status", bg="black", fg="white", font=('Helvetica', 18, 'bold'))

        attendanceLabel.grid(row=0, columnspan=2, pady=(100, 20), padx=(100,100))
        n=1
        for i in range(1,11):
            label = tk.Label(self.rightFrame, bg="black", text="14IT"+str(i)+"      :", fg="white")
            label.grid(row=n, column=0, padx=(20,20), sticky=tk.E)
            n = n+1


        button1 = tk.Button(self.leftFrame, text="Display Result", bg="white", fg="black", font=('Helvetica', 14),command = self.displayResult)
        button2 = tk.Button(self.leftFrame, text="Show attendance", bg="white", fg="black", font=('Helvetica', 14), command =self.recognizeFaces)
        button3 = tk.Button(self.leftFrame, text="Take attendance", bg="white", fg="black", font=('Helvetica', 14), command=self.image_capture)

        button1.grid(row=2, column=1, pady=(20, 20))
        button2.grid(row=3, column=1, pady=(20, 20))
        button3.grid(row=4, column=1, pady=(20, 20))


        self.leftFrame.pack(side=tk.LEFT)
        self.rightFrame.pack()

        root.mainloop()

    # Function to find the recognized images
    def recognizeFaces(self):
        try:
            start = time.time()
            argsnum = len(sys.argv)

            # path to our database

            path = "E:\POP project\images\input"

            # all the set of images that have to be recognized (input)
            image_paths = [os.path.join(path, f) for f in os.listdir(path)]
            print "no of images: ",len(image_paths)

            n = 11
            # initialise the dictionary with all marked as absent
            for i in range(1,n):
                self.dict.update({i:"Absent"})

            for imgname in image_paths:
                # imgname="E:\POP project\images\probes\jack1.png"
                dirname = "E:\POP project\images\Basedatabase"
                eigenfaces = 22
                threshold = 0.6

                pyf = pyfaces.PyFaces(imgname, dirname, eigenfaces, threshold)
                match = pyf.getMatchFile()

                if(match is not None):
                    # print 'match = ',match
                    self.matches.update({imgname:match})
                    match = match.split("_")[0]
                    # print 'match = ',match
                    match = match.split("\\")[4]
                    # print 'match = ',match

                    # we maintain a dictionary to map roll no with attendance status
                    self.dict[int(match)] = "Present"
                    # self.count = self.count + 1

                    end = time.time()
                    print 'took :', (end - start), 'secs'

            print "Attendance status=",str(self.dict)
            print "Matches=",(self.matches)
            # print "Number of FACES RECOGNIZED = ", self.count

            n = 1
            for i in self.dict:
                # print self.dict[i]
                label = tk.Label(self.rightFrame, bg="black", text=self.dict[i], fg="white")
                label.grid(row=n, column=1, padx=(0,0), sticky=tk.W)
                n = n + 1


        except Exception, detail:
            print detail.args
            print "usage:python pyfacesdemo imgname dirname numofeigenfaces threshold "


    # code for capturing live image using Webcam
    def image_capture(self):
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Detect faces in the image
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            print "Found {0} faces!".format(len(faces))

            # Crop Padding
            left = 5
            right = 5
            top = 5
            bottom = 5

            # Draw rectangle
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x-20, y-20), (x+20+w, y+20+h), (0, 255, 0), 2)

            cv2.namedWindow("Taking Attendance")
            cv2.imshow("Taking Attendance",frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            for (x, y, w, h) in faces:
                # print "x=" + str(x) + " y=" + str(y) + " w=" + str(w) + " h=" + str(h)
                image = gray[y-top:y+h+bottom, x-left:x+w+right]
                size = 125,150
                image = cv2.resize(image, size)
                # print "cropped_{1}_{0}".format(str(y),str(x))
                cv2.imwrite("E:\POP project\images\input\cropped_{1}_{0}.png".format(str(y), str(x)), image)

            # time.sleep(2)
            winsound.Beep(self.Freq,self.Dur)

        video_capture.release()
        cv2.destroyAllWindows()


    ##
    def displayResult(self):

        labelMatch = tk.Label(self.leftFrame, text="Matched with -->", fg="white", bg="black", font=('Comic Sans MS', 16))
        labelMatch.grid(row=1, column=1, padx=(0,0))

        for i in self.matches:
            #print "key =",i
            #print "value= ",self.matches[i]
            img = PIL.ImageTk.PhotoImage(PIL.Image.open(i))
            panel = tk.Label(self.leftFrame, image=img, borderwidth=5)
            panel.grid(row=1, column=0, padx=(10, 0), pady=(0, 50))

            self.leftFrame.update()
            time.sleep(1)
            img = PIL.ImageTk.PhotoImage(PIL.Image.open(self.matches[i]))
            panel = tk.Label(self.leftFrame, image=img, borderwidth=5)
            panel.grid(row=1, column=2, padx=(10, 10), pady=(0, 50))

            self.leftFrame.update()
            time.sleep(1)

        self.leftFrame.update()
        time.sleep(5)

if __name__ == "__main__":
    print "start"
    obj = Main()
    obj.createGui()
    sys.exit(0)





