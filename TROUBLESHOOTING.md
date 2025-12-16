# Guide de dépannage Wifiphisher

## Problèmes courants et solutions

### 1. Crash du système avec les cartes Mediatek

**Symptômes:**
- Le système devient instable après le lancement de wifiphisher
- Impossible d'ouvrir de nouveaux terminaux
- Le système se fige complètement

**Causes:**
- Certaines cartes WiFi Mediatek (mt76, mt7921, etc.) ont des drivers qui ne gèrent pas bien les changements de mode monitor/managed
- Tentatives répétées de changement de mode sans délai suffisant
- Conflits avec NetworkManager

**Solutions appliquées dans le code:**

1. **Mécanisme de retry** - Les changements de mode sont maintenant tentés jusqu'à 3 fois avec un délai de 0.5s
2. **Fallback ip link** - Si pyric échoue, on utilise la commande `ip link` comme alternative
3. **Cleanup robuste** - Le nettoyage en cas d'erreur ne fait plus crasher le programme
4. **Restauration du mode managed** - Les interfaces sont restaurées en mode managed lors de la sortie

**Solutions manuelles supplémentaires:**

```bash
# Avant de lancer wifiphisher, désactiver NetworkManager
sudo systemctl stop NetworkManager

# Mettre manuellement l'interface en mode monitor
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Après utilisation, restaurer:
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up
sudo systemctl start NetworkManager
```

### 2. Conflits avec WireGuard

**Symptômes:**
- Wifiphisher ne démarre pas correctement
- Erreurs liées aux interfaces réseau
- Perte de connexion VPN

**Causes:**
- WireGuard crée des interfaces (wg0, wg1) qui peuvent être détectées par wifiphisher
- Tentatives de manipulation des interfaces VPN par wifiphisher
- Conflits de routing

**Solutions appliquées dans le code:**

Le code ignore maintenant automatiquement les interfaces:
- `wg*` (WireGuard)
- `tun*` (OpenVPN, autres VPN)
- `tap*` (VPN bridge mode)
- `docker*` (Docker)
- `veth*` (Virtual ethernet)
- `br-*` (Bridge)
- `vmnet*` (VMs)
- `lo` (Loopback)

**Solutions manuelles:**

```bash
# Option 1: Arrêter WireGuard temporairement
sudo wg-quick down wg0

# Option 2: Utiliser --protectinterface
sudo wifiphisher --protectinterface wg0

# Après utilisation:
sudo wg-quick up wg0
```

### 3. Erreurs "Interface managed by NetworkManager"

**Solutions:**

```bash
# Configuration permanente dans /etc/NetworkManager/conf.d/unmanaged.conf
[keyfile]
unmanaged-devices=interface-name:wlan1

# Puis redémarrer NetworkManager
sudo systemctl restart NetworkManager
```

### 4. Carte WiFi bloquée (rfkill)

**Diagnostic:**
```bash
sudo rfkill list
```

**Solution:**
```bash
sudo rfkill unblock wifi
sudo rfkill unblock all
```

### 5. Permissions insuffisantes

**Solution:**
```bash
# Toujours lancer avec sudo
sudo wifiphisher [options]
```

### 6. Logs pour le debugging

**Activer les logs détaillés:**
```bash
# Les logs sont dans:
cat /var/log/wifiphisher.log

# Ou lancer en mode verbose (si disponible)
sudo wifiphisher --debug [autres options]
```

### 7. Restauration manuelle en cas de crash

Si wifiphisher crashe et ne nettoie pas correctement:

```bash
# 1. Arrêter tous les processus liés
sudo pkill -9 wifiphisher
sudo pkill -9 hostapd
sudo pkill -9 dnsmasq

# 2. Restaurer les interfaces
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up

# 3. Nettoyer les règles iptables
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X

# 4. Redémarrer NetworkManager
sudo systemctl restart NetworkManager

# 5. Supprimer les interfaces virtuelles créées
for iface in $(ip link | grep wfphshr | awk -F: '{print $2}' | tr -d ' '); do
    sudo ip link del $iface
done
```

### 8. Cartes Mediatek spécifiques

**MT7921 (RTL8852AE et similaires):**
- Ces cartes nécessitent parfois un firmware spécifique à jour
- Vérifier: `dmesg | grep mt76` ou `dmesg | grep mt7921`

**Update firmware:**
```bash
sudo apt update
sudo apt install linux-firmware
# Ou manuellement depuis:
# https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
```

**Drivers alternatifs:**
```bash
# Vérifier le driver actuel
lspci -k | grep -A 3 -i network

# Parfois, recharger le module aide:
sudo modprobe -r mt7921e
sudo modprobe mt7921e
```

## Rapport de bugs

Si les problèmes persistent, créer un rapport avec:

```bash
# Informations système
uname -a
lspci | grep -i network
lsusb | grep -i wireless
dmesg | tail -50
rfkill list
ip link
```

Et poster sur: https://github.com/wifiphisher/wifiphisher/issues
