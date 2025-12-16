# Guide Rapide - Utilisation après les correctifs

## ⚡ Démarrage rapide

### Si vous avez une carte Mediatek (mt7921, mt76, etc.)

```bash
# 1. Diagnostic rapide
sudo ./wifiphisher_recovery.sh check

# 2. Lancer wifiphisher avec votre carte en monitoring
sudo wifiphisher -eI wlan1 --noextensions

# Si problème, restaurer:
sudo ./wifiphisher_recovery.sh restore
```

### Si vous avez WireGuard actif

```bash
# Option 1: Laisser WireGuard tourner (recommandé avec les nouveaux correctifs)
sudo wifiphisher -eI wlan1 --noextensions
# Les interfaces wg* seront automatiquement ignorées

# Option 2: Arrêter temporairement WireGuard
sudo wg-quick down wg0
sudo wifiphisher -eI wlan1 --noextensions
# Après utilisation:
sudo wg-quick up wg0
```

## 🔧 En cas de problème

### Le PC a crashé / terminal bloqué

**Depuis un autre terminal ou après redémarrage:**

```bash
sudo ./wifiphisher_recovery.sh restore
```

Cela va:
- Tuer tous les processus wifiphisher/hostapd/dnsmasq
- Supprimer les interfaces virtuelles
- Restaurer les interfaces WiFi en mode managed
- Nettoyer iptables
- Redémarrer NetworkManager

### L'interface reste en mode monitor

```bash
# Méthode automatique
sudo ./wifiphisher_recovery.sh restore

# Méthode manuelle
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up
```

### Erreur "Interface managed by NetworkManager"

```bash
# Vérifier l'état
nmcli dev

# Rendre l'interface unmanaged temporairement
sudo nmcli dev set wlan1 managed no

# Ou permanent (créer le fichier):
sudo nano /etc/NetworkManager/conf.d/unmanaged.conf
# Ajouter:
# [keyfile]
# unmanaged-devices=interface-name:wlan1

sudo systemctl restart NetworkManager
```

### Interface bloquée (rfkill)

```bash
# Vérifier
sudo rfkill list

# Débloquer
sudo rfkill unblock wifi
sudo rfkill unblock all
```

## 📊 Diagnostic complet

```bash
sudo ./wifiphisher_recovery.sh diagnose
```

Affiche:
- Toutes les interfaces réseau
- État des interfaces wireless
- Processus en cours
- État NetworkManager et WireGuard
- Dernières erreurs kernel
- Informations sur votre carte WiFi

## 🧪 Tests recommandés

### Test 1: Mode sans extensions (le plus stable)
```bash
sudo wifiphisher --noextensions -aI wlan1
```

### Test 2: Avec evil twin complet
```bash
# Sélectionner manuellement les interfaces
sudo wifiphisher -eI wlan1 -aI wlan1

# Ou laisser la détection automatique
sudo wifiphisher -i wlan1
```

### Test 3: Vérifier que le cleanup fonctionne
```bash
# Lancer et arrêter immédiatement avec Ctrl+C
sudo wifiphisher --noextensions -aI wlan1
# Appuyer sur Ctrl+C après quelques secondes

# Vérifier que l'interface est bien restaurée
ip link show wlan1
iw dev wlan1 info
# Devrait afficher "type managed"
```

## 🎯 Commandes utiles

### Voir les modes supportés par votre carte
```bash
iw list | grep -A 10 "Supported interface modes"
```

### Voir le driver utilisé
```bash
lspci -k | grep -A 3 -i network
# ou pour USB:
lsusb -v | grep -A 5 -i wireless
```

### Informations sur l'interface
```bash
iw dev wlan1 info
ip link show wlan1
ethtool -i wlan1
```

### Changer manuellement le mode
```bash
# Mode monitor
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Mode managed
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up
```

## 🚨 Que faire si rien ne fonctionne

1. **Redémarrer complètement le système**
   ```bash
   sudo reboot
   ```

2. **Après redémarrage, vérifier l'état**
   ```bash
   sudo ./wifiphisher_recovery.sh check
   ```

3. **Mettre à jour le firmware de la carte**
   ```bash
   sudo apt update
   sudo apt install linux-firmware
   sudo reboot
   ```

4. **Vérifier les logs système**
   ```bash
   dmesg | grep -iE "wlan|wifi|mt76|mt7921" | tail -30
   journalctl -xe | tail -50
   ```

5. **Créer un rapport de bug**
   ```bash
   sudo ./wifiphisher_recovery.sh diagnose > /tmp/diagnostic.txt
   # Partager diagnostic.txt dans une issue GitHub
   ```

## 📝 Notes importantes

### Cartes Mediatek
Les cartes Mediatek (notamment mt7921) peuvent être capricieuses:
- Préférer le mode `--noextensions` au début
- Laisser un délai entre les commandes
- Ne pas changer le mode trop rapidement

### WireGuard
- Les interfaces `wg*` sont maintenant automatiquement ignorées
- Vous pouvez garder votre VPN actif pendant l'utilisation
- Si problèmes, arrêter WireGuard temporairement

### NetworkManager
- Peut interférer avec les opérations
- Option `--keepnetworkmanager` existe mais peut causer des conflits
- Préférer rendre l'interface unmanaged

### Permissions
- **TOUJOURS** utiliser `sudo`
- Ne pas lancer en tant que root directement (utilisez sudo)

## 🔗 Ressources

- Documentation complète: `TROUBLESHOOTING.md`
- Détails techniques: `FIXES_README.md`
- Script de récupération: `wifiphisher_recovery.sh`
- Tests: `test_fixes.py`
