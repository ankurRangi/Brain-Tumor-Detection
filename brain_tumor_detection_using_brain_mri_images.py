# -*- coding: utf-8 -*-
"""Brain Tumor Detection using Brain MRI Images.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C1cV5mT7XQ9rup6M0nxzNzzquHWV2YZ_

**DIP Project : Identifying Brain tumor using Brain MRI images**
"""

#Importing the required libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from google.colab import drive
import tensorflow as tf

#Accessing google drive, where the MRI images are stored
#For now, there are 19 images in the drive, 9 without tumor and 10 with tumor
drive.mount('/content/drive')
image_path = "drive/My Drive/MRI_Dataset"
image_files = sorted([os.path.join(image_path, file)
                          for file in os.listdir(image_path)
                          if file.endswith('.jpg')])

"""So far, we have read our input MRI images into an array, so that they can be worked on easily. The entire MRI dataset available on Kaggle consisted of a total of 98 images without tumors, and 155 images with tumors. All the images were greyscale, however they were'nt of the same size.

As uploading the entire dataset and working on all of the images was neither necessary nor feasibile, we work with just 19 images, which include 10 images containing tumors, and 9 that don't. These images were chosen randomly from the dataset. 
"""

#Reading the images into an array img, and plotting an image to check it works
img = [cv2.imread(i, cv2.IMREAD_UNCHANGED) for i in image_files[:]]   
plt.imshow(img[-1])

"""**IMAGE DENOISING**

The first step in our image processing task is removing noise from the images. We have tried three noise removal techniques, and compared the final denoised images by their PSNR values to figure out which technique would work best. The denoising techniques were as follows:

**1) Gaussian Blur:**

Gaussian Blur involves passing the image through a Gaussian Low Pass Filter. It is a smoothing operator that blurs images and removes details and Noise. In a sense, the Gaussian LPF is similar to a Mean Filter, but the kernel is different, and represented in the form of a Bell-Shaped hump.

![Gaussian Filter.gif](data:image/gif;base64,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)

**2) Median Filtering:**

Median Filtering is a non-Linear image filtering technique, used to remove noise from an image. Its biggest advantage is that it removes noise while also preserving edges to some extent. It works by computing the median of the neighbors for each pixel in the image, and replacing it's value with the median.

**3) Non Local Means Denoising:**

Non Local Means Denoising is another strong noise-removal technique. It involves taking a pixel, then taking a small window around it. We then search for similar windows within the input image, and average out all such windows and then replace the pixel with the result we got. This method is computationally a bit expensive, but it gives good results.
"""

Denoised_Gaussian = []
Denoised_Median = []
Denoised_Nlmean = []  
for i in range(len(img)):
  temp1 = cv2.GaussianBlur(img[i], (5, 5), 0)   #Applying Gaussian Blur to remove noise
  Denoised_Gaussian.append(temp1)
  temp2 = cv2.medianBlur(img[i],5)    #Applying Median filter to remove noise
  Denoised_Median.append(temp2)
  temp3 = cv2.fastNlMeansDenoising(img[i],10,10,7,21)
  Denoised_Nlmean.append(temp3)     #Applying Non-Local Means Denoising.

plt.figure(1)
plt.imshow(Denoised_Gaussian[-1]), plt.title("Image after Gaussian Blur")
plt.figure(2)
plt.imshow(Denoised_Median[-1]), plt.title("Image after Median Filtering")
plt.figure(3)
plt.imshow(Denoised_Nlmean[-1]), plt.title("Image after Non-Local Means Denoising")

"""We then compute the PSNR values of the denoised images by each of the techniques with respect to the original imput images. This step is carried out to figure out which noise removal technique works the best, since visual analysis of the images isn't enough."""

psnr_gauss = cv2.PSNR(Denoised_Gaussian[-1],img[-1],255)
print("PSNR for Gaussian = ",psnr_gauss)
psnr_median = cv2.PSNR(Denoised_Median[-1],img[-1],255)
print("PSNR for Median = ",psnr_median)
psnr_nlmean = cv2.PSNR(Denoised_Nlmean[-1],img[-1],255)
print("PSNR for NL Means = ",psnr_nlmean)
if psnr_gauss == max(psnr_gauss,psnr_median,psnr_nlmean):
  print("Max PSNR value is obtained after Gaussian Blurring")
elif psnr_median == max(psnr_gauss,psnr_median,psnr_nlmean):
  print("Max PSNR value is obtained after Median Blurring")
else:
  print("Max PSNR value is obtained after Non-Local Means Denoising")

"""**IMAGE SHARPENING**

Removing noise from images almost always causes blurring, and could lead to the loss of important features and edges. Hence, image sharpening procedures are carried out to highlight such edges. We tried a couple of image sharpening techniques, namely Laplacian Mask, and Unsharp Masking.

**1) Laplacian Mask:**

As we know, the gradient operator is often used to detect sudden changes in pixel values in the image, that is, detecting sharp edges. The Laplacian Mask works in the same way, by calculating the Laplacian of an image to isolate edges, and then adding the resultant image to the original image.

![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAAClCAYAAACqepoAAAAW5UlEQVR4Ae1dbagd1RUd+qe/RTDGQCBBQlpjBAnPEo0x9KUBP4gKIVYUjRg0Ka2maItJqMmzSoRGJX6Ahv6pqBCNiBb808qDYi19IFop+IGBpNhCrUFKW0rRO2XNy5pZM2/m3vtu7j1zzpn9YN7MnTkze++19zqfc84k6Zm/r776OuXW632d9tuQDtftzxAwBAoE+nFGr5Fn2OMvwb//fPl5+vRjh9KZmZmhtj177klf+fVvM9LifiNkhqX96yACjP3Tfz2RcWjv/v1DcQjp3njr7QyxjIR4wIVJkiaL2O7e+0j6z3/9N3sIGd1BH5jJHUeAsX/q0z8vij/g2qNHj2Xo5STcfFGSnrt2c8bOP733Xjo3N9d3+/Tk3/KSsON+MPMNgfT06dPpMLxBml8+/lBG2CdeeLVMwqkkSVdt3J6XboarIWAITAaBP7z5an8Sfvb5l5lkFLOs71ZVaTpfTWe/DQFDYB4BVlvxa2gSGtEsfAyB8SGgfBqahMrc8aliTzIEuomAkbCbfjerPULASOiRM0yVbiJgJOym381qjxAwEnrkDFOlmwgYCbvpd7PaIwSMhB45w1TpJgJGwm763az2CIHoSAiDdPMIa1PFGQK9PAb6vd3lTJ0BgqIhoRpStbnftWramH530e5+NuOajy+aqM5BvjGjBoBAeGP91KlT2d5HwF2QXO0GPpxW5kJ2mzLUbhw3xUI1ZtrUGbJVn+BISOWxxzQQTD6+c+fOFJMiMbl4949+nE0whjPm/3pt4z1R+cSDQjCPDZhwgijPx7zHJPTZ2dn00MH9eSwgJvYdfDibfqdE9QUH9VtQJKTiAP2lo09l0z8uu/qmLOBQEpKUmCB58+13pe9+fMIXzCeuB+wHJpvWrchwwUoHXfhDprNv9x2ZzZhYjhgAFu/98ff5+QOHn0k5G4gx1DY2qkcwJKTSX//v3/kkSBAQk4mrf2++8qvMKcs3XlN7vZo+1N/AhCXfuhXfyGzmaghdICFWgNi9fUtmN4hWrYIjs37w3h0LrjOW2vS76hAECVVhEgzBplUuVDlY7VDwddkNfU6bDhiP7F6W2x87diyrcr35+vH0uqsuyYkYKwnpQ2TGTz/0QGbvxm235Zkt44Cx8MkHcylWiUC8KCZ8znh8sfinqPwgSEhAvzj5UXrLlqkM0G2778urGLwOKHjcRNbFw+XnHXAi2r3M/RGUj//8J9GTkN5AdZOlPtdmUf8zDrTmlEwVNSMlAZ/pcq/yvSehKqvEeu754znhCDhAZHpU06YvPi8nLIPVJdAuZXWBhPQtajpFhrM8rxHx+jzuRYccgxyk5TouGisu/URZqiv1o275Qk9cY4YNWg10PsjFnnK1ilmuihZgQx8ah/T377zpTG65JH3n/Q9dqOtcBvHpAgkJLjLYK1fOVzG1X4BYMB1/o0qqGTJjmrHC9C73KjsYEiqQyer1ec+nGqMgIijZZqjmgJouluPYSah+/t1vXs+rotos0TTwK0moHThJohlyOQN3GQuqq/ckJDAKfL/cj+nTtJe++Ozh3FnaQVOkCf+IzuwKCWEnlwhE5vrTA7/I28XEgl7l73KtyI8OGuoGXb0mYaFoL9X2oOZ+zO0IvO71HvSgsRqiaUI/pv1dIWG1WYKhCWJQ9SXjp4qN3sM01Xsn/VvlBkHCau4HEv7l7//IcGpyAC7OvvZyXhJqz9ikAXb5fNpfDTTtjnepz6RkMWhBwl03bsj9ig66pj/eA2y0aaK1IqZpesakzqtcr0moAaYg7rrvQF4FYZo6sGgcqi3JsjV5O7IubajnaH/sJKR/0L67dVMxHjoKCZGJs7dcyUAZLvYql3HqZe+oBthZk/CcVUZCF9E1ERlFBwpIeMOlKxddEmo7UpszSoaJqN7wUJUbNQm1M8dKwoZoCOK0kTBzE0sllz6jzGqdfqTqqAxruLRh0rIUo2IAu9wDOGkdXD5/1OqoloQaP1oiubRD5XpdElJRkFCHGwAiezoZhHUAascMPm5T97J33X0hnaP9sbcJGQvomOFL22jrj9Im7Des4cr3tAfyhiah3uRe0YVDFMP0juoQhTbGXenvQs5wJCyqcy50moQMxl91iIKdGXUyeU+1JqXEZZq6+yd5TuUOTUI6e5KK9Xu2tu9GGazXsaF+ckK7Rr90pSRE8GqtSKcwEQv6kIFeJa7OvmFa13vqBrnek5DA4n3B6y8/0ys2dU3e06nGKJDV3C+2cTPaSny6QkLYrRlyv/YdsSm9tuZJ34DG7dAk1JsYAC72BBK5mXY8NOVm1BPp8xe4PQF+EngRn9hJiNcQ+YcpbcyQ+9WKiA3eO+aKAz4M1MMOximOa0kII9ckSYqZ6Wx76U0Ew/Vec0DU6wky92occj/OPURDnGl8sGOcuNGe+ElYBC5sLXo7m6YyFS9wa9xojYgxMU5/DPss+g3p2YHIeZGNU5n0pmEFjSsdwdK6vQ648jrk8ViBL6YxFbnpuHRr+zn0SxdIqFijdMN0O/SQInjp9+oe+Oh6ROxVJ276TJfHKr+2JEQp4st8wiowAH/ZGfCruRoN04CMtUOGuDDo1GYEJrEBJsSF94S8L2yRHnPpI0C1FWmIC2J5+xUXZGRtasK0gUdhR0N11EcSFkr3Sg3zopSbhxLpODShpWUbQLuUqdVvlg4u5buUxVjQail8XR0H1poThjJITN7vUueqLNUhqJKQimOPNUa4sBFKO6w7icWOsPYkghDnWPWoAhDLb6wxMzc3l9nNZf9g+/y2JBvIBi5YBpAvLMdiO+0A0ZjpLl93VW4zFsDase3aFBPAUSvwiYDQnbGM46BIWFUeQYggO3LkyXwD+Ag6gk5nxbin/cAAGwjJjed4Pj4S9sTHvWytUWTCGgsgn5aOGvhtx4PqEhwJq0QkmCBdlXhqKNPZPi4Eqj7G72ocwOJqurZRUH2CJCEBrAObgKuRTG/7OBGAr5v83RQjbSOh+gZNQgJJJ2DvK+jU1faTRUBjYbKSzu7p0ZHw7OCwuw0B9wgYCd1jbhINgRICRsISHPbDEHCPgJHQPeYm0RAoIWAkLMFhPwwB9wgYCd1jbhINgRICRsISHPbDEHCPgJHQPeYm0RAoIWAkLMFhPwwB9wgYCd1jbhINgRICRsISHPbDEHCPgJHQPeYm0RAoIWAkLMFhPwwB9wgYCd1jbhINgRICRsISHPbDEHCPgJHQPeYm0RAoIWAkLMFhPwwB9whETUI1zj20YUrEagSxrUiAOPA5FlS3KJa3wIKvsQVRmHT2Q+sQYiEiEi4kH5YBDMEJfoTrvBbALAbcyn7veW1TFCQsA56mWI0Z35+YmZkprTXpU7D7pAvxw8rd+HoVVrD26eM/i8GKtvAeLgiMjwZxvVUNeqZrc6/6BF8dBeBYjZsrb2P1aS74qoa2Cbhvshm0wC7/3Nzq9cGSkPiiNMcCwFyN/PYf/iwnIW1m2rb3GpvBkhCAY3VpJR8I+O3LrzcS9okwdT6Xjwdu3/v+jiBJCHtOnTqVkS//HuWZTwHot+mNhH2CYjGXGEBZdeP14ymXvMenr751wTezbzCcu3azkbAPqAxG/boVSOjbtyj7mID1tPPLICDigMv9a6ZsJMxhGv8B2n/akYBPaU9ffF5GQisJm/EmAZGJodS4+fa70j177slw27jttoBKwoKEiANs/NPvUhoJiYqDPUjILzQZCesBZy0CpQi+couOGHw45+mHHgiQhPU24qyRsBmbsV9BUDFnNxIODy+D9N2PT2Q9ymxHhVUSlu3VWKB9qGJbSVjGaSK/mLs3kXAiQgN8KDMrDEdsOH/+89IwA9VS9iSGTEJtI0ZDwi9OfpSuCaCxzuBqIiFJGiBvxqYyMUI7+sF7d2TVUI6dxUPCAq4QSTj72stZk+DRo8cyQxL8r/tcto8BzQAzEhZBqEfqMw5HoBrKPyMhkXC/V98EO04I2AaR0D20fkkkPhiOQBsJX67FHwPASNiev+gDaBA1CdXQ9uBuRzJtB9F23bghvXvvI3mmRXIaCdvxDaTSPzg2Erbnh4lJLhzcS1989nCKFxg++/zLTB6u8bqRcGIuGPhg+gAJjYQD4Qo3ATsp3njr7cwIloDcGwnb862RsD3sc8l0AoiAl47x6tU4NhKuOhyRC5aqkJFQUXF7TP9DqpWEbrHPpbE0AlmuPfPCMTpPznbDzAG8xoXZEXgrhsMRuWA5aCKhJAnukKW/DdY7ch0DOcQhCuaE4y4J8SIzA/HA4WfSubm57OVmnK9uKIF3bLs2Iz5e4EZJzPTYE19H7hyLGNpuJBwLnIMfwiAJkYSDrRs9BccEhy1VlyxduqAE/u62H+SlKDOM0TVyd6eR0B3WmSQjYT3gaGMsS5J0enp64KYERPqtW7dm9+p7l0bCepzP5qxiam3Cs0HSy3vn11bBPDtO86nueQ01CL47etnVN6XvvP9hdg+vM5Pz0swGpawkbABmUqeZmzRVRyclN5bnoj1aN5UpZPuMhI69x5y6iYQkqWO1vBAH2+s2KEfcQEK81I22I2ZRcG0eXvfCkCGUgJ3U2Ug4BGCTSKIkRLWKb4foFJdJyA31mQxYLQl1jRleD8e+YqZ9lYS0xbcMWfUJuk3IIFHgkaujbWN/zQgwMLUkROYV6pKHtBTTtbBqAHuFUboXGTJT+bEPnoQwAJ0HGPfC2NamdSty4OEA5OqYMYCxLlax/IDeDy1iIiFswTIdiIWnHztUigPEwr6DD2fXEAvMZHzwQhQkJPAcgAbI3HgOe50/5wP4PumgAQzs+r1d45PeqgtKP6w7S58zBrjneeyNhIqcHRsCHUcg+JKQ/oMh/Tams30zAopfcyr/r6gddce+WQAd+RdFxwyNsb0hEAoCRsJQPGV6RouAkTBa15phoSBgJAzFU6ZntAgYCaN1rRkWCgJGwlA8ZXpGi4CRMFrXmmGhIGAkDMVTpme0CBgJo3WtGRYKAkbCUDxlekaLgJEwWteaYaEgYCQMxVOmZ7QIGAmjda0ZFgoCRsJQPGV6RouAkTBa15phoSBgJAzFU6ZntAiMREK9KVpkzDBDwBECyqfaSb1fnPwoXZMkKT4SwnU59CZHepoYQyBaBJRPs6+9nC1Q9ejRY5m9Cf7jc11TSZKu2rg9XzKOK3T5hgqMqW6+6uoKO3WwK5k+yKnGgc84qG61JaH/JOzln3xucr4a2ZQmrvODMYnL3sKaQb4edL14krsj1SlQEhZgwRh88ATrkGIrL9tXrMxc3BHfEUp+dSp+l3GIz+Y6i2A34wAx4XONSP0VLAkBMNabPHRwf3rnzp3pnj33ZHscY+FfX1dergueUc+pI/EM/MYnAbAILj+bPeqzQ7oPK4njg6eMAe658K+PGZL6LiAS9vKcDaBzuXMsdY6FXlkavnT0qayRi2Xdu7LwLzIkLIZM27HyNDKiLvwh07l/502Zz/FNRfgcsQA8+LEbnGcHoy+YBElCKg0C4nvsCDR8k72uxOOXas9duzlqIir5Npxf/t59F0gIAt666ZK8Z7Fa/cTq3Pz02917H8mr6IylNgmpOgRREhYK91ISDCTkh19wHQ6gE/RDJ76BP07Hozqu35nn9+djLgkZC5oZ49sj/OYIrjMegDWIev3lKzOiPvf88Rx+Pic/4fhA5QdBQpILgN6yZSoDdNd9B/JSkNeBI4/1S00xlgpwYrnzoZfXEGImIbmi/lVy0f8Mcv1Sk081I+oHe7wnYaFsuRSsAx7fI2R6EHb64vPyaquPjXMG1Dj2CDZW02MlIX2rNZ0kWV6qERVYFn0IStgnXng1z6j5vOIed0cq23sSMmcrA5809v7ROKRng12rru5gnrwk2Ep8ukBCIvrJB3Mp28DogGNVlFgwHX8jPTNkVF3Zj8BYYXqXe5XtPQmpLIDcfNGZzofV6/MOF16vAqiNcpAQOWCMfwy02EmoftaSTTvnNA18TWzw8snu7VuyWlE5Q25vHFl19Z6EJI4C3y/3Y3pUTV989nAOvHbQFGnCP2KgdYWEsJPDUyAUhh/Y1CAW9CoDvVor0j4CpuE9rvYqt5aEvrzAXShabg9q7lcFXkHUnlSfP52sOi/2mPZ3hYTVZgleeiYGVewYP8CGQxUg7oHDz+T3ME313kn/Vrm1L3D7RsJq7tfUM1oFjsYBeJ96xqp6ns1vOrNLJNx144a8hqMddFUcFRslodaKmKZ676R/q1zGaWkWhS8kZA5XzclAwqYqiILHYh4kTJatyduRmib0Y8Uo9t5R+ArtuxsunR/3g19HISFqUowfJYPLWFC5UZNQ25HJOauMhC6jbKyyig6UUUmo7UhtzigZxqrygIep3O6Q0ErCAWERxuVxkdBKwiH9rVUtrdOPVB2VYY0hxQeRTDHqSnWU74supjqqJaHGj5ZILh2ucr0uCako2oQ63KAgMgjrAKRxcJYOa9SlDfUc7e/fMVNU50K1k7GA3lEd8xulTYhhDeLG57rGReUyTr3smCkUXThEwakpBLMORB2i0MZ4XdpQzxGj/iQM1bpCb7WTU5SQuTJwi5TFEe8BcbUmpcRlmuIuN0cq12sSKhzayaKlWjMJy4P1Ojakzw39mPZ3hYQIXq0VDTtYr8T1YcJzUCRkkOkMikTad2qMEir2oKStxCd2e9XPmiH36+kkNqXX1iR2iGEbe7XH+5KQQFaDbFBuVnpVaeqaKIcnEDxN+OirWW0E2fhlFu1akIpzBPvViogN3jvetG5FNsDvw0A9sAmKhOpMzQFRryfIahCP8cLBdVfNz7qOtSqq2FQzqfhIWAQubC2qpMvzGTX0PXFhfGjcaObN60zvcq+6el8SAhiCpe8NajWE12EYjxV4zsB3CbIrWbS3iYTqbFc6uZCD5gmnM2kmSzxoN3Dh2jv6/jCvu9C1TobKD4KEmBHBP51L1pTbA3g2xPu94MtnxrBvImEMtqkNRfBKj/nSy/KJvZoWxyArp8BpKVhN5/p3YUeaBkLCoioCsLSUqwKrOZ/W/12D7Foego3tJHTda+ngWpdJy2MAq69RynFyL+Wj7cjM2JcZ9dSNNuB3MCSEsqo4FjniwkZcXxJrT+7bfUfWAEebka8m0fDY9lhjBss9wm5dRQAkTJIl6ZEjT6azs7PZ8n+xYcFYABExHnwhbF69PrcZC2AhPs5fe0XWZqxWU9uOBeoPPYIiIRRW5dFGBBkRbDMzM9ke4FdzxLYBH6/8omoOEoJk2EDG6qbXYiNhNRaw8jYyI40F1JL4Ukc1/Xh9svinaRwHR8LFmMvcbzH3WFpDwAUC0ZBQDSmAK1ZcK85146gej27b7ismqlfUJWE3wq/OyqLKWnfVzrWPgJGwfR+YBh1HwEjY8QAw89tHwEjYvg9Mg44jYCTseACY+e0jYCRs3wemQccRGEhCvO4zlSTpqo3b83X7bcyt41Fj5o8VASUhl+bkpxoSSDISjhVve5ghsAABI+ECSOyEIeAWASOhW7xNmiGwAAEj4QJI7IQh4BYBI6FbvE2aIbAAASPhAkjshCHgFoGRSKg3uVXXpBkC8SGgfFrUEAVurG6ARx8YH1xmkSEwGgLkCu7mMbmi4+5Dk3A0NewuQ8AQGIRAIwmvXDn/xsy7H59IsYzCMNsgYXbdEOgKAijphuEM0vCbKQvemAEJsWDQ1q1bB25Lli7NvpjKdUxY5HYFcLPTECACjH2sfoeFpqanpwfy5zsXzX95eAEJb9kylX8XfH71rnlSNh1jiT2SUOu7VM72hkAXECAJsT7ummzVu/68UT6VSAgSYfWqxWxY1crI14UwMxuHQQBLMS6GP0iLqin+she4hxFiaQwBQ2AyCPwfzD+elJmT7TwAAAAASUVORK5CYII=)

**2) Unsharp Mask:**

Unsharp Masking is an image sharpening technique, that uses a blurred, or "unsharp" of an image as a mask. This unsharp mask is combined with the original image, hence creating an image that is less blurry than the original. We used Gaussian Blur to creat the unsharp mask for the image, and used weighted addition to obtain our final sharpened image.
"""

Laplacian = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])

Sharp_Laplacian = []
Sharp_Unsharp = []
for i in range(len(Denoised_Gaussian)):
  image_sharp1 = cv2.filter2D(Denoised_Gaussian[i], -1, Laplacian)
  Sharp_Laplacian.append(image_sharp1)
  temp = cv2.GaussianBlur(Denoised_Gaussian[i], (5, 5), 0)
  image_sharp2 = cv2.addWeighted(Denoised_Gaussian[i], 1.5, temp , -0.5, 0, Denoised_Gaussian[i])
  Sharp_Unsharp.append(image_sharp2)

plt.figure(1)
plt.imshow(Sharp_Laplacian[-1]), plt.title("Image after Sharpening with Laplacian")
plt.figure(2)
plt.imshow(Sharp_Unsharp[-1]), plt.title("Image after Sharpening with Unsharp Mask")

"""
# **Segmentation** 

Segmentation is the technique of dividing or partitioning an image into parts, called segments. It is mostly useful for applications like image compression or object recognition. Here we are using Threshold and Adaptive Threshold Segmentation. Another method of segmentation is Watershed Segmentation.


**1. Threshold Method**

In case of threshold, we change the pixels of an image to make the image easier to analyze, where there is a convertion of an image from color or grayscale into a binary image (Black and white).

**2. Watershed Method**

Watersheds separate basins from each other. It basically sperates and assigns all the pixels into either a region or a watershed area. 


"""

thresh_seg = []
adThresh_seg = []


  #Threshold Method
for i in range(len(Sharp_Laplacian)):
  image = Sharp_Laplacian[i]
  #shifted = cv2.pyrMeanShiftFiltering(image, 5, 35)
  #gray = cv2.cvtColor(shifted.astype(np.uint8), cv2.COLOR_BGR2GRAY)
  if image.ndim == 2:
    grey = image
  elif image.ndim == 3:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
  addap_thresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,-2)
  thresh_seg.append(thresh)
  adThresh_seg.append(addap_thresh)
#workingg..

plt.figure(1)
plt.imshow(thresh_seg[-1], cmap= 'gray', vmin=0, vmax=250), plt.title("Image after Segmentaion using Threshold")
plt.figure(2)
plt.imshow(adThresh_seg[-1], cmap= 'gray', vmin=0, vmax=250), plt.title("Image after Segmentaion using ADThreshold")
#plt.figure(3)
#plt.imshow(waters_seg[-1], cmap= 'gray', vmin=0, vmax=250), plt.title("Image after Segmentaion using Watershed Method")

kernel = np.ones((3, 3), np.uint8)
Morph = []
for i in range(len(thresh_seg)):
  opening = cv2.morphologyEx(thresh_seg[i], cv2.MORPH_OPEN, kernel, iterations=7)
  sure_bg = cv2.dilate(opening, kernel, iterations=3)
  dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
  ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
  sure_fg = np.uint8(sure_fg)
  Morph.append(sure_bg)

plt.figure(1)
plt.subplot(121), plt.imshow(Morph[-1]), plt.title("Final segmented out tumor")
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img[-1]), plt.title("Original image")
plt.xticks([]), plt.yticks([])
plt.show()

plt.figure(2)
plt.subplot(121), plt.imshow(Morph[15]), plt.title("Final segmented out tumor")
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img[15]), plt.title("Original image")
plt.xticks([]), plt.yticks([])
plt.show()

plt.figure(3)
plt.subplot(121), plt.imshow(Morph[5]), plt.title("Final segmented out tumor")
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img[5]), plt.title("Original image")
plt.xticks([]), plt.yticks([])
plt.show()