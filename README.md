# m2-monRSA

# monRSA

`monRSA` est un outil de chiffrement RSA en ligne de commande. Il permet de générer des paires de clés, de chiffrer des messages avec une clé publique et de déchiffrer des messages avec une clé privée.

## Commandes

### `keygen`

Génère une paire de clés RSA et les sauvegarde dans des fichiers.

```bash
python monRSA.py keygen [-f filename] [-s size]
```

- `-f, --filename` : Le préfixe des noms de fichiers où les clés seront sauvegardées. Par défaut, c'est `monRSA`.
- `-s, --size` : La taille de la clé à générer. Par défaut, c'est 10.

### `encrypt`

Chiffre un message avec une clé publique.

```bash
python monRSA.py encrypt <keyfile> <message> [-i] [-o output]
```

- `<keyfile>` : Le fichier contenant la clé publique.
- `<message>` : Le message à chiffrer.
- `-i, --input` : Si cette option est utilisée, le message sera lu depuis un fichier.
- `-o, --output` : Le nom du fichier où sauvegarder le message chiffré.

### `decrypt`

Déchiffre un message avec une clé privée.

```bash
python monRSA.py decrypt <keyfile> <message> [-i] [-o output]
```

- `<keyfile>` : Le fichier contenant la clé privée.
- `<message>` : Le message chiffré à déchiffrer.
- `-i, --input` : Si cette option est utilisée, le message chiffré sera lu depuis un fichier.
- `-o, --output` : Le nom du fichier où sauvegarder le message déchiffré.

## Exemples

### Générer une paire de clés

```bash
python monRSA.py keygen
```

### Chiffrer un message

```bash
python monRSA.py encrypt monRSA.pub "Votre message ici"
```

### Déchiffrer un message

```bash
python monRSA.py decrypt monRSA.priv "Votre message chiffré ici"
```

### Chiffrer un message depuis un fichier

```bash
python monRSA.py encrypt monRSA.pub votre_message.txt -i
```

### Sauvegarder un message chiffré dans un fichier

```bash
python monRSA.py encrypt monRSA.pub "Votre message ici" -o message_chiffre.txt
```

## Notes
Développeur : Cedric Kadima
