#!/bin/bash
# Script de diagnostic et restauration pour wifiphisher
# Usage: sudo ./wifiphisher_recovery.sh [check|restore|diagnose]

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}[!]${NC} Ce script doit être exécuté en tant que root (sudo)"
        exit 1
    fi
}

function diagnose() {
    echo -e "${GREEN}[*]${NC} Diagnostic du système..."
    echo ""
    
    echo -e "${YELLOW}=== Interfaces réseau ===${NC}"
    ip link show
    echo ""
    
    echo -e "${YELLOW}=== Interfaces wireless ===${NC}"
    iw dev
    echo ""
    
    echo -e "${YELLOW}=== État rfkill ===${NC}"
    rfkill list
    echo ""
    
    echo -e "${YELLOW}=== Processus wifiphisher/hostapd/dnsmasq ===${NC}"
    ps aux | grep -E "wifiphisher|hostapd|dnsmasq" | grep -v grep
    echo ""
    
    echo -e "${YELLOW}=== NetworkManager ===${NC}"
    systemctl status NetworkManager --no-pager | head -10
    echo ""
    
    echo -e "${YELLOW}=== WireGuard ===${NC}"
    wg show 2>/dev/null || echo "WireGuard non actif"
    echo ""
    
    echo -e "${YELLOW}=== Interfaces virtuelles wifiphisher ===${NC}"
    ip link | grep wfphshr || echo "Aucune interface virtuelle trouvée"
    echo ""
    
    echo -e "${YELLOW}=== Dernières erreurs kernel (interfaces réseau) ===${NC}"
    dmesg | grep -iE "wlan|wifi|mt76|mt7921|rtl88|ath" | tail -20
    echo ""
    
    echo -e "${YELLOW}=== Carte WiFi détectée ===${NC}"
    lspci | grep -i network
    lsusb | grep -i wireless
    echo ""
}

function restore() {
    echo -e "${GREEN}[*]${NC} Restauration du système..."
    
    # 1. Tuer les processus
    echo -e "${GREEN}[+]${NC} Arrêt des processus wifiphisher, hostapd, dnsmasq..."
    pkill -9 wifiphisher 2>/dev/null && echo "  - wifiphisher arrêté"
    pkill -9 hostapd 2>/dev/null && echo "  - hostapd arrêté"
    pkill -9 dnsmasq 2>/dev/null && echo "  - dnsmasq arrêté"
    
    # 2. Nettoyer les interfaces virtuelles
    echo -e "${GREEN}[+]${NC} Suppression des interfaces virtuelles..."
    for iface in $(ip link | grep wfphshr | awk -F: '{print $2}' | tr -d ' '); do
        ip link del $iface 2>/dev/null && echo "  - $iface supprimée"
    done
    
    # 3. Restaurer les interfaces wireless
    echo -e "${GREEN}[+]${NC} Restauration des interfaces WiFi en mode managed..."
    for iface in $(iw dev | grep Interface | awk '{print $2}'); do
        echo "  - Traitement de $iface..."
        ip link set $iface down 2>/dev/null
        iw dev $iface set type managed 2>/dev/null
        ip link set $iface up 2>/dev/null
        echo "    $iface restaurée en mode managed"
    done
    
    # 4. Débloquer rfkill
    echo -e "${GREEN}[+]${NC} Déblocage rfkill..."
    rfkill unblock wifi
    rfkill unblock all
    
    # 5. Nettoyer iptables
    echo -e "${GREEN}[+]${NC} Nettoyage des règles iptables..."
    iptables -F 2>/dev/null
    iptables -X 2>/dev/null
    iptables -t nat -F 2>/dev/null
    iptables -t nat -X 2>/dev/null
    iptables -t mangle -F 2>/dev/null
    iptables -t mangle -X 2>/dev/null
    
    # 6. Redémarrer NetworkManager
    echo -e "${GREEN}[+]${NC} Redémarrage de NetworkManager..."
    systemctl restart NetworkManager
    sleep 2
    
    echo ""
    echo -e "${GREEN}[✓]${NC} Restauration terminée!"
    echo ""
}

function check_interfaces() {
    echo -e "${GREEN}[*]${NC} Vérification des interfaces WiFi..."
    
    has_wifi=false
    for iface in $(iw dev 2>/dev/null | grep Interface | awk '{print $2}'); do
        has_wifi=true
        echo ""
        echo -e "${YELLOW}Interface: $iface${NC}"
        
        # Mode actuel
        mode=$(iw dev $iface info | grep type | awk '{print $2}')
        echo "  Mode: $mode"
        
        # Capacités
        echo "  Modes supportés:"
        iw phy$(iw dev $iface info | grep wiphy | awk '{print $2}') info | grep -A 10 "Supported interface modes" | grep -E "monitor|AP" | sed 's/^/    /'
        
        # rfkill
        if rfkill list | grep -q "$iface.*blocked: yes"; then
            echo -e "  ${RED}BLOQUÉ par rfkill${NC}"
        else
            echo -e "  ${GREEN}Non bloqué${NC}"
        fi
        
        # NetworkManager
        if nmcli dev | grep "$iface" | grep -q "unmanaged"; then
            echo -e "  NetworkManager: ${GREEN}unmanaged${NC}"
        else
            echo -e "  NetworkManager: ${YELLOW}managed${NC}"
        fi
        
        # Driver
        driver=$(basename $(readlink /sys/class/net/$iface/device/driver) 2>/dev/null)
        echo "  Driver: ${driver:-inconnu}"
        
        # Chipset
        if [ -e "/sys/class/net/$iface/device/uevent" ]; then
            vendor=$(cat /sys/class/net/$iface/device/vendor 2>/dev/null)
            device=$(cat /sys/class/net/$iface/device/device 2>/dev/null)
            echo "  Chipset: $vendor:$device"
        fi
    done
    
    if [ "$has_wifi" = false ]; then
        echo -e "${RED}[!]${NC} Aucune interface WiFi détectée!"
    fi
    echo ""
}

function main() {
    check_root
    
    case "$1" in
        diagnose)
            diagnose
            ;;
        restore)
            restore
            ;;
        check)
            check_interfaces
            ;;
        *)
            echo "Usage: $0 {check|restore|diagnose}"
            echo ""
            echo "  check     - Vérifier l'état des interfaces WiFi"
            echo "  restore   - Restaurer le système après un crash"
            echo "  diagnose  - Diagnostic complet du système"
            echo ""
            exit 1
            ;;
    esac
}

main "$@"
