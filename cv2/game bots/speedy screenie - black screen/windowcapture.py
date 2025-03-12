import win32gui, win32ui, win32con
import numpy as np


class WindowCapture:

    # PROPERTIES
    w = 0 # set this
    h = 0 # set this
    hwnd = None

    # CONSTRUCTOR
    def __init__(self, window_name):

        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}' .format(window_name))

        self.w = 1920
        self.h = 1080

    
    def get_screenshot(self, window_name):


        #get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0),(self.w, self.h) , dcObj, (0, 0), win32con.SRCCOPY)

        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


        img = img[...,:3]
        img = np.ascontiguousarray(img)


        return img


    def list_window_names(self):
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print (hex(hwnd), win32gui.GetWindowText( hwnd ))

        win32gui.EnumWindows(winEnumHandler, None)