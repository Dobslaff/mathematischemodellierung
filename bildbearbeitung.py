import os
from PIL import Image
import random
import shutil

def bildgroesse(folders):
    total_width = 0
    num_images = 0

    for folder_path in folders:
        # Loop through all images in the folder
        for filename in os.listdir(folder_path):
            # Open the image
            img = Image.open(os.path.join(folder_path, filename))
            # Add the width to the total
            total_width += img.width
            # Increment the number of images
            num_images += 1

    # Calculate the average width
    avg_width = total_width // num_images

    print(f'The average size of images in {folder_path} is {avg_width}x{avg_width} pixels.')

def einsortierunguntergroessenanpassung(source_folder, destination_folder, size):
    # Liste aller Bilder im Quellordner
    images = os.listdir(source_folder)

    # Fehler, falls schon Endbilder im Ordner sind
    if 'o_1.jpg' in os.listdir(destination_folder) or 't_1.jpg' in os.listdir(destination_folder) or 'e_1.jpg' in os.listdir(destination_folder):
        raise Exception('Es befinden sich schon gemischte Dateien im Ordner die beim Fortfahren doppelt vorlägen.\n'
                        'Fangen sie nochmal mit dem Prozedere an!')

    # Kopieren der Bilder in den Zielordner
    for i, image in enumerate(images):
        # Pfad zur aktuellen Bilddatei
        image_path = os.path.join(source_folder, image)
        # Öffnen des Bildes
        with Image.open(image_path) as img:
            # Ändern der Größe auf size x size
            img_resized = img.resize((size, size))
            # Neuer Name für die Bilddatei
            i += 1
            new_name = f'{i}_image.jpg'
            # Pfad zur neuen Bilddatei
            new_image_path = os.path.join(destination_folder, new_name)
            while os.path.exists(new_image_path):
                i += 1
                # Neuer Name für die Bilddatei
                new_name = f'{i}_image.jpg'
                # Pfad zur neuen Bilddatei
                new_image_path = os.path.join(destination_folder, new_name)
            # Speichern des Bildes im Zielordner
            img_resized.save(new_image_path)

    print(f'Alle Bilder wurden erfolgreich mit der Größe {size} kopiert.')

def manipulation(folder):

    # Liste aller Bilder im Ordner
    images = os.listdir(folder)

    # Fehler, falls schon Endbilder oder manipulierte Bilder im Ordner sind
    if 'o_1.jpg' in images or 't_1.jpg' in images or 'e_1.jpg' in images or 'image_1_manipulated.jpg' in images:
        raise Exception('Es befinden sich schon gemischte Dateien im Ordner die beim Fortfahren doppelt vorlägen.\n'
                        'Fangen sie nochmal mit dem Prozedere an!')

    # Speichern von manipulierten Bildern
    for i, image in enumerate(images):

        # manipulation nach HPI
        # manipulation von image i

        manipulated_image_path = os.path.join(folder, f'image_{i + 1}_manipulated.jpg')

        # Speichern des Bildes im Ordner
        image.save(manipulated_image_path)

    print("Manipulierte Bilder wurden gepeichert.")

def neusortierung(source_folder):
    # Positionierung
    if source_folder == 'ai_open_eye':
        position = 'o'
    elif source_folder == 'ai_tired_eye':
        position = 't'
    else:
        position = 'e'

    # Liste aller Bilder im Quellordner
    images = os.listdir(source_folder)

    # Fehler, falls schon Endbilder im Ordner sind
    if 'o_1.jpg' in images or 't_1.jpg' in images or 'e_1.jpg' in images:
        raise Exception('Es befinden sich schon gemischte Dateien im Ordner die beim Fortfahren doppelt vorlägen.\n'
                        'Fangen sie nochmal mit dem Prozedere an!')

    # Durchmischen der Bilder
    random.shuffle(images)

    # Kopieren der Bilder in den Zielordner
    for i, image in enumerate(images):
        # Pfad zur aktuellen Bilddatei
        image_path = os.path.join(source_folder, image)
        # Öffnen des Bildes
        with Image.open(image_path) as img:
            # Neuer Name für die Bilddatei
            i += 1
            new_name = f'{position}_{i}.jpg'
            # Pfad zur neuen Bilddatei
            new_image_path = os.path.join(source_folder, new_name)
            while os.path.exists(new_image_path):
                i += 1
                # Neuer Name für die Bilddatei
                new_name = f'{position}_{i}.jpg'
                # Pfad zur neuen Bilddatei
                new_image_path = os.path.join(source_folder, new_name)
            # Speichern des Bildes im Zielordner
            img.save(new_image_path)
            print(f"gespeichert in {new_image_path}")

    for file in os.listdir(source_folder):
        if file.endswith('manipulated.jpg') or file.endswith('image.jpg'):
            os.remove(os.path.join(source_folder, file))

    print(f'Alle Bilder wurden erfolgreich durchmischt.')


folders = ['tired_eye', 'open_eye', 'error_eye']
#bildgroesse(folders)

# Pfad zum Ordner mit den Bildern
source_folder = 'error_eye'
# Pfad zum Zielordner
destination_folder = 'ai_error_eye'
# neue größe
size = 98
#einsortierunguntergroessenanpassung(source_folder, destination_folder, size)

# Pfad zum Ordner mit den Bildern
source_folder = 'ai_error_eye'
#manipulation(source_folder)
#neusortierung(source_folder)