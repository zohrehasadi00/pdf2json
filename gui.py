import FreeSimpleGUI as sg
import json
import os
from PIL import Image
import io


def resize_image(image_path, target_width, target_height):
    img = Image.open(image_path)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)

    return bio.getvalue()

def papaias():
    sg.theme("Green")
    resized_image = resize_image(r"/statics/fu-logo.png", 500, 170)
    layout = [
        [sg.Text("MediLink - Freie Universität, Berlin", justification="center", size=(50, 1), font=("Helvetica", 20))],
        [sg.Image(data=resized_image, pad=((42,0), (20,20)))],
        [sg.InputText(key="file_path", enable_events=True, visible=True, size=(57,70), pad=((42,0), (30,30)) ), sg.FileBrowse("Browse", file_types=(("PDF Dateien", "*.pdf"),), key="browse", button_color="Black", size=(10, 2))],
        [sg.Button("Process", key="start", size=(20, 3), button_color="green", pad=((80, 50), (0,0))), sg.Button("Cancel", key="exit", size=(20, 3), button_color="red")]
    ]

    window = sg.Window("PDF Auswahl", layout, size=(600, 450))

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, "exit"):
            break

        if event == "start":
            pdf_path = values["file_path"]
            if pdf_path and os.path.exists(pdf_path):
                return pdf_path
            else:
                sg.popup("Bitte wählen Sie eine gültige PDF-Datei.", title="Fehler")

    window.close()
