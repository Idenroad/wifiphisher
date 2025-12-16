# 📚 Index de la documentation Wifiphisher v2.0

> **Note**: Cette version (2.0) intègre le support WPA3 et consolide toute la documentation dans le README principal.  
> Les anciens fichiers FIXES_README.md et README_FIXES.txt ont été archivés dans README_ARCHIVE.md.

## 🚀 Par où commencer ?

### Vous démarrez avec Wifiphisher v2.0 ?
👉 Lisez **[README.md](README.md)** - Documentation complète avec installation et utilisation  
👉 Consultez **[QUICKSTART.md](QUICKSTART.md)** pour une mise en route rapide (5 min)

### Wifiphisher a crashé votre système ?
👉 Exécutez `sudo ./wifiphisher_recovery.sh restore`  
👉 Consultez **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** pour plus de détails

### Vous voulez comprendre ce qui a été modifié ?
👉 Lisez **[RESUME_MODIFICATIONS.md](RESUME_MODIFICATIONS.md)** (10 min)  
👉 Consultez **[CHANGELOG](CHANGELOG)** pour voir les nouveautés de la v2.0

### Vous êtes développeur et voulez les détails techniques ?
👉 Lisez **[CHANGELOG_FIXES.md](CHANGELOG_FIXES.md)** pour l'historique détaillé  
👉 Consultez **[README_ARCHIVE.md](README_ARCHIVE.md)** pour l'ancienne documentation

---

## 📖 Documentation principale

| Document | Description | Public |
|----------|-------------|--------|
| **[README.md](README.md)** | 📘 Documentation principale consolidée (installation, usage, troubleshooting) | 👤👨‍💻 Tous |
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 Guide rapide d'utilisation | 👤 Utilisateur |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 🔧 Guide de dépannage complet | 👤 Utilisateur |
| **[CHANGELOG](CHANGELOG)** | 📝 Historique des versions (incl. v2.0 WPA3) | 👤👨‍💻 Tous |

## 📚 Documentation technique

| Document | Description | Public |
|----------|-------------|--------|
| **[RESUME_MODIFICATIONS.md](RESUME_MODIFICATIONS.md)** | Résumé visuel des modifications | 👤👨‍💻 Tous |
| **[CHANGELOG_FIXES.md](CHANGELOG_FIXES.md)** | Historique détaillé des correctifs | 👨‍💻 Développeur |
| **[README_ARCHIVE.md](README_ARCHIVE.md)** | Archive des anciennes documentations | 👨‍💻 Développeur |

## 🛠️ Outils et scripts

| Fichier | Taille | Description | Usage |
|---------|--------|-------------|-------|
| **[wifiphisher_recovery.sh](wifiphisher_recovery.sh)** | 5.7 KB | Script de récupération système | `sudo ./wifiphisher_recovery.sh [check\|restore\|diagnose]` |
| **[test_fixes.py](test_fixes.py)** | 4.1 KB | Suite de tests de validation | `python3 test_fixes.py` |

## 🎯 Guide par situation

### Situation 1: Première utilisation de Wifiphisher v2.0
1. Lire [README.md](README.md) - Sections "Installation" et "Usage"
2. Consulter [QUICKSTART.md](QUICKSTART.md) pour démarrage rapide
3. Exécuter `sudo ./wifiphisher_recovery.sh check`
4. Lancer wifiphisher selon vos besoins

### Situation 2: Le système a crashé
1. **Action immédiate**: `sudo ./wifiphisher_recovery.sh restore`
2. Lire [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Section "Restauration manuelle"
3. Si problème persiste: `sudo ./wifiphisher_recovery.sh diagnose`

### Situation 3: Carte Mediatek problématique
1. Lire [README.md](README.md) - Section "Troubleshooting > Mediatek Chipsets"
2. Lire [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Section "Cartes Mediatek spécifiques"
3. Tester avec `--noextensions` d'abord

### Situation 4: Conflit avec WireGuard
1. Lire [README.md](README.md) - Section "Troubleshooting > WireGuard/VPN Conflicts"
2. Normalement, pas besoin d'arrêter WireGuard (géré automatiquement)
3. Si problème, consulter [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Situation 5: Découvrir le support WPA3
1. Lire [README.md](README.md) - Section "What's New in Version 2.0"
2. Consulter [CHANGELOG](CHANGELOG) - Section v2.0
3. Le support WPA3 est automatique via roguehostapd

### Situation 6: Contribuer ou modifier le code
1. Lire [CHANGELOG_FIXES.md](CHANGELOG_FIXES.md) pour le contexte
2. Consulter [README_ARCHIVE.md](README_ARCHIVE.md) pour l'historique
3. Exécuter les tests: `python3 test_fixes.py`

## 📋 Checklist rapide

### Avant de lancer wifiphisher v2.0
- [ ] J'ai lu [README.md](README.md) ou [QUICKSTART.md](QUICKSTART.md)
- [ ] J'ai exécuté `sudo ./wifiphisher_recovery.sh check`
- [ ] Je connais ma carte WiFi (Mediatek ? autre ?)
- [ ] Je sais si WireGuard est actif ou non
- [ ] J'ai installé les dépendances: `sudo python setup.py install`

### Après un crash
- [ ] J'ai exécuté `sudo ./wifiphisher_recovery.sh restore`
- [ ] J'ai vérifié que les interfaces sont restaurées: `ip link`
- [ ] J'ai consulté [TROUBLESHOOTING.md](TROUBLESHOOTING.md) si besoin
- [ ] J'ai fait un diagnostic si le problème persiste

### Pour rapporter un bug
- [ ] J'ai exécuté `sudo ./wifiphisher_recovery.sh diagnose > diagnostic.txt`
- [ ] J'ai noté ma carte WiFi: `lspci | grep -i network`
- [ ] J'ai consulté [README.md](README.md) - Section "Troubleshooting"
- [ ] J'ai les logs d'erreur

## 🔍 Recherche rapide

| Je cherche... | Document | Section |
|---------------|----------|---------|
| Commandes rapides | QUICKSTART.md | Toutes |
| Restaurer après crash | QUICKSTART.md | "En cas de problème" |
| Info sur carte Mediatek | TROUBLESHOOTING.md | "Cartes Mediatek spécifiques" |
| Gérer WireGuard | QUICKSTART.md | "Si vous avez WireGuard actif" |
| Détails techniques | FIXES_README.md | "Modifications apportées" |
| Liste des changements | CHANGELOG_FIXES.md | Tout le fichier |
| Résumé visuel | RESUME_MODIFICATIONS.md | Tout le fichier |
| NetworkManager | TROUBLESHOOTING.md | "Erreurs Interface managed by NetworkManager" |
| rfkill | QUICKSTART.md | "Interface bloquée (rfkill)" |
| Tests | FIXES_README.md | "Tests recommandés" |

## 💻 Commandes essentielles

```bash
# Vérifier l'état du système
sudo ./wifiphisher_recovery.sh check

# Restaurer après crash
sudo ./wifiphisher_recovery.sh restore

# Diagnostic complet
sudo ./wifiphisher_recovery.sh diagnose

# Lancer wifiphisher (mode safe)
sudo wifiphisher -eI wlan1 --noextensions

# Tester les correctifs
python3 test_fixes.py

# Voir les interfaces
ip link show
iw dev
```

## 📞 Besoin d'aide ?

1. **Consultez d'abord**: [QUICKSTART.md](QUICKSTART.md) et [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Diagnostic**: `sudo ./wifiphisher_recovery.sh diagnose`
3. **Rapport de bug**: Créer une issue GitHub avec le diagnostic

## 🎓 Ressources supplémentaires

- [README.md](README.md) - Documentation officielle wifiphisher
- [requirements.txt](requirements.txt) - Dépendances Python
- [wifiphisher/common/interfaces.py](wifiphisher/common/interfaces.py) - Code modifié

---

**Dernière mise à jour**: 15 décembre 2024  
**Version des correctifs**: 1.0  
**Compatibilité**: Toutes versions de wifiphisher

*Pour toute question, consultez d'abord cette documentation avant de créer une issue.*
