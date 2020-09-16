#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import zipfile
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
# the rest is up to you!
zip = zipfile.ZipFile('readonly/images.zip','r')
zip.extractall()
img_lst = []
for name in zip.infolist():
    display(name.filename)
    i = Image.open(name.filename)
    img_lst.append(i)


# In[ ]:


final_contactlist = []
for i in range(len(img_lst)):
    pil_img=img_lst[i].copy()
    open_cv_version=pil_img.convert("L")
    open_cv_version.save("msi_r.png")
    cv_img=cv.imread('msi_r.png')
    faces = face_cascade.detectMultiScale(cv_img,1.7)
    img1 = []
    for x,y,w,h in faces:
        img1.append(img_lst[i].crop((x,y,x+w,y+h)))
    if len(img1) == 0:
        final_contactlist.append("But there were no faces in that file!")
    else:
        import PIL
        contact_sheet=PIL.Image.new(img1[0].mode, (100*5,100*2))
        MAX = (100,100)
        x= 0
        y = 0
        for s in img1:
            s.thumbnail(MAX)
            contact_sheet.paste(s, (x, y) )
            if x+s.width >= 500:
                x=0
                y=y+100
            else:
                x=x+s.width
        final_contactlist.append(contact_sheet)
for i in range(len(img_lst)):
    display(final_contactlist[i])


# In[ ]:


from kraken import pageseg
final_strlist = []
for i in range(len(img_lst)):
    im = img_lst[i].copy()
    imb_w = im.convert('L')
    bound = pageseg.segment(imb_w.convert('1'))['boxes']
    str = ""
    for b in bound:
        r = pytesseract.image_to_string(imb_w.crop(tuple(b)))
        str = str+r
    final_strlist.append(str)


# In[ ]:


wrd = input("Enter the word:")
for i in range(len(final_strlist)):
    if wrd in final_strlist[i]:
        k = 0
        for name in zip.infolist():
            if k == i:
                print("Results found in file "+ name.filename)
            k+=1
        display(final_contactlist[i])

