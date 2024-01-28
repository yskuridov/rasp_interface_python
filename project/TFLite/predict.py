import cv2
from lobe import ImageModel

def capture_image():
    model = ImageModel.load('./modele')
    capture = cv2.VideoCapture(0)

    _, img = capture.read()
    cv2.imshow('Frame', img)

    nomFichier = "./img.jpg"
    cv2.imwrite(nomFichier, img)
    print("Capture terminée.")
    resultat = model.predict_from_file(nomFichier)

    # L'étiquette de la prédiction, on l'inscrit sur l'image
    etiquette = resultat.prediction

    # Le niveau de confiance pour le meilleur choix
    confiance = resultat.labels[0][1]

    # Résultats
    print(f"Prédiction: {etiquette} | Confiance: {confiance * 100:.2f}")
    cv2.putText(img, f"{etiquette} | {confiance * 100:.2f}", (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    capture.release()
    cv2.destroyAllWindows()

# Call the capture_image function
capture_image()
