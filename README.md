# Vacon 100 FLOW — Custom Component Home Assistant

Intégration native pour le variateur **Vacon 100 FLOW** (Danfoss) via **Modbus TCP**.

## Entités créées

### Capteurs (lecture)
| Entité | Unité | Description |
|--------|-------|-------------|
| Fréquence sortie | Hz | Fréquence de sortie |
| Vitesse moteur | rpm | Vitesse moteur |
| Courant moteur | A | Courant moteur |
| Couple moteur | % | Couple moteur |
| Puissance | kW | Puissance active |
| Tension sortie | V | Tension de sortie |
| Tension bus DC | V | Tension bus DC |
| Température variateur | °C | Température interne |
| Énergie cumulée | kWh | Énergie totale |
| Consigne fréquence active | Hz | Consigne lue depuis variateur |

### Commandes (écriture)
| Entité | Description |
|--------|-------------|
| Marche / Arrêt | RUN / STOP |
| Sens inverse | Sens rotation FWD/REV |
| Consigne fréquence | 0–50 Hz (pas 0.1 Hz) |
| Reset défaut | Reset défaut actif |

## Installation via HACS

1. HACS → Intégrations → ⋮ → Dépôts personnalisés
2. URL : `https://github.com/vx4500/vacon100-flow-ha` — catégorie **Intégration**
3. Installer → Redémarrer HA
4. Paramètres → Appareils & Services → + Ajouter → **Vacon 100 FLOW**

## Configuration

| Champ | Valeur par défaut |
|-------|-------------------|
| Adresse IP | IP du variateur |
| Port | 502 |
| ID esclave | 1 |
| Intervalle | 10 secondes |

## Compatibilité

Testé sur **Vacon 100 FLOW** — `VACON0100-3L-xxxx-5-FLOW`
HA version minimale : 2023.1
