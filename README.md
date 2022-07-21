# Brain-Tumor-Detection
Identifying Brain tumor using Brain MRI Images, via OpenCV

A tumor is a mass of tissue formed by the rapid growth of abnormal cells inside the body. A tumor can stay in the body undetected for a long time, while slowly growing in size and turning into a cancer. Brain tumors are one of the deadliest forms of cancer, and thus, early detection of these tumors is necessary, and hence it composes a wide field of medical research.
MRI (Magnetic Resonance Imaging) is basically used in the biomedical to detect and visualize finer details in the internal structure of the body. It can easily detect differences in neighbouring tissues, and thus is a primary tool for tumor detection.
We have tried to correctly identify and segment brain tumors from MRI images of the brain. The images are acquired from **‘Brain MRI images for Brain Tumor Detection’ dataset available on Kaggle.** 

These images will then be converted to **greyscale**, and subsequently **sharpened and enhanced** (involving removing noise followed by high pass filtering). Then, the images will be subjected to **Watershed Segmentation**, and finally morphological operations will be carried out to extract the tumor from the rest of the image, so that it can be correctly identified.



Literature References:

1)Anam Mustaqeem,Ali Javed,Tehseen Fatima,"An Efficient Brain Tumor Detection Algorithm Using Watershed & Thresholding Based Segmentation", IJIGSP, vol.4, no.10, pp.34-39, 2012.

2)Gang Li , “Improved watershed segmentation with optimal scale based on ordered dither halftone and mutual information”, Page(s) 296 - 300, Computer Science and Information Technology (ICCSIT), 2010 3rd IEEE International Conference ,9-11 July 2010. 
