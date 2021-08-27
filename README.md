# Air Cursor




# Mediapipe

[MediaPipe](https://google.github.io/mediapipe/) offers cross-platform, customizable ML solutions for live and streaming media.It provides various kinds of detection features such as Face Detection , Face Mesh , Iris , Hands , Pose etc.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Mediapipe.

```bash
pip install mediapipe
```

# PyAutoGUI



[PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) lets your Python scripts control the mouse and keyboard to automate interactions with other applications.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyAutoGUI.

```bash
pip install PyAutoGUI
```


# Opencv


[OpenCV](https://opencv.org/) is the huge open-source library for the computer vision, machine learning, and image processing and now it plays a major role in real-time operation

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Opencv.

```bash
pip install opencv-python
```

# NumPy


[NumPy](https://numpy.org/) is the fundamental package for scientific computing in Python. It is a Python library that provides a multidimensional array object, various derived objects (such as masked arrays and matrices), and an assortment of routines for fast operations on arrays, including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation and much more.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NumPy.

```bash
pip install numpy
```
# Pycaw


[Pycaw](https://github.com/AndreMiras/pycaw) is the library for audio controls

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pycaw.

```bash
pip install pycaw
```


## Code

```
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
```




# Controls

1) Close Hand:-Mode Selection<br/>

2) Cursor Mode:-Open Hand<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Move Cursor:- Thumb (up) + Index Finger (up) + other 3 fingers (down)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Left Click:-  Thumb (down) + Index Finger (up) + other 3 fingers (down)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Right click:- Thumb (up) + Index Finger (down) + Middle finger (down) + Ring finger (down) + little finger (up)
    
3) Volume:-Index finger + Thumb<br/>

4) Scroll:-Index finger +Middle finger + Ring finger<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) scroll up:-Index finger +Middle finger + Ring finger<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) scroll down:-Index finger +Middle finger + Ring finger + little finger<br/>
 

