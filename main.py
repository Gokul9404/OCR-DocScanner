import cv2 
import numpy as np
from PIL import Image, ImageTk

from tkinter import Frame , Label, Canvas, Button, Menu, Tk, TOP, LEFT, RIGHT, X, BOTH, NW
from tkinter import filedialog as fld
from tkinter import messagebox as tmsg

import utils
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
RUN = True

CAM_MODE = False
Camera_connected = False
Cam = None
#===========================================
# Image Processing-properties Variables
Image_path = ''             # Image directory path for access
Img = None                  # Image being captured or Selected
Image_to_process = None     # Image segement needed for Text-extraction
Img_Final = None            # Image used for final process of text-extraction
Image_to_show = 0           # Which image to show in the Apk (Img[0], Image_to_Process[1], Img_final[2])
Is_Image_setted = False     # Is there any image selected for processing
Is_extacted = False         # Is image segment is extracted
Is_processed = False        # Is image processed for Text-extracted
Image_from_Camera = False   # Is image captured from camera to process
Is_Text_extracted  = False  # Are text-extracted from the image
#===========================================
# Image Properties
width_img, height_img = 480, 640
Threshold1, Threshold2 = 65, 210
#==============================================================================
def Draw_image(img, mode=0):
    """Used for drawing cv2(Image) into the Canvas

    Args:
        img     : Image to be displayed
        mode    : Mode to image Resizing. 0 [resize with same aspect ratio], 1[resize to 640x480px]. Defaults to 0.
    """
    global Base_apk ,width_img, height_img, img_canvas, Image_to_process
    if img is None: return
    try: 
        height, width = img.shape[:2]
        fin_height, fin_width = height, width
        fin_x, fin_y = 0, 0

        if mode == 0:
            if width > height:
                final_aspect = width_img / width
                fin_width = width_img
                fin_height = int(final_aspect * height)
            elif height >= width:
                final_aspect = height_img / height
                fin_height = height_img 
                fin_width = int(final_aspect * width)
        else:
            fin_height, fin_width = height_img, width_img
        fin_x = int((width_img - fin_width) // 2)
        fin_y = int((height_img - fin_height)//2)    

        show_img_base = cv2.resize(img, (fin_width,fin_height))
        show_img_base = cv2.cvtColor(show_img_base, cv2.COLOR_BGR2RGB)
        show_img = ImageTk.PhotoImage(Image.fromarray(show_img_base))
        img_canvas.create_image(fin_x,fin_y,image=show_img,anchor=NW)
    except Exception: pass
    Update_base_apk()

#================================================================
def Update_base_apk():
    """
    Method used for Updating the Base-Apk 
    """
    global Base_apk, RUN
    try:
        Base_apk.update()
    except Exception:
        RUN =  False

#==============================================================================
def Change_to_image():
    """
    To change mode from Camera-Mode to Image-Mode, with repective variable changes
    """
    global CAM_MODE
    print(CAM_MODE)
    if not CAM_MODE: 
        tmsg.showinfo("Image", f"Application is already in Image mode")
    if CAM_MODE == True:
        global Img, Image_path, Image_to_process, Image_from_Camera, Is_Image_setted, Cam_mode_frame, Is_processed, Is_extacted, Is_Text_extracted, Img_Final
        CAM_MODE = False
        Is_extacted = False
        Is_processed = False
        Is_Text_extracted = False
        Image_path = None
        Img = None
        Img_Final = None
        Cam_mode_frame.destroy()
        Image_mode_widget()
        if Image_from_Camera:
            Img = Image_to_process.copy()
            Image_to_process = None
            Is_Image_setted = True
        else: Is_Image_setted = False

#================================================================
def Change_to_camera():
    """
    To change mode from Image-Mode to Camera-Mode,
    Set variables for image procesing.
    """
    global CAM_MODE
    print(CAM_MODE)
    if CAM_MODE: 
        tmsg.showinfo("Connected", f"Camera is already Connected")
    
    if CAM_MODE == False:
        global  Image_path, Img, Img_Final, Image_to_process, Image_from_Camera, Is_Image_setted, Img_mode_frame, Is_extacted, Is_processed, Is_Text_extracted
        CAM_MODE = True
        Img = None
        Img_Final = None
        Image_path = None
        Is_Image_setted = False
        Image_from_Camera = False
        Is_processed = False
        Is_extacted = False
        Is_Text_extracted = False
        Img_mode_frame.destroy()
        Camera_mode_widget()

#==============================================================================
def Camera_mode_widget():
    """Widgets which are Used to collect image from camera is created by this function"""
    global Cam_mode_frame, Img_set_but, img_canvas
    
    # Changing the Name of the Window and Top-label
    Base_apk.title("Doc-Scanner Camera")
    top_name.config(text='Camera Mode')

    # Creating a Frame for the required widgets 
    Cam_mode_frame = Frame(Base_apk,bg=background_col,width=450,height=120,borderwidth=2)
    Cam_mode_frame.pack(side=TOP,fill=BOTH)

    # save image to Img global variable button
    Img_set_but = Button(Cam_mode_frame,text='Scan',font='century 14 bold',bg='#ffdf0f',width=10,command=set_cam_image)
    Img_set_but.pack(pady=1,padx=(15,0),side=LEFT)

#================================================================
def set_cam_image():
    """
        Used to set the image captured from Camera for further processing
    """
    global Image_to_process, Image_from_Camera, Img, Camera_connected
    if Camera_connected:
        Image_from_Camera = True
        Image_to_process = Img
        tmsg.showinfo("Image-Copied", f"Image is ready to be processed\nPlease select Image Mode for further processing")
    elif not Camera_connected:
        tmsg.showinfo("Cam not found", f"No Camera found to read image!!!")

#==============================================================================
def Image_mode_widget():
    """Widgets which are Used to Scan Image is created by this function"""
    global Img_mode_frame, Img_get_but, Set_img_save_but, Get_extrated_but, Process_img_but, Get_text_but
    
    # Changing the Name of the Window and Top-label
    Base_apk.title("Doc-Scanner Image")
    top_name.config(text='Image-Scan Mode')

    # Creating a Frame for the required widgets 
    Img_mode_frame = Frame(Base_apk,bg=background_col,width=450,height=120,borderwidth=2)
    Img_mode_frame.pack(side=TOP,fill=BOTH)
   
    # Get image from folder
    Img_get_but = Button(Img_mode_frame,text='Get Image',font='century 8 bold',bg='#ffdf0f',width=10, command=Get_img_path)
    Img_get_but.pack(padx=(15,0),pady=2,side=TOP, anchor="w")

    # Save Image
    Set_img_save_but = Button(Img_mode_frame,text='Save Image',font='century 8 bold',bg='#ffdf0f',width=10)
    Set_img_save_but.pack(padx=(15,0),side=LEFT, anchor="s")

    # Scan image get text
    Get_text_but = Button(Img_mode_frame,text='Get Text',font='century 8 bold',bg='#ffdf0f',width=12, command = Get_text)
    Get_text_but.pack(padx=(15,0),side=RIGHT, anchor="w")
    
    Get_extrated_but = Button(Img_mode_frame,text='Get Extracted',font='century 8 bold',bg='#ffdf0f',width=12, command=Extract_image)
    Get_extrated_but.pack(padx=(15,0),side=LEFT, anchor="w")

    Process_img_but = Button(Img_mode_frame,text='Process Image',font='century 8 bold',bg='#ffdf0f',width=12, command=Process_image)
    Process_img_but.pack(padx=(15,0),side=TOP, anchor="w")

#================================================================
def Get_img_path():
    """
    Used to get Directory Path of the image user want to Process, and set the Image for processing
    """
    global Image_path, Img, Is_Image_setted
    try:
        Image_path = fld.askopenfilename(filetypes= ( ("JPG","*.jpg"),("JPEG","*.jpeg"),("PNG","*.png")))
        Img = cv2.imread(Image_path)
        Is_Image_setted = True
    except Exception: pass

#================================================================
def Extract_image():
    """
        Used to get the image-segment for which further processing can be done 
    """
    global Img, Image_to_process, Is_extacted, Image_to_show, Get_extrated_but
    if not Is_extacted: 
        if Img is None: return
        # Resizing the image
        width, height = 1080, 1530
        img = cv2.resize(Img, (width, height))
        #========================================================
        # Copies of image for process-result-comparison
        img_copy = img.copy()
        img_final = img.copy()
        #========================================================
        # Converted image into gray scale
        Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Gray_blur = cv2.GaussianBlur(Gray,(5,5), 1)
        #========================================================
        # Detecting edges using Canny-Edge-detection with user give threshold values
        Edges = cv2.Canny(Gray_blur,Threshold1,Threshold2)
        #========================================================
        # Creating kernl of size 5x5
        kernel = np.ones((5, 5))
        Final_edge = cv2.morphologyEx(Edges, cv2.MORPH_CLOSE, kernel)
        #========================================================
        # Finding Contours in the 'Edge'-image
        contour, _ = cv2.findContours(Final_edge , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        
        # FIND THE BIGGEST CONTOUR
        biggest = utils.biggestContour(contour)

        # if there is contour in the image
        if biggest.size != 0:
            # if there is contour in the image, then sort the contours based on Top-down approach
            biggest = utils.reorder(biggest)
            # DRAW THE BIGGEST CONTOUR
            cv2.drawContours(img_copy, biggest, -1, (0, 255, 0), 20)
            #=====================================================
            # Apply Projective-Transformation on the image for the given biggest contour
            pts1 = np.float32(biggest) 
            pts2 = np.float32([[0, 0],[width, 0], [0, height],[width, height]]) 
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img_final = cv2.warpPerspective(img, matrix, (width, height))
            img_final = cv2.resize(img_final,(width, height))
        #========================================================
        Img = img_copy.copy()
        Image_to_process = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)
        Is_extacted = True
        Get_extrated_but['text'] = "Show Extarcted"
    elif Is_extacted:
        Image_to_show = 1

#================================================================  
def Process_image():
    """
        Convert the Extracted-image_segment (apply different filters) to binary-channel image, that can be used for Text-extraction
    """
    global Is_extacted, Is_processed, Image_to_show, Image_to_process, Img_Final, Process_img_but

    if not Is_extacted: return
    
    if not Is_processed:
        im_bw = cv2.adaptiveThreshold(Image_to_process, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
        img_no_noise = utils.noise_removal(im_bw)
        dilated_image = utils.thick_font(img_no_noise)
        Img_Final = dilated_image.copy()
        Is_processed = True
        Process_img_but['text'] = "Show Processed"
    elif Is_processed:
        Image_to_show = 2

#================================================================
def Get_text():
    """
        Takes the binary-channel image [Img_final], and extract Text from it [and save them later].
    """
    global Img_Final, Is_Text_extracted, Get_text_but, Text_from_Img
    if Is_Text_extracted:
        with open("Text_from_image.txt", 'w') as f:
            txt = " ".join(Text_from_Img)
            f.write(txt)
        return

    Text_from_Img = utils.get_text_from_img(Img_Final)
    if Text_from_Img == []:
        tmsg.showinfo("Unable to process!!","The given image is being unable to get processed for TEXT extraction") 
        return
    else:
        Is_Text_extracted = True
        Get_text_but['text'] = "Save text"

#==============================================================================
def Apk_loop():
    """
        It consist the Mainloop, used to run the APK.
    """
    global Is_Image_setted, Image_to_show, Img, Image_to_process, Img_Final
    if CAM_MODE: Camera_mode_widget()
    else: Image_mode_widget()
    while RUN:
        try:
            if Is_Image_setted:
                if not CAM_MODE:
                    if Image_to_show == 0:
                        Draw_image(Img)
                    if Image_to_show == 1:
                        Draw_image(Image_to_process)
                    if Image_to_show == 2:
                        Draw_image(Img_Final)
            else:
                Update_base_apk()
        except Exception: pass        

#==============================================================================
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
top_frame = Frame(Base_apk,bg='#4e545c',height=13,borderwidth=2)
top_frame.pack(side=TOP,fill=X)
top_name = Label(top_frame,text='Doc-Scanner',bg="#e1ecfa",fg='#ff250d',font='georgia 12 bold')
top_name.pack(fill=X)
#===========================================
# QR canvas
canvas_frame = Frame(Base_apk,bg=background_col,height=height_img,width=width_img,borderwidth=2)
canvas_frame.pack(side=TOP,fill=BOTH)
img_canvas = Canvas(canvas_frame,width=width_img,height=height_img,bg='#6a6e75',borderwidth=2)
img_canvas.pack(side=TOP,padx=15)

#==============================================================================
if __name__ == "__main__":
    Apk_loop()