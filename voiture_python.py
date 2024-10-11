import can
import time

def read_log_file(log_file_path):
    """Lit le fichier log et extrait les trames CAN."""
    frames = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.startswith("("):
                parts = line.split()
                if len(parts) < 3:
                    print(f"Ligne mal formée ou incomplète : {line}")
                    continue
                
                timestamp = parts[0][1:-1]
                can_id_data = parts[2]
                if '#' in can_id_data:
                    can_id, data_str = can_id_data.split('#')
                    try:
                        can_id = int(can_id, 16)
                        data = [int(data_str[i:i+2], 16) for i in range(0, len(data_str), 2)]
                        frames.append((can_id, data, float(timestamp)))
                    except ValueError as e:
                        print(f"Erreur de conversion des données dans la ligne : {line} - {e}")
                else:
                    print(f"Ligne mal formée (pas de '#') : {line}")
            else:
                print(f"Ligne non reconnue : {line}")
    return frames

def send_trame_fermeture(bus, fermeture_id, fermeture_data):
    """Envoie la trame pour fermer la porte."""
    msg = can.Message(arbitration_id=fermeture_id, data=fermeture_data, is_extended_id=False)
    try:
        bus.send(msg)
        print(f"Trame de fermeture envoyée: ID={hex(fermeture_id)}, données={fermeture_data}")
    except can.CanError:
        print(f"Erreur lors de l'envoi de la trame de fermeture: ID={hex(fermeture_id)}")

def send_can_frames_in_batches(bus, frames, batch_size, fermeture_id, fermeture_data):
    """Envoie les trames par paquets et envoie la trame de fermeture après détection de l'ouverture."""
    num_frames = len(frames)
    
    # Si le nombre de trames est 1 ou moins, on envoie directement
    if num_frames <= 1:
        for can_id, data, timestamp in frames:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            try:
                bus.send(msg)
                print(f"Trame envoyée: ID={hex(can_id)}, données={data}")
                time.sleep(0.1)
            except can.CanError:
                print(f"Erreur lors de l'envoi de la trame: ID={hex(can_id)}")
        return
    
    # Diviser les trames en paquets
    num_batches = (num_frames + batch_size - 1) // batch_size
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, num_frames)
        current_batch = frames[start_index:end_index]
        
        print(f"Envoi du paquet {i + 1}/{num_batches}, trames {start_index} à {end_index - 1}")
        # Envoyer chaque trame dans le paquet
        for can_id, data, timestamp in current_batch:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            try:
                bus.send(msg)
                print(f"Trame envoyée: ID={hex(can_id)}, données={data}")
                time.sleep(0)
            except can.CanError:
                print(f"Erreur lors de l'envoi de la trame: ID={hex(can_id)}")
        
        # Demander à l'utilisateur si la porte s'est ouverte
        porte_ouverte = input("La porte s'est-elle ouverte après cet envoi ? (o/n) : ").strip().lower()
        if porte_ouverte == 'o':
            # Si la porte s'est ouverte, envoyer la trame de fermeture
            print("La porte s'est ouverte. Fermeture en cours...")
            send_trame_fermeture(bus, fermeture_id, fermeture_data)
            print("Recherche de la trame exacte en cours...")
            send_can_frames_in_batches(bus, current_batch, max(1, batch_size // 2), fermeture_id, fermeture_data)  # Réduire la taille des paquets
            break  # Arrêt l'envoi des autres paquets

def send_can_frames(interface, frames, batch_size, fermeture_id, fermeture_data):
    """Fonction principale pour envoyer les trames en paquets et gérer la fermeture de la porte."""
    with can.interface.Bus(channel=interface, bustype='socketcan') as bus:
        send_can_frames_in_batches(bus, frames, batch_size, fermeture_id, fermeture_data)

if __name__ == "__main__":
    log_file_path = '/home/emma/Documents/ICSim-master/candump-2024-10-10_164358.log' 
    interface = 'vcan0'
    
    # Lire les trames à partir du fichier log
    frames = read_log_file(log_file_path)
    
    # Définir la taille du premier paquet
    batch_size = 1000
    
    # Trame de fermeture de la porte
    fermeture_id = 0x19B  # ID CAN de la trame de fermeture
    fermeture_data = [0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00] # Données de la trame de fermeture
    
    # Envoyer les trames via l'interface CAN et gérer la fermeture de la porte
    send_can_frames(interface, frames, batch_size, fermeture_id, fermeture_data)
