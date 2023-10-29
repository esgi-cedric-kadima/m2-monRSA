import random
from math import gcd
import base64
import sys
import argparse



''' Étape 1: Génération des clés '''
def is_prime(n, k=5):  # nombre de tests
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Écrire n comme d*2^r + 1
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Test de primalité de Miller-Rabin
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(digits=10):
    while True:
        number = random.randint(10 ** (digits - 1), 10 ** digits - 1)
        if is_prime(number):
            return number
        print(number)

def calculate_n_and_phi(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    return n, phi


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def find_e_d(phi):
    e = 3
    while True:
        if gcd(e, phi) == 1:
            d = multiplicative_inverse(e, phi)
            if d != e:
                return e, d
        e += 2

def keygen(filename='monRSA', size=10):
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()

    n, phi = calculate_n_and_phi(p, q)
    e, d = find_e_d(phi)

    # Sauvegarder les clés dans des fichiers
    with open(f"{filename}.priv", "w") as priv_file:
        priv_key = (f"---begin monRSA private key---\n{base64.b64encode(f'{n}:{d}'.encode()).decode()}\n---end monRSA "
                    f"key---")
        priv_file.write(priv_key)

    with open(f"{filename}.pub", "w") as pub_file:
        pub_key = (f"---begin monRSA public key---\n{base64.b64encode(f'{n}:{e}'.encode()).decode()}\n---end monRSA "
                   f"key---")
        pub_file.write(pub_key)

''' Étape 2: Chiffrement '''

def encrypt(message, public_key_filename="monRSA.pub"):
    # Charger la clé publique
    with open(public_key_filename, "r") as pub_file:
        pub_key = pub_file.readlines()[1].strip()
        n, e = map(int, base64.b64decode(pub_key).decode().split(':'))

    # Convertir le message en nombres en utilisant le code ASCII et le diviser en blocs
    message_numbers = [ord(char) for char in message]
    message_blocks = [''.join(map(lambda x: str(x).zfill(3), message_numbers[i:i+3])) for i in range(0, len(message_numbers), 3)]

    # Chiffrer chaque bloc
    encrypted_blocks = []
    for block in message_blocks:
        block_number = int(block)
        encrypted_block = pow(block_number, e, n)
        encrypted_blocks.append(str(encrypted_block).zfill(10))  # Assurez-vous que chaque bloc chiffré a une longueur fixe

    # Encoder le résultat en Base64
    encrypted_message = base64.b64encode(' '.join(encrypted_blocks).encode()).decode()
    return encrypted_message

''' Étape 3: Déchiffrement '''

def decrypt(encrypted_message, private_key_filename="monRSA.priv"):
    # Charger la clé privée
    with open(private_key_filename, "r") as priv_file:
        priv_key = priv_file.readlines()[1].strip()
        n, d = map(int, base64.b64decode(priv_key).decode().split(':'))

    # Décoder le message de Base64
    encrypted_blocks = map(int, base64.b64decode(encrypted_message).decode().split())

    # Déchiffrer chaque bloc
    decrypted_message = ""
    for block in encrypted_blocks:
        decrypted_block_number = pow(block, d, n)
        decrypted_block = str(decrypted_block_number).zfill(9)  # Assurez-vous que chaque bloc déchiffré a une longueur fixe
        for i in range(0, len(decrypted_block), 3):
            ascii_number = int(decrypted_block[i:i+3])
            if ascii_number != 0:  # Ignorez les zéros ajoutés pour le padding
                decrypted_message += chr(ascii_number)

    return decrypted_message

''' Étape 4: Interface en ligne de commande '''
def main():
    parser = argparse.ArgumentParser(description='monRSA: Un outil de chiffrement RSA en ligne de commande.')

    parser.add_argument('command', choices=['keygen', 'encrypt', 'decrypt'], help='La commande à exécuter.')
    parser.add_argument('keyfile', nargs='?', help='Le fichier contenant la clé RSA.')
    parser.add_argument('message', nargs='?', help='Le message à chiffrer ou déchiffrer.')

    parser.add_argument('-f', '--filename', default='monRSA', help='Le nom de base des fichiers de clé générés.')
    parser.add_argument('-s', '--size', type=int, default=10, help='La taille de la clé à générer.')
    parser.add_argument('-i', '--input', action='store_true', help='Lire le message depuis un fichier.')
    parser.add_argument('-o', '--output', help='Le nom du fichier où sauvegarder le message chiffré/déchiffré.')

    args = parser.parse_args()

    if args.command == 'keygen':
        # Générez les clés ici avec args.filename et args.size
        pass
    elif args.command in ['encrypt', 'decrypt']:
        if args.input:
            with open(args.message, 'r') as file:
                args.message = file.read()

        # Exécutez la commande de chiffrement ou de déchiffrement ici

        output_message = "Votre message chiffré/déchiffré ici"

        if args.output:
            with open(args.output, 'w') as file:
                file.write(output_message)
        else:
            print(output_message)

if __name__ == "__main__":
    command = sys.argv[1].lower()
    if command == "keygen":
        keygen()
    elif command == "encrypt":
        public_key_filename = sys.argv[2]
        message = sys.argv[3]
        print(encrypt(message, public_key_filename))
    elif command == "decrypt":
        private_key_filename = sys.argv[2]
        encrypted_message = sys.argv[3]
        print(decrypt(encrypted_message, private_key_filename))
    elif command == "help":
        print("Syntaxe :\nmonRSA <commande> [<clé>] [<texte>] [switchs]\nCommande :\nkeygen : Génère une paire de "
              "clé\ncrypt : Chiffre <texte> pour le clé publique <clé>\ndecrypt: Déchiffre <texte> pour le clé privée "
              "<clé>\nhelp : Affiche ce manuel")
