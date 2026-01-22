import subprocess
import os
from pyngrok import ngrok

# Arrêter ngrok s'il y a déjà une instance
ngrok.kill()

# Créer un tunnel public pour le serveur Django
public_url = ngrok.connect(8000)
print("\n" + "="*60)
print("🌐 URL PUBLIQUE POUR VOTRE AMI:")
print(f"   {public_url}")
print("="*60)
print("\nPartagez cette URL avec votre ami!")
print("Il peut y accéder de n'importe où.\n")

# Garder le tunnel ouvert
ngrok_process = ngrok.get_ngrok_process()
ngrok_process.proc.wait()
