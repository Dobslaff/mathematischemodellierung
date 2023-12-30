import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os

# Initialisierung der Kameraerfassung
camera = cv2.VideoCapture(0) # 0 bezieht sich auf die Standardkamera

# Laden des Haar Cascade Classifiers für die Augenerkennung
cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# GUI Benutzeroberfläche wird erstellt
root = tk.Tk()
root.title("Augenerkennung")
root.geometry('2200x1200')

# Framerate-Variable
framerate = tk.DoubleVar()
framerate.set(10.0) # Standard-Framerate: 10 Frames pro Sekunde

# Vorherige Augengröße initialisieren
prev_eye_size = (0, 0)

# Funktion für den Start/Stop-Button
def toggle_camera():
    if not camera.isOpened():
        camera.open(0)
        btn_start["text"] = "Stop"
        update()
    else:
        camera.release()
        btn_start["text"] = "Start"

# Funktion zur Blinkenerkennung
def detect_blinking(eyes, empfindlichkeitswert):
    # Überprüfe, ob keine Augen erkannt wurden
    if len(eyes) == 0:
        return False

    (x, y, w, h) = eyes[0]
    # Extrahiert den Bereich des Auges aus dem Graustufenbild (ohne weißen Rand)
    eye_region = im_gray[y:y + h, x:x + w]
    '''
    # Berechne den Durchschnittswert der eye_region Matrizen
    eye_region_avg_value = np.mean(eye_region)
    
    # Wendet einen Schwellenwert (eye_region_avg_value) auf den Augenbereich an, um die Pupille zu isolieren
    _, eye_region_threshold = cv2.threshold(eye_region, eye_region_avg_value, 255, cv2.THRESH_BINARY)
    
    # Zählt die Anzahl der weißen bzw. hellen (70 bis 255) Pixel im Schwellenwertbereich
    eye_region_white_pixels = cv2.countNonZero(eye_region_threshold)
    
    if eye_region_white_pixels <= empfindlichkeitswert: # Wert anpassen, um die Empfindlichkeit zu steuern (Anzahl der Hellen Pixel)
    blink_label.config(text="Geschlossenes Auge!") # Zeige die Nachricht im Label an
    else:
    blink_label.config(text="") # Lösche die Nachricht im Label
    '''
    # neue Lösung
    eye_region_threshold = eye_region

    # Konvertiere die Schwellenwertmatrizen für die Anzeige
    threshold_image = Image.fromarray(eye_region_threshold)
    threshold_image = ImageTk.PhotoImage(image=threshold_image)
    threshold_panel.img = threshold_image
    threshold_panel.config(image=threshold_image)

    # Speichern des eye_region_threshold
    save_open_button_left.config(state=tk.NORMAL, command=lambda: save_image(eye_region_threshold, "open_eye", position="open", partie="l"))
    save_closed_button_left.config(state=tk.NORMAL, command=lambda: save_image(eye_region_threshold, "closed_eye", position="closed", partie="l"))

    save_open_button_right.config(state=tk.NORMAL, command=lambda: save_image(eye_region_threshold, "open_eye", position="open", partie="r"))
    save_closed_button_right.config(state=tk.NORMAL, command=lambda: save_image(eye_region_threshold, "closed_eye", position="closed", partie="r"))

def save_image(eye_region_threshold, folder, position, partie):
    if partie == "l":
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = os.path.join(folder, f"eye_{position}_{len(os.listdir(folder))+1}.png")
        cv2.imwrite(file_path, eye_region_threshold)
        print(f"Threshold saved to {file_path}")

    if partie == "r":
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = os.path.join(folder, f"eye_{position}_{len(os.listdir(folder))+1}.png")
        cv2.imwrite(file_path, cv2.flip(eye_region_threshold, 1))
        print(f"Threshold saved to {file_path}")




# Button zum Starten/Stoppen der Kamera
btn_start = tk.Button(master=root, text="Start", command=toggle_camera, bg="green", fg='black')
btn_start.place(x=0,y=0,width=50, height=40)
'''
# Label für die Blinkenerkennungsnachricht
blink_label = tk.Label(root, text="")
blink_label.place(x=750,y=200,width=100, height=20)
'''
# Schieberegler für die Framerate
framerate_label = tk.Label(root, text="Framerate:")
framerate_label.place(x=400,y=0,width=200,height=20)
framerate_scale = tk.Scale(master=root, variable=framerate, from_=1.0, to=30.0, orient=tk.HORIZONTAL, resolution=1.0, length=200)
framerate_scale.set(10.0) # Standard-Framerate
framerate_scale.place(x=400,y=20)

# Panel für die Anzeige des Video-Feeds erstellen
panel = tk.Label(root)
panel.place(x=0,y=200,width=640,height=480)

# Anzeige der größe der Augenmatrix
size_label = tk.Label(root, text="Größe:")
size_label.place(x=780, y=560, width=100, height=20)

# Panel für die Anzeige der Augenmatrix erstellen
threshold_panel = tk.Label(root)
threshold_panel.place(x=820,y=630, anchor=tk.CENTER)

# Button zum Speichern des offenen Auges links
save_open_button_left = tk.Button(root, text="Save Open Left Eye", state=tk.DISABLED)
save_open_button_left.place(x=650,y=600,width=125,height=20)

# Button zum Speichern des geschlossenen Auges links
save_closed_button_left = tk.Button(root, text="Save Closed Left Eye", state=tk.DISABLED)
save_closed_button_left.place(x=650,y=640, width=125,height=20)

# Button zum Speichern des offenen Auges rechts
save_open_button_right = tk.Button(root, text="Save Open Right Eye", state=tk.DISABLED)
save_open_button_right.place(x=865,y=600,width=125,height=20)

# Button zum Speichern des geschlossenen Auges rechts
save_closed_button_right = tk.Button(root, text="Save Closed Right Eye", state=tk.DISABLED)
save_closed_button_right.place(x=865,y=640, width=125,height=20)

# Funktion zum Aktualisieren des Video-Feeds
def update():
    ret, frame = camera.read()
    if ret:
        frame = cv2.flip(frame, 1)
        global im_gray, prev_eye_size # Füge die Graustufen-Version und vorherige Augengröße der globalen Variable hinzu
        im_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = cascade.detectMultiScale(im_gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            eye_region = im_gray[y:y + h, x:x + w]
            prev_eye_size = eye_region.shape
        if len(eyes) == 0:
            eye_region = np.zeros(prev_eye_size, dtype=np.uint8)

        empfindlichkeitswert = np.mean(im_gray)
        # Blinkenerkennung und Anzeige der Schwellenwertmatrix
        detect_blinking(eyes, empfindlichkeitswert)

        # Aktualisiere die Größe im Label
        size_label.config(text=f"Größe: {eye_region.shape[0]} x {eye_region.shape[1]}")

        # Anzeige des Video-Feeds
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(image=img)
        panel.img = img
        panel.config(image=img)

        # Aktualisierung basierend auf der ausgewählten Framerate
        panel.after(int(1000 / framerate.get()), update)

# Button zum Beenden der Anwendung
btn_quit = tk.Button(root, text="Quit", command=root.destroy,bg="red", fg="black")
btn_quit.place(x=950, y=0, width=50, height=40)

root.mainloop()
