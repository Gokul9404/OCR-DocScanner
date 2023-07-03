import cv2 
import numpy as np
from PIL import Image, ImageTk

import utils

import tkinter as tk
from tkinter import BitmapImage, Frame , Label, Canvas, Button, Menu, Tk, Text, Entry, ACTIVE, DISABLED,  TOP, LEFT, RIGHT,X, END, BOTTOM, BOTH, NW
from tkinter import filedialog as fld
from tkinter import messagebox as tmsg

#==============================================================================
# Tkinter Apk Properties
background_col = "#e1ecfa"

#===========================================
def connect_cam():
    """ Used to connect camera if not connected"""
    global CAM_MODE, Cam, Camera_connected
    try:
        Cam = cv2.VideoCapture(0)                           
        Camera_connected = True
    except Exception:
        tmsg.showerror('Camera not found!','The App is unable to Connect the Camera')
        
#===========================================
CAM_MODE = True
Camera_connected = False
Cam = None
# connect_cam()
#===========================================
# Image use Variables
Image_path = ''
Image_to_process = None
Img = None
Img_Final = None
Image_set = False
Image_from_Camera = False
#===========================================
# Image Properties
width_img, height_img = 480, 640
Threshold1, Threshold2 = 65, 210
#================================================================
def nothing():
    pass

def Change_to_image():
    global CAM_MODE
    print(CAM_MODE)
    if not CAM_MODE: 
        tmsg.showinfo("Image", f"Application is already in Image mode")
    if CAM_MODE == True:
        global  Image_path, Image_to_process, Image_from_Camera, Image_set, Cam_mode_frame 
        CAM_MODE = False
        Image_path = None
        Cam_mode_frame.destroy()
        Image_mode_widget()
        if not Image_from_Camera:
            Image_to_process = None
            Image_set = True
        else: Image_set = False

def Change_to_camera():
    global CAM_MODE
    print(CAM_MODE)
    if CAM_MODE: 
        tmsg.showinfo("Connected", f"Camera is already Connected")
    
    if CAM_MODE == False:
        global  Image_path, Img, Image_from_Camera, Image_set, Img_mode_frame 
        CAM_MODE = True
        Img = None
        Image_set = False
        Image_from_Camera = False
        Img_mode_frame.destroy()
        Camera_mode_widget()

#================================================================
def Camera_mode_widget():
    """Widgets which are Used to collect image from camera is created by this function"""
    global Cam_mode_frame, text_result
    
    # Changing the Name of the Window and Top-label
    Base_apk.title("Doc-Scanner Camera")
    top_name.config(text='Camera Mode')
    # Changing color of the Canavs
    img_canvas.delete('all')
    img_canvas.configure(bg="#b8c3d6")

    # Creating a Frame for the required widgets 
    Cam_mode_frame = Frame(Base_apk,bg=background_col,width=450,height=120,borderwidth=2)
    Cam_mode_frame.pack(side=TOP,fill=BOTH)
    # text_result = Text(Cam_mode_frame,font='lucida 12 italic',bg='#D3D3DB',fg="#242629")
    # text_result.pack(fill=BOTH,padx=10,pady=(2,5))

    # save image to Img global variable button
    Img_set_but = Button(Cam_mode_frame,text='Scan',font='century 14 bold',bg='#ffdf0f',width=10,command=set_cam_image)
    Img_set_but.pack(pady=1,padx=(15,0),side=LEFT)


def set_cam_image():
    global Image_to_process, Image_from_Camera, Img, Camera_connected
    if Camera_connected:
        Image_from_Camera = True
        Image_to_process = Img
        tmsg.showinfo("Image-Copied", f"Image is ready to be processed\nPlease select Image Mode for further processing")
    elif not Camera_connected:
        tmsg.showinfo("Cam not found", f"No Camera found to read image!!!")
#================================================================

def Image_mode_widget():
    """Widgets which are Used to Scan Image is created by this function"""
    global Img_mode_frame, text_result
    
    # Changing the Name of the Window and Top-label
    Base_apk.title("Doc-Scanner Image")
    top_name.config(text='Image-Scan Mode')

    # Creating a Frame for the required widgets 
    Img_mode_frame = Frame(Base_apk,bg=background_col,width=450,height=120,borderwidth=2)
    Img_mode_frame.pack(side=TOP,fill=BOTH)
    # Get image from folder
    # Save Image
    # Customize Thres value -> sub-window
    # set values -> destroy new window
    # Scan image get text

def Apk_loop():
    if CAM_MODE: Camera_mode_widget()
    else: Image_mode_widget()

    while True:
        try:
            Base_apk.update()
        except Exception:
            break

#================================================================
# Creating the tkinter apk
Base_apk = Tk()
Base_apk.geometry('520x740')
Base_apk.resizable(0,0)
Base_apk.config(bg=background_col)
#===========================================
# Create, Scan Menu
menu_bar = Menu(Base_apk)
menu_bar.add_command(label='Camera',command=Change_to_camera)
menu_bar.add_command(label='Image',command=Change_to_image)
Base_apk.config(menu=menu_bar)
#===========================================
# Top Frame containing App Name
top_frame = Frame(Base_apk,bg='#4e545c',height=15,borderwidth=2)
top_frame.pack(side=TOP,fill=X)
top_name = Label(top_frame,text='Doc-Scanner',bg="#e1ecfa",fg='#ff250d',font='georgia 14 bold')
top_name.pack(fill=X)
#===========================================
# QR canvas
canvas_frame = Frame(Base_apk,bg=background_col,height=height_img,width=width_img,borderwidth=2)
canvas_frame.pack(side=TOP,fill=BOTH)
img_canvas = Canvas(canvas_frame,width=width_img,height=height_img,bg='#6a6e75',borderwidth=2)
img_canvas.pack(side=TOP,padx=15,pady=(0,2))

#================================================================

if __name__ == "__main__":
    Apk_loop()