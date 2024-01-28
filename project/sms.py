import smtplib # si manquant -> pip install secure-smtplib

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
