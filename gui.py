import PySimpleGUI as sg
import io
from PIL import Image
import os.path
import subprocess
import sys
import detect
# import detect
# detect.detect('region_duplication/dataset/test.png',
#               'region_duplication/output/', 32)


def onDetect(input_image, output_directory, window):
    print("aaa")
    result_path = detect.detect(input_image, output_directory, 32)
    Image.open(result_path)
    image.thumbnail((400, 400))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE2-"].update(data=bio.getvalue())

input_row = [
    [
        sg.Text("Pilih gambar"),
        sg.In(size=(25,1), enable_events=True, key="-FILE-"),
        sg.FileBrowse(file_types=(("Image Files", ("*.png","*.jpg")),)),
    ],
    [
        sg.Text("Pilih output folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FILEOUTPUT-"),
        sg.FolderBrowse(),
    ],
]

image_left = [
    [sg.Text("Dataset:")],
    [sg.Image(key="-IMAGE-")]
]

image_right = [
    [sg.Text("Hasil Deteksi:")],
    [sg.Image(key="-IMAGE2-")]
]

layout = [
    input_row,
    [sg.Button("Deteksi")],
    [sg.Text("Logs:")],
    [sg.Output(key='-OUTPUT-',size=(100, 1))],
    [
        sg.Column(image_left),
        sg.VSeperator(),
        sg.Column(image_right)
    ]
]
window = sg.Window("Duplicated Region Detection", layout)
filename = ""
output_dir = ""
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FILE-" or "-FILEOUTPUT":
        filename = values["-FILE-"]
        output_dir = values["-FILEOUTPUT-"]
        try:
            if os.path.exists(filename) and os.path.exists(output_dir):
                print(filename)
                print(output_dir)
                image = Image.open(values["-FILE-"])
                image.thumbnail((400,400))
                bio = io.BytesIO()
                image.save(bio,format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
        except:
            sg.popup_error('file error')

    if event == "Deteksi":
        try:
            if os.path.exists(filename):
                print(filename)
                onDetect(filename, output_dir, window=window)
        except Exception as e:
            print(e)
            sg.popup_error('deteksi error')
        
window.close()
