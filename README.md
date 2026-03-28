# TomTom Traffic Capture — API Edition

Capture automatique du trafic routier (A13, Grisons) via l'**API TomTom** toutes les 10 minutes, orchestrée par GitHub Actions.

## Principe

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  GitHub      │────▶│  capture.py      │────▶│  branche     │
│  Actions     │     │  (requests +     │     │  captures/   │
│  (cron 10m)  │     │   Pillow)        │     │  (JPEG)      │
└─────────────┘     └──────────────────┘     └──────────────┘
                            │
                    ┌───────┼───────┐
                    ▼       ▼       ▼
              Base Map   Flow    Incidents
              (tuiles)  (tuiles)  (tuiles)
                    │       │       │
                    └───────┼───────┘
                            ▼
                     Composite JPEG
                     1920 × 1080
```

**3 couches superposées :**
1. 🗺️ Carte de base (Map Display API)
2. 🟢🟡🔴 Traffic Flow — vitesse relative sur les segments
3. ⚠️ Traffic Incidents — bouchons et incidents

## vs Ancienne version (Playwright)

| | Playwright (v1) | API (v2) |
|---|---|---|
| Dépendances | Chromium (~400 MB) | requests + Pillow (~5 MB) |
| Temps/capture | ~45s (3 zones) | ~5s (3 zones) |
| Fiabilité | Fragile (popups, modals) | Déterministe |
| Budget | N/A | ~15'500 / 50'000 tuiles/jour |

## Installation

### 1. Clé API TomTom (gratuite)

1. Créer un compte sur [developer.tomtom.com](https://developer.tomtom.com/)
2. Créer une application → copier la **API Key**
3. Dans le repo GitHub : **Settings → Secrets → New repository secret**
   - Nom : `TOMTOM_API_KEY`
   - Valeur : votre clé

### 2. Activer le workflow

Le workflow démarre automatiquement via cron. Pour un lancement manuel :
**Actions → TomTom Traffic Capture (API) → Run workflow**

## Configuration

Tout se configure dans `capture.py` :

```python
# Zones — collez directement l'URL de plan.tomtom.com
ZONES = {
    "zone_globale_A2_A13": "https://plan.tomtom.com/en/?p=46.68973,8.93561,8.55z",
    "zone_A13_Chur":       "https://plan.tomtom.com/en/?p=46.89942,9.32459,9.75z",
    "zone_Chur_Isla-T":    "https://plan.tomtom.com/en/?p=46.84086,9.45618,12.17z",
}

VIEWPORT_WIDTH  = 1920       # Largeur de l'image finale
VIEWPORT_HEIGHT = 1080       # Hauteur
TILE_SIZE       = 512        # 512×512 (meilleure qualité)
RETENTION_DAYS  = 7          # Durée de conservation
```

### Ajouter une zone

1. Aller sur [plan.tomtom.com](https://plan.tomtom.com/)
2. Naviguer/zoomer jusqu'à la vue souhaitée
3. Copier l'URL du navigateur
4. Ajouter dans `ZONES` :
```python
"ma_nouvelle_zone": "https://plan.tomtom.com/en/?p=47.12345,8.54321,11.5z",
```

Le système extrait automatiquement lat, lon et zoom depuis l'URL.
Le zoom fractionnaire (ex: 8.55) est arrondi à l'entier le plus proche.

### Budget tuiles

| Paramètre | Impact |
|---|---|
| +1 zone | +36 tuiles/capture |
| Zoom +1 | ~même nombre de tuiles |
| Intervalle ÷2 | Budget ×2 |

## Captures

Les captures sont sur la branche `captures` :
- **Naviguer** : [branche captures](../../tree/captures)
- **ZIP complet** : [télécharger](../../archive/refs/heads/captures.zip)

## Développement local

```bash
export TOMTOM_API_KEY="votre_clé"
pip install -r requirements.txt
python capture.py
```
