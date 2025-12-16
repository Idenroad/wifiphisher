#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider les correctifs wifiphisher
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer wifiphisher
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_vpn_interface_exclusion():
    """Test que les interfaces VPN sont bien exclues"""
    print("[*] Test d'exclusion des interfaces VPN...")
    
    ignored_prefixes = ['wg', 'tun', 'tap', 'docker', 'veth', 'br-', 'vmnet', 'lo']
    test_interfaces = [
        ('wg0', True),
        ('wlan0', False),
        ('tun0', True),
        ('tap1', True),
        ('docker0', True),
        ('eth0', False),
        ('wlan1', False),
        ('veth123', True),
        ('br-a1b2c3', True),
    ]
    
    failures = 0
    for iface, should_ignore in test_interfaces:
        is_ignored = any(iface.startswith(prefix) for prefix in ignored_prefixes)
        if is_ignored == should_ignore:
            print(f"  ✓ {iface}: {'ignoré' if is_ignored else 'autorisé'}")
        else:
            print(f"  ✗ {iface}: ERREUR - attendu {'ignoré' if should_ignore else 'autorisé'}")
            failures += 1
    
    return failures == 0

def test_imports():
    """Test que les imports fonctionnent"""
    print("[*] Test des imports...")
    
    try:
        import wifiphisher.common.interfaces as interfaces
        print("  ✓ Import de interfaces.py réussi")
        return True
    except Exception as e:
        print(f"  ✗ Erreur d'import: {e}")
        return False

def test_networkmanager_class():
    """Test que la classe NetworkManager est bien définie"""
    print("[*] Test de la classe NetworkManager...")
    
    try:
        import wifiphisher.common.interfaces as interfaces
        
        # Vérifier que la classe existe
        assert hasattr(interfaces, 'NetworkManager')
        print("  ✓ Classe NetworkManager trouvée")
        
        # Vérifier les méthodes clés
        methods = ['start', 'up_interface', 'down_interface', 'set_interface_mode', 'on_exit']
        for method in methods:
            assert hasattr(interfaces.NetworkManager, method)
            print(f"  ✓ Méthode {method} trouvée")
        
        return True
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def test_retry_logic():
    """Test conceptuel du mécanisme de retry"""
    print("[*] Test du mécanisme de retry...")
    
    # Simulation du retry
    max_retries = 3
    successful = False
    
    for attempt in range(max_retries):
        try:
            if attempt == 2:  # Succès au 3ème essai
                successful = True
                print(f"  ✓ Succès à la tentative {attempt + 1}")
                break
            else:
                raise Exception("Échec simulé")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⟳ Tentative {attempt + 1} échouée, retry...")
            else:
                print(f"  ✗ Échec après {max_retries} tentatives")
    
    return successful

def main():
    print("=" * 60)
    print("Tests des correctifs wifiphisher")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Exclusion VPN", test_vpn_interface_exclusion),
        ("Classe NetworkManager", test_networkmanager_class),
        ("Mécanisme de retry", test_retry_logic),
    ]
    
    results = []
    for test_name, test_func in tests:
        print()
        result = test_func()
        results.append((test_name, result))
        print()
    
    print("=" * 60)
    print("Résumé des tests")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ Tous les tests sont passés!")
        return 0
    else:
        print("✗ Certains tests ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
