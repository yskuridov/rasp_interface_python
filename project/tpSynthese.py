from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from gpiozero import DistanceSensor
import Freenove_DHT11 as DHT
from time import sleep
import cv2
from lobe import ImageModel
from LEDMatrix import display_message
import smtplib
import os

app = Flask(__name__)


distanceSensor = DistanceSensor(6, 5)
dht = DHT.DHT(4)
verification = dht.readDHT11()


entered_password = ""
correct_password = "1234"
dateTime = None
category = None
distance = None
image = None
sms = None
temperature = None
humidity = None
lastRefreshTime = None

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/main', methods=['POST', 'GET'])
def main():
    global entered_password
    if entered_password == "":
        entered_password = request.form.get('password')
    
    
    if entered_password == correct_password:
        return render_template('tableau.html', dateTime=dateTime, image=image, category=category, distance=distance, sms=sms, temperature=temperature, humidity=humidity)
    else:
        return render_template('index.html', error=True)
    
    


#def readPassword(): keypad



def sendSms():
    global sms
    sms = datetime.now()
    gmail_utilisateur = 'yskuridov@gmail.com'
    gmail_app_motPasse = 'txee wipa vxdy ptri'  # obtenu de Google
    de = gmail_utilisateur
    vers = gmail_utilisateur
    sujet = "URGENT"
    try:
        corps = "Bonjour!\n\nUne image suspecte a été prise par votre Raspberry PI!"
        leCourriel = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (de, vers, sujet, corps)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_utilisateur, gmail_app_motPasse)
        server.sendmail(de, vers, leCourriel.encode('utf-8')) # latin pour Outlook
        server.close()
        print('Courriel envoyé!')
    except Exception as exception:
        print("Erreur: %s!\n\n" % exception)


    

def predict_new_image():
    global category
    global image
    
    current_time = datetime.now()
    name = current_time.strftime("%Y%m%d%H%M%S")+ ".jpg"
    
    model = ImageModel.load('./TFLite/modele')
    capture = cv2.VideoCapture(0)

    _, img = capture.read()
    cv2.imshow('Frame', img)
    
    
    nomFichier = f"./static/{name}"
    cv2.imwrite(nomFichier, img)
    
    print("Capture terminée.")
    resultat = model.predict_from_file(nomFichier)
    
    etiquette = resultat.prediction
    
    if etiquette == "disarmed":
        category = "désarmé"
    elif etiquette == "armed":
        sendSms()
        category = "armé"

    confiance = resultat.labels[0][1]

    print(f"Prédiction: {etiquette} | Confiance: {confiance * 100:.2f}")
    cv2.putText(img, f"{etiquette} | {confiance * 100:.2f}", (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    
    image = f"../static/{name}"
    print(image)
    
    capture.release()
    cv2.destroyAllWindows()

def setTemperatureAndHumidity():
    global temperature
    global humidity
    global verification
    if (verification is dht.DHTLIB_OK):
        temperature = dht.temperature
        humidity = round(dht.humidity, 2)


def displayMatrice(message):
    display_message(message)
    


def toggleRefresh():
    global dateTime, distance
    predict_new_image()
    dateTime = datetime.now()
    distance = round(distanceSensor.distance * 10, 2)
    if(distance < 10):
        sendSms()
    setTemperatureAndHumidity()
    
    

@app.route('/refresh', methods=['POST'])
def refresh_page():
    toggleRefresh()
    return redirect(url_for('main'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        
        displayMatrice(message)
        return redirect(url_for('main'))



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
