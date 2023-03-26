import logging
import base64
import hashlib

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from CipheredGUI import *



from cryptography.fernet import Fernet


class FernetGUI(CipheredGUI):

    def run_chat(self, sender, app_data) -> None:
    # Fonction de rappel utilisée par la fenêtre de connexion pour démarrer une session de chat
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connexion {name}@{host}:{port}")
        
        # Dérivation de la clé à partir du mot de passe en utilisant sha256().digest() et base64.b64encode()
        key_bytes = hashlib.sha256(password.encode()).digest()
        key = base64.b64encode(key_bytes)
        self._key = key
        
        self._callback = GenericCallback()
        
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message) -> bytes:
        # Créer un objet Fernet en utilisant la clé de chiffrement
        crypted = Fernet(self._key) 
        # Convertir le message en bytes
        bytes_message = bytes(message, 'utf-8') 
        # Chiffrer le message en utilisant l'objet Fernet
        encrypted_message = crypted.encrypt(bytes_message)
        # Enregistrer un message de log pour le message chiffré
        self._log.info(f"Voci le message chiffré : {bytes_message}")
        # Retourner le message chiffré
        return encrypted_message
    

    # Surcharge de la fonction decrypt
    def decrypt(self, message_data) -> str :
        encrypted_message = base64.b64decode(message_data['data']) 
        fernet_obj = Fernet(self._key)
        decrypted_message = fernet_obj.decrypt(encrypted_message).decode('utf8')
        self._log.info(f"Voici le Message déchiffré : {decrypted_message}") 
        return decrypted_message




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
