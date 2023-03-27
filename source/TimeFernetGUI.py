import logging
import base64


from FernetGUI import *

import time


from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

TTL = 30


class TimeFernetGUI(FernetGUI):
    def encrypt(self, message) -> bytes:
        # Crée une instance de la classe Fernet en utilisant la clé privée
        crypted = Fernet(self._key)  
        # Récupère le temps actuel et le convertit en entier
        temps = int(time.time())  
        # Convertit le message en entrée en une chaîne de bytes
        b_message = bytes(message, 'utf-8') 
         # Chiffre le message avec un TTL de 30 secondes à partir du temps actuel
        crypted_message = crypted.encrypt_at_time(b_message, temps + TTL)  
        # Retourne le message chiffré sous forme de bytes
        return crypted_message  # Retourne le message chiffré sous forme de bytes
    


    def decrypt(self, message) -> str:
        # On décode le message de base64
        msg = base64.b64decode(message['data'])
        # On crée un objet Fernet avec la clé
        decrypted = Fernet(self._key)
        # On récupère le temps actuel et on le convertit en entier
        temps = int(time.time())
        try:
            # On déchiffre le message en utilisant la méthode decrypt_at_time de Fernet avec un TTL de 30 secondes
            decrypted_message = decrypted.decrypt_at_time(msg, TTL, temps).decode('utf8')
            # On retourne le message déchiffré
            return decrypted_message
        except InvalidToken:
            # Si le message est expiré ou si la clé est invalide, on affiche un message d'erreur
            error_msg = "Erreur de déchiffrement : le message a expiré ou la clé est invalide"
            self._log.error(error_msg)
            return error_msg

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()

