import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from datetime import datetime


def get_button(window, text,color, command, fg='white'):
    button = tk.Button(window, text=text,
    activebackground='black',
    activeforeground='white',
    fg=fg,
    bg=color,
    command=command,
    height=1,width=15,font=('Helvetica bold', 15))

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=('sans-serif',18), justify='left')
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window, height=1, width=15, font=('Arial', 20))

    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title,description)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        return encodeList 

def markAttendance(name):
    with open('attendance.csv', 'r+') as file:
        myDataList = file.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            file.writelines(f'\n{name},{dtString}')