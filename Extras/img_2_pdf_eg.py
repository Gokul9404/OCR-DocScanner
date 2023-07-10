# from PIL import Image
# from fpdf import FPDF

# # Step 1: Install the required libraries
# # Step 2: Import the required modules

# # Step 3: Load the image using PIL
# image_path = 'Img_extarct_output.jpg'
# image = Image.open(image_path)

# # Step 4: Get the image dimensions
# image_width, image_height = image.size

# # Step 5: Create a PDF object using FPDF
# pdf = FPDF()

# # Step 6: Add a page to the PDF and set its dimensions
# pdf.add_page()
# pdf.set_auto_page_break(auto=True, margin=0)
# # pdf.set_page_unit("pt")
# # pdf.set_xy(0, 0)
# # pdf.set_margins(0, 0, 0)
# # pdf.set_auto_page_break(auto=False)
# # pdf.set_xy(0, 0)
# pdf.set_fill_color(255, 255, 255)
# pdf.rect(0, 0, image_width, image_height, style='F')

# # Step 7: Convert the image to PDF
# pdf_file_path = 'output.pdf'
# image.save(pdf_file_path, "PDF", resolution=100.0)

#===================================================================================================


# from fpdf import FPDF
# import PIL.Image as PImage
# import cv2

# width, height =  480, 640
# pdf = FPDF(unit="pt", format="A4")


# x, y, w, h = 10,10, 120, 480

# # PImage.open("Testimg_1.jpg")

# imagelist = [0,1]
# image = PImage.open("Img_extarct_output.jpg")

# # imagelist is the list with all image filenames
# for _ in imagelist:
#     pdf.add_page()
#     pdf.image(image,x,y,w,h)
# pdf.output("yourfile.pdf", "F")





#===================================================================================================
from PIL import Image
import img2pdf, cv2


with open( 'output.pdf', 'wb' ) as f:
    # specify paper size (A4)
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    f.write( img2pdf.convert( [ 'Img_extarct_output.jpg', 'Img_extarct_output.jpg'], layout_fun = layout_fun))
