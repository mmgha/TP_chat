import logging
import base64

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import *

# Derivation de la clef
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Cipher block (chiffrage)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend

# Taille en octets de la clé
KEY_SIZE = 16 
# Nombre d'itérations pour la dérivation de la clé
ITERATIONS = 1000
# Taille en bits d'un bloc de chiffrement
BLOCK_SIZE = 128 
# Sel utilisé pour la dérivation de la clé
SALT = b"ceci_est_le_sel"



class CipheredGUI(BasicGUI):

    #Surcharge du constructeur pour y inclure le champ self._key qui contiendra la clef de chiffrement (default : None)
    def __init__(self) -> None:
        super().__init__() # surcharge du constructeur
        self._key = None 

#Surcharge de la fonction _create_connection_window() pour y inclure un champ password
    def _create_connection_window(self) -> None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):

            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(
                        default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            # Ajouter un champ password
            with dpg.group(horizontal=True):
                dpg.add_text("password")
                dpg.add_input_text(
                    default_value="", tag=f"connection_password", password=True)
            dpg.add_button(label="Connect", callback=self.run_chat)


#Surcharger la fonction run_chat() pour y inclure la récupération du password et faire la dérivation de clef (self._key)
    def run_chat(self, sender, app_data) -> None:
            # Fonction de rappel utilisée par la fenêtre de connexion pour démarrer une session de chat
            host = dpg.get_value("connection_host")
            port = int(dpg.get_value("connection_port"))
            name = dpg.get_value("connection_name")
            password = dpg.get_value("connection_password")
            self._log.info(f"Connexion {name}@{host}:{port}")
            
            # Fonction de dérivation de clé
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=KEY_SIZE,
                salt=SALT,
                iterations=ITERATIONS,
                backend=default_backend()
            )
    
            # Dérivation de la clé à partir du mot de passe
            key = kdf.derive(bytes(password, "utf8"))
            # Stockage de la clé dérivée
            self._key = key
    
            self._callback = GenericCallback()
    
            self._client = ChatClient(host, port)
            self._client.start(self._callback)
            self._client.register(name)
    
            dpg.hide_item("connection_windows")
            dpg.show_item("chat_windows")
            dpg.set_value("screen", "Connecting")

    def encrypt(self, message):
        # Générer un vecteur d'initialisation aléatoire
        iv  = os.urandom(16)
        # Initialiser le cipher avec l'algorithme AES et le mode CTR
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv))
        # Initialiser l'objet encryptor avec le cipher
        encryptor = cipher.encryptor()

        # Ajouter un padding pour obtenir la taille souhaitée
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(bytes(message, "utf8")) + padder.finalize()

        # Chiffrer le message en utilisant l'encryptor
        _encryptor_ = encryptor.update(padded_text) + encryptor.finalize()

        # Retourner le vecteur d'initialisation et le cipher final
        return (iv, _encryptor_)
        
 
    def decrypt(self, message):
        
        
        iv = base64.b64decode(message[0]['data'])
        message = base64.b64decode(message[1]['data'])
        
        decryptor = Cipher(
            algorithms.AES(self._key),
            modes.CTR(iv),
            backend=default_backend()
        ).decryptor()

        # Déchiffrer le message
        unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
        data = decryptor.update(message) + decryptor.finalize()
        #Retourner le message déchiffré
        return (unpadder.update(data) + unpadder.finalize()).decode()

    def recv(self) -> None:
        # Fonction appelée pour recevoir les messages entrants et les afficher
        if self._callback is not None:
            for user, encrypted_message in self._callback.get():
                decrypted_message = self.decrypt(encrypted_message) # Déchiffrement du message reçu
                self.update_text_screen(f"{user} : {decrypted_message}")
            self._callback.clear()

    def send(self, message: str) -> None:
        # Fonction appelée pour envoyer un message
        encrypted_message = self.encrypt(message) # Chiffrement du message à envoyer
        self._client.send_message(encrypted_message)
        self._client.send_message(encrypted_message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()






        
