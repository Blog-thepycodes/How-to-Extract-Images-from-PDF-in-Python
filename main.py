import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfReader
import os
import io
from PIL import Image
import re
 
 
def extract_images_from_pdf(pdf_path, output_dir):
   images = []
   with open(pdf_path, 'rb') as f:
       reader = PdfReader(f)
       for page_num, page in enumerate(reader.pages):
           if '/XObject' in page['/Resources']:
               xObject = page['/Resources'].get('/XObject')
               for obj in xObject:
                   obj_ref = xObject[obj]
                   if obj_ref.get('/Subtype') == '/Image':
                       size = (obj_ref['/Width'], obj_ref['/Height'])
                       data = obj_ref.get_data()
                       mode = ''
                       if obj_ref.get('/ColorSpace') == '/DeviceRGB':
                           mode = 'RGB'
                       else:
                           mode = 'P'
 
 
                       if obj_ref.get('/Filter'):
                           if obj_ref['/Filter'] == '/FlateDecode':
                               img = Image.frombytes(mode, size, data)
                               images.append(img)
                           elif obj_ref['/Filter'] == '/DCTDecode':
                               img = io.BytesIO(data)
                               img = Image.open(img)
                               images.append(img)
                               obj_name = re.sub(r'[^a-zA-Z0-9]', '_', obj)  # Replace invalid characters
                               file_path = os.path.join(output_dir, f"extracted_image_{page_num}_{obj_name}.jpg")
                               img.save(file_path)  # Save the image to the chosen directory
   return images
 
 
def browse_pdf():
   filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
   if filename:
       output_dir = filedialog.askdirectory(title="Select Directory to Save Images")
       if output_dir:
           extracted_images = extract_images_from_pdf(filename, output_dir)
           messagebox.showinfo("Extraction Complete", f"{len(extracted_images)} images extracted successfully.")
 
 
# Tkinter GUI
root = tk.Tk()
root.title("PDF Image Extractor - The Pycodes")
root.geometry("400x100")
 
 
browse_button = tk.Button(root, text="Browse PDF", command=browse_pdf,width=20)
browse_button.pack(pady=20)
 
 
root.mainloop()
