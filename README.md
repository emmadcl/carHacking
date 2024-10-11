# carHacking

# Projet de Simulation CAN pour l'ouverture et la fermeture des portes de voiture

Ce projet simule l'envoi et l'analyse de trames CAN (Controller Area Network) pour détecter la trame spécifique qui ouvre la porte d'une voiture. Il permet d'envoyer des trames en blocs à travers une interface CAN virtuelle (`vcan0`), de détecter la trame qui déclenche l'ouverture de la porte, et d'envoyer automatiquement une trame de fermeture une fois la porte ouverte.

## Fonctionnalités

- Envoi des trames CAN à partir d'un fichier `.log`.
- Diviser les trames en blocs et envoi par lots pour affiner la recherche de la trame d'ouverture de porte.
- Détection manuelle de l'ouverture de la porte par l'utilisateur.
- Envoi automatique de la trame de fermeture de la porte après son ouverture.
- Recherche récursive pour trouver précisément la trame d'ouverture.

## Prérequis

Avant d'exécuter le projet, assurez-vous d'avoir les éléments suivants installés :

1. Python 3 : installé sur votre machine.
 
  ```bash
  pip install python
  ```
   
2.    Bibliothèque `python-can` : pour la gestion des interfaces CAN :

  ```bash
   pip install python-can
   ```
4. Utilisation de ICSim

   Mettre en place ICSim à l'aide de : https://github.com/zombieCraig/ICSim

3. **Interface CAN virtuelle (`vcan0`) configurée** sur votre machine. Vous pouvez la configurer en exécutant les commandes suivantes :

   ```bash
   sudo modprobe vcan
   sudo ip link add dev vcan0 type vcan
   sudo ip link set up vcan0
   ```

## Utilisation

### 1. Lancer le projet

Le projet lit les trames CAN depuis un fichier `.log` et les envoie via l'interface `vcan0`. Pour lancer le projet, exécutez :

```bash
python3 voiture_python.py
```

### 2. Fonctionnalité de détection d'ouverture de la porte

Le projet envoie des trames par paquets, puis vous demande si la porte s'est ouverte après chaque paquet. Si vous répondez "oui", le projet enverra automatiquement la trame de fermeture et continuera à affiner la recherche pour trouver la trame exacte qui a ouvert la porte.

### 3. Variables à ajuster

Dans le fichier `voiture_python.py`, ajustez les valeurs suivantes en fonction de vos besoins :

- **Trame de fermeture de la porte** : Modifiez les variables `fermeture_id` et `fermeture_data` dans le code pour correspondre à l'ID CAN et aux données de la trame de fermeture de la porte de votre véhicule.

   ```python
   fermeture_id = 0x19B 
   fermeture_data = [0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00] 
   ```

- **Taille des paquets** : La variable `batch_size` contrôle le nombre de trames envoyées par paquet. Vous pouvez ajuster cette valeur pour affiner la recherche plus rapidement ou lentement.

   ```python
   batch_size = 1000
   ```

### 4. Exemple d'exécution

Lorsque vous lancez le projet, le terminal vous demandera si la porte s'est ouverte après chaque envoi de paquet. Voici un exemple d'exécution :

```bash
Envoi du paquet 1/5, trames 0 à 9
Trame envoyée: ID=0x13f, données=[0x00, 0x00, 0x05, 0x00, 0x1f]
La porte s'est-elle ouverte après cet envoi ? (o/n) : o
La porte s'est ouverte. Fermeture en cours...
Trame de fermeture envoyée: ID=0x123, données=[0x00, 0x00, 0x00, 0xff]
Recherche de la trame exacte en cours...
```

### 5. Capture des logs

Les trames envoyées et les erreurs potentielles seront affichées dans le terminal pour vous aider à suivre l'état du processus.

### 6. Acquisiton de la trame d'ouverture de porte

Après affinage, le terminal affichera un résultat de type :
Trame envoyée: ID=0x19B, données=[0x00, 0x00, 0x0E, 0x00, 0x00]



### Explication des sections :

1. **Fonctionnalités** : Présente les principales fonctionnalités du projet.
2. **Prérequis** : Indique les outils nécessaires pour que le projet fonctionne correctement.
3. **Installation** : Les étapes à suivre pour cloner et installer le projet.
4. **Utilisation** : Explique comment lancer et utiliser le projet, y compris les variables à ajuster (trame de fermeture, taille des paquets).
5. **Exemple d'exécution** : Donne une idée de ce à quoi ressemble l'exécution du script.
6. **Contribution** : Invitation à contribuer au projet.
7. **License** : Section sur la licence utilisée.
