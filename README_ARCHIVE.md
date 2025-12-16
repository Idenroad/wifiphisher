# Archive - Anciennes documentations

> **Note**: Ce fichier archive les anciennes documentations qui ont été intégrées dans le README.md principal. Il est conservé pour référence historique.

---

## FIXES_README.md (Archive)

# Correctifs pour les problèmes de stabilité avec Mediatek et WireGuard

## Modifications apportées

### 1. Fichier: `wifiphisher/common/interfaces.py`

#### Changements principaux:

**a) Exclusion automatique des interfaces VPN et virtuelles**
- Les interfaces WireGuard (`wg*`), OpenVPN (`tun*`, `tap*`), Docker, etc. sont maintenant automatiquement ignorées
- Évite les conflits avec les VPN actifs

**b) Mécanisme de retry pour les changements de mode**
- 3 tentatives avec délai de 0.5s entre chaque tentative
- Résout les problèmes avec les drivers Mediatek qui peuvent être lents ou instables

**c) Fallback sur `ip link` pour les opérations d'interface**
- Si `pyric.pyw` échoue, on utilise la commande `ip link` comme alternative
- Améliore la compatibilité avec les drivers problématiques

**d) Cleanup robuste et sûr**
- Les erreurs lors du nettoyage ne font plus crasher le programme
- Restauration automatique en mode managed
- Gestion d'erreur pour chaque interface individuellement

### 2. Nouveaux fichiers

**`TROUBLESHOOTING.md`**
- Guide complet de dépannage
- Solutions pour les problèmes courants
- Commandes de restauration manuelle
- Informations spécifiques aux cartes Mediatek

**`wifiphisher_recovery.sh`**
- Script de récupération automatique
- 3 modes: `check`, `restore`, `diagnose`
- Permet de restaurer le système après un crash

## Utilisation

### Avant de lancer wifiphisher

Si vous avez une carte Mediatek ou WireGuard actif:

```bash
# 1. Vérifier l'état des interfaces
sudo ./wifiphisher_recovery.sh check

# 2. (Optionnel) Arrêter WireGuard temporairement
sudo wg-quick down wg0

# 3. Lancer wifiphisher normalement
sudo wifiphisher [options]
```

### En cas de crash

```bash
# Restaurer automatiquement le système
sudo ./wifiphisher_recovery.sh restore
```

### Pour diagnostiquer un problème

```bash
# Diagnostic complet
sudo ./wifiphisher_recovery.sh diagnose
```

## Tests recommandés

### Test 1: Interface Mediatek seule
```bash
sudo wifiphisher -i wlan1 --noextensions
```

### Test 2: Avec WireGuard actif
```bash
# Laisser WireGuard tourner
sudo wifiphisher -i wlan1 --noextensions
# Les interfaces wg* doivent être automatiquement ignorées
```

### Test 3: Vérification du cleanup
```bash
sudo wifiphisher -i wlan1 --noextensions
# Ctrl+C pour arrêter
# Vérifier que l'interface est bien restaurée:
ip link show wlan1
iw dev wlan1 info
```

## Problèmes connus résolus

✅ **Crash système avec cartes Mediatek**
- Résolu par le mécanisme de retry et le fallback ip link

✅ **Conflit avec WireGuard**
- Résolu par l'exclusion automatique des interfaces wg*

✅ **Terminal inutilisable après crash**
- Résolu par le cleanup robuste et le script de récupération

✅ **Interface reste en mode monitor**
- Résolu par la restauration automatique en mode managed

## Améliorations futures possibles

- [ ] Détecter automatiquement les drivers problématiques (via `lspci`)
- [ ] Proposer un mode "safe" pour les cartes Mediatek
- [ ] Sauvegarder l'état complet des interfaces avant modification
- [ ] Ajouter un watchdog pour détecter les freeze

## Logs et debug

Les logs détaillés sont maintenant disponibles dans les opérations critiques:

```python
logger.info("Successfully set {interface_name} to {mode} mode")
logger.warning("Failed to set mode on attempt {attempt + 1}, retrying...")
logger.error("Failed to bring up {interface_name} with ip link: {e}")
```

Pour voir ces logs en temps réel:
```bash
# Si wifiphisher utilise le logger Python
tail -f /var/log/syslog | grep wifiphisher
```

## Contribution

Si vous rencontrez encore des problèmes:

1. Exécuter le diagnostic:
   ```bash
   sudo ./wifiphisher_recovery.sh diagnose > diagnostic.txt
   ```

2. Créer une issue avec:
   - Le fichier `diagnostic.txt`
   - Le modèle exact de votre carte WiFi (`lspci | grep -i network`)
   - Les logs d'erreur
   - Les commandes utilisées

## Licence

Ces modifications suivent la même licence que wifiphisher (GPL v3).

---

## README_FIXES.txt (Archive)

```
CORRECTIFS WIFIPHISHER - Résumé
Lisez INDEX.md pour commencer!

Fichiers créés:
CHANGELOG_FIXES.md
FIXES_README.md
INDEX.md
QUICKSTART.md
RESUME_MODIFICATIONS.md
test_fixes.py
TROUBLESHOOTING.md
wifiphisher_recovery.sh
```

---

**Note**: Toutes ces informations ont été consolidées dans le README.md principal et dans TROUBLESHOOTING.md.
