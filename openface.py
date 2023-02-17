import tkinter as tk
import cv2
import face_recognition
import os
import numpy as np
from PIL import Image, ImageTk 
import outils


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("800x420+350+100")
        self.main_window.config(bg='grey')
        self.login_button_main_window = outils.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=550, y=100)
        self.webcam_label = outils.get_img_label(self.main_window)
        self.webcam_label.place(x=5, y=5, width=500, height=400)

        self.add_webcam(self.webcam_label)

        self.db_dir_user = './db/user'
        self.db_dir_admin = './db/admin'
        if not os.path.exists(self.db_dir_user):
            os.mkdir(self.db_dir_user)
        if not os.path.exists(self.db_dir_admin):
            os.mkdir(self.db_dir_admin)

    def login(self):

        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.db_dir_admin) 
        print(self.myList)

        for cl in self.myList:
            curImg = cv2.imread(f'{self.db_dir_admin}/{cl}') 
            self.images.append(curImg) 
            self.classNames.append(os.path.splitext(cl)[0]) 
            # print(classNames)

        encodeListKnown = outils.findEncodings(self.images)
        print('Encoding Complete')

        imgS = cv2.resize(self.most_recent_capture_arr, (0,0), None, 0.25,0.25) 
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            name = self.classNames[matchIndex].upper()

        if matches[matchIndex]:
            
            self.main_admin_window = tk.Toplevel(self.main_window)
            self.main_admin_window.geometry("800x420+350+100")
            self.main_admin_window.config(bg="grey")

            self.register_button_new_user = outils.get_button(self.main_admin_window, 'New user', 'cyan', self.register_new_user, fg='black')
            self.register_button_new_user.place(x=550, y=210)

            self.register_button_new_admin = outils.get_button(self.main_admin_window, 'New Admin', 'cyan', self.register_new_admin, fg='black')
            self.register_button_new_admin.place(x=550, y=280)

            self.capture_label = outils.get_img_label(self.main_admin_window)
            self.capture_label.place(x=10, y=0, width=500, height=400)

            self.webcam_admin_label = outils.get_img_label(self.main_admin_window)
            self.webcam_admin_label.place(x=5, y=5, width=500, height=400)

            self.add_webcam(self.webcam_admin_label)

            self.button_openvid = outils.get_button(self.main_admin_window, 'OpenVid ', 'cyan', self.openvid, fg='black')
            self.button_openvid.place(x=550, y=140)

            """ self.button_show_attendance = outils.get_button(self.main_admin_window, 'show attendance', 'cyan', self.show_attendance, fg='black')
            self.button_show_attendance.place(x=550, y=70) """

            self.text_admin = outils.get_text_label(self.main_admin_window, name )
            self.text_admin.place(x=550, y=10)
            self.text_admin.config(bg="grey")
            
            
        if not matches[matchIndex]:
            outils.msg_box("Failed", "you are not and administrator")
        
        
        
    def openvid(self):
        self.images_users = []
        self.classNames_users = []
        self.myList = os.listdir(self.db_dir_user) 

        for cl in self.myList:
            curImg = cv2.imread(f'{self.db_dir_user}/{cl}') 
            self.images_users.append(curImg) 
            self.classNames_users.append(os.path.splitext(cl)[0])

        encodeListKnown_users = outils.findEncodings(self.images_users)

        while True:
            success, img = self.cap.read()
            imgS = cv2.resize(img, (0,0), None, 0.25,0.25) #resizing the image
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown_users, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown_users, encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.classNames_users[matchIndex].upper()
                    #print(name)

                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1), (x2,y2), (0,0,255), 1)
                    cv2.rectangle(img,(x1, y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
 
                    outils.markAttendance(name)
                else:
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1), (x2,y2), (0,0,255), 1)
                    cv2.rectangle(img,(x1, y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                    cv2.putText(img, 'unknown', (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            k = cv2.waitKey(1)
            if k%256 == ord('q'):
                break
                

            cv2.imshow('Webcam', img)
            cv2.waitKey(1)
    
    def show(self):
        pass

    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_admin_window)
        self.register_window.geometry("800x420+350+100")
        self.register_window.config(bg="grey")

        self.register_button = outils.get_button(self.register_window, 'REGISTER', 'green', self.register_user)
        self.register_button.place(x=550, y=170)

        self.try_button = outils.get_button(self.register_window, 'TRY AGAIN', 'red', self.try_again, fg='black')
        self.try_button.place(x=550, y=230)

        self.capture_label = outils.get_img_label(self.register_window)
        self.capture_label.place(x=5, y=5, width=500, height=400)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new = outils.get_entry_text(self.register_window)
        self.entry_text_register_new.place(x=550, y=110)

        self.text_register_new_user = outils.get_text_label(self.register_window, 'user name')
        self.text_register_new_user.place(x=550, y=70)
        self.text_register_new_user.config(bg="grey")

    def register_new_admin(self):
        self.register_window = tk.Toplevel(self.main_admin_window)
        self.register_window.geometry("800x420+350+100")
        self.register_window.config(bg="grey")

        self.register_button = outils.get_button(self.register_window, 'REGISTER', 'green', self.register_admin)
        self.register_button.place(x=550, y=170)

        self.try_button = outils.get_button(self.register_window, 'TRY AGAIN', 'red', self.try_again, fg='black')
        self.try_button.place(x=550, y=230)

        self.capture_label = outils.get_img_label(self.register_window)
        self.capture_label.place(x=5, y=5, width=500, height=400)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new = outils.get_entry_text(self.register_window)
        self.entry_text_register_new.place(x=550, y=110)

        self.text_register_new_admin = outils.get_text_label(self.register_window, 'admin name')
        self.text_register_new_admin.place(x=550, y=70)
        self.text_register_new_admin.config(bg="grey")


    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    

    def register_user(self):
        name = self.entry_text_register_new.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir_user, '{}.jpg'.format(name)), self.register_new_user_capture)
        outils.msg_box("success", "registered successfully")
        self.register_window.destroy()
    
    def register_admin(self):
        name = self.entry_text_register_new.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir_admin, '{}.jpg'.format(name)), self.register_new_user_capture)
        outils.msg_box("success", "registered successfully")
        self.register_window.destroy()

    def try_again(self):
        self.register_window.destroy()

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def start(self):
        self.main_window.mainloop()
        self.main_admin_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()