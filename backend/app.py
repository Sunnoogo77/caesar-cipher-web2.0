# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from cipher.caesar import caesar_cipher_extended
# from cipher.caesar import brute_force_decrypt
# import random
# from cipher.caesar import SYMBOLS
# from cipher.file_cipher import encrypt_file, decrypt_file
# import os

# app = Flask(__name__)
# CORS(app) 

# UPLOAD_FOLDER = 'uploads'
# DOWNLOAD_FOLDER = 'downloads' 

# #Existance des fichiers
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# @app.route('/encrypt', methods=['POST'])
# def encrypt():
#     data = request.json
#     message = data.get('message', '')
#     key = data.get('key', None)

#     # Si aucune clé n'est fournie, générer une clé aléatoire
#     if key is None:
#         key = random.randint(0, len(SYMBOLS) - 1)

#     encrypted_message = caesar_cipher_extended(message, int(key), "encrypt")
#     return jsonify({"key": key, "encrypted": encrypted_message})

# @app.route('/decrypt', methods=['POST'])
# def decrypt():
#     data = request.json
#     message = data.get('message', '')
#     key = data.get('key', None)

#     if key is not None:
#         decrypted_message = caesar_cipher_extended(message, int(key), "decrypt")
#         return jsonify({"decrypted": decrypted_message})
#     else:
#         # Si pas de clé fournie, effectuer une attaque par force brute
#         brute_force_results = brute_force_decrypt(message)
#         return jsonify({"brute_force_results": brute_force_results})


# @app.route('/encrypt-file', methods=['POST'])
# def encryptF():
#     if 'file' not in request.files:
#         return jsonify({"error": "Aucun fichier envoyé"}), 400
    
#     file = request.files['file']
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)
    
#     encrypted_path = os.path.join(DOWNLOAD_FOLDER, file.filename + ".enc")
#     encrypt_file(file_path, encrypted_path)
    
#     return jsonify({"error": "Fichier chiffré avec succès", "file": encrypted_path}), 200

# @app.route('/decrypt-file', methods=['POST'])
# def decryptF():
#     if 'file' not in request.files:
#         return jsonify({"error": "Aucun fichier envoyé"}), 400
    
#     file = request.files["file"]
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)
    
#     decrypted_path = os.path.join(DOWNLOAD_FOLDER, file.filename.replace('.enc', ''))
#     decrypt_file(file_path, decrypted_path)
    
#     return jsonify({"message": "Fichier déchiffré avec succès", "file": decrypted_path})

# @app.route('/download/<filename>', methods=['GET'])
# def download(filename):
#     return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cipher.caesar import caesar_cipher_extended, brute_force_decrypt, SYMBOLS
from cipher.file_cipher import encrypt_file, decrypt_file
import os
import random

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads' 

# Vérifier l'existence des dossiers requis
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.json
        message = data.get('message', '')
        key = data.get('key', None)

        # Si aucune clé n'est fournie, en générer une aléatoirement
        if key is None:
            key = random.randint(0, len(SYMBOLS) - 1)

        encrypted_message = caesar_cipher_extended(message, int(key), "encrypt")
        return jsonify({
            "key": key,
            "encrypted": encrypted_message
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors du chiffrement: {str(e)}"}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.json
        message = data.get('message', '')
        key = data.get('key', None)

        if key is not None:
            decrypted_message = caesar_cipher_extended(message, int(key), "decrypt")
            return jsonify({
                "decrypted": decrypted_message
            }), 200
        else:
            # Si aucune clé n'est fournie, effectuer une attaque par force brute
            brute_force_results = brute_force_decrypt(message)
            return jsonify({
                "brute_force_results": brute_force_results
            }), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors du déchiffrement: {str(e)}"}), 500

@app.route('/encrypt-file', methods=['POST'])
def encryptF():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400
        
        file = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        encrypted_filename = file.filename + ".enc"
        encrypted_path = os.path.join(DOWNLOAD_FOLDER, encrypted_filename)
        encrypt_file(file_path, encrypted_path)

        return jsonify({
            "message": "Fichier chiffré avec succès",
            "file": encrypted_filename  # Ne renvoyer que le nom du fichier
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors du chiffrement de fichier: {str(e)}"}), 500

@app.route('/decrypt-file', methods=['POST'])
def decryptF():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400
        
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        decrypted_filename = file.filename.replace('.enc', '')
        decrypted_path = os.path.join(DOWNLOAD_FOLDER, decrypted_filename)
        decrypt_file(file_path, decrypted_path)

        return jsonify({
            "message": "Fichier déchiffré avec succès",
            "file": decrypted_filename  # Ne renvoyer que le nom du fichier
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors du déchiffrement de fichier: {str(e)}"}), 500

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Fichier non trouvé: {str(e)}"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
