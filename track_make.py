"""
file that helps in converting png images into our tracks.
3 possible ways. 
    1) this file can be ran on it's own and then you will be able to select a single file from your pc and that file wil create a track.
    2) convert_png() allows you to do 1 but via code, notice that you still have to manualy select a single file
    3) convert_png_() you give the adres of a png.

track files will be left in the folder where the image is from (in all 3 cases)

png files are interpreted via lib (library defined underneath), the colors currently used are the standard colors from paint.
the idea is that you make a png using paint,
colors used so far are: black, whit, red, green, light grey
colors not in use will be maped onto -1.

if you want more colors to have a meaning, add the <(r, g, b):value> to the lib and it will appear in the track files, do note that you will have to rebuild the track files.
negative numbers are error values,
positive numbers (including 0) can be used as mapping for things in game
note that you will still need to implement it's behavior elsewhere. (this file is simply for conversion)
"""

from argparse import FileType
from msilib.schema import Error
from PIL import Image                                                                                
import tkinter as tk
from tkinter import filedialog

lib = {
            (0, 0, 0):0#outside of border
            ,(255, 255, 255):1#normal track
            ,(127,127,127):2#point line
            ,(237, 28, 36):3#finish
            ,(34, 177, 76):4#start
            }

def convert_png()->None:
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    convert_png_(file_path)

def convert_png_(file_path:str)->None:
    try:
        if file_path[-4:] != '.png':
            print("wrong file type selected")
            return
    except:
        print("wrong file type selected")
        return
    output_file_path = file_path[:-4]+".txt"
    img = Image.open(file_path)
    text = [[]]
    other = []

    def get_output(rgb:tuple[int, int, int])->int:
        r, g, b = rgb
        if -1 in lib.values():
            raise NameError("-1 should be used as error value, should not be in library.")
        if rgb in lib.keys():
            return lib[rgb]
        return -1# make sure -1 stays an error value, so don't use this as an value in the map

    for i in range(img.width):
        for j in range(img.height):
            if j == 0:
                text.append([])
            code = get_output(img.getpixel((i, j)))
            text[-1].append(code)
            if code not in other:
                other.append(code)




    with open(output_file_path, 'w') as f:
        for row in text:
            for letter in row:
                f.write(str(letter))
                f.write(',')
            f.write("\n")



if __name__ == "__main__":
    convert_png()