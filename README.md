# TomTom Traffic Capture — Vector Flow Edition

Capture automatique du trafic routier (A13/A2, Grisons) via l'**API TomTom**, orchestrée par GitHub Actions.

## Principe

```
┌──────────────────────────────────────────────────────────┐
│  3 couches superposées par Pillow                        │
│                                                          │
│  1. 🗺️  Carte de base    → API Static Image (1 requête) │
│  2. 🚗  Traffic Flow      → Vector Tiles (.pbf)          │
│     ├── Filtrage par type de route (motorway, major…)    │
│     ├── Épaisseur proportionnelle à la catégorie         │
│     └── Couleurs relative0 de plan.tomtom.com            │
│  3. ⚠️  Incidents         → API v5 + pointillés Pillow   │
└──────────────────────────────────────────────────────────┘
```

## vs Versions précédentes

|                  | Playwright (v1) | Raster tiles (v2) | **Vector tiles (v3)** |
|------------------|-----------------|--------------------|-----------------------|
| Dépendances      | Chromium ~400MB | requests + Pillow  | **requests + Pillow** |
| Temps/capture    | ~45s            | ~5s                | **~5s**               |
| Fiabilité        | Fragile         | Déterministe       | **Déterministe**      |
| Filtrage routes  | ✗               | ✗                  | **✓ par catégorie**   |
| Charte TomTom    | ~80%            | ~60%               | **~95%**              |
| Épaisseur lignes | Non contrôlable | Fixe               | **Par type de route** |

## Configuration

Tout se configure dans `capture.py` :

```python
# Zones — collez directement l'URL de plan.tomtom.com
ZONES = {
    "zone_globale_A2_A13": "https://plan.tomtom.com/en/?p=46.68973,8.93561,8.55z",
    "zone_A13_Chur":       "https://plan.tomtom.com/en/?p=46.89942,9.32459,9.75z",
    "zone_Chur_Isla-T":    "https://plan.tomtom.com/en/?p=46.84086,9.45618,12.17z",
}

# Filtrage des routes par zoom — ajustable
ROAD_TYPES_BY_ZOOM = {
    8:  [0],            # Motorway uniquement
    9:  [0, 1],         # + International
    10: [0, 1, 2],      # + Major
    12: [0, 1, 2, 3],   # + Secondary
}
```

### Ajouter une zone

1. Aller sur [plan.tomtom.com](https://plan.tomtom.com/)
2. Naviguer/zoomer jusqu'à la vue souhaitée
3. Copier l'URL du navigateur
4. Ajouter dans `ZONES`

### Types de route (roadTypes)

| Code | Type              | Exemple              |
|------|-------------------|----------------------|
| 0    | Motorway          | A2, A13              |
| 1    | International road| Routes nationales    |
| 2    | Major road        | Routes cantonales    |
| 3    | Secondary road    | Routes régionales    |
| 4    | Connecting road   | Liaisons locales     |
| 5+   | Local roads       | Routes communales    |

### Charte visuelle (relative0)

| État du trafic        | Couleur   | traffic_level |
|-----------------------|-----------|---------------|
| Fluide                | 🟢 Vert   | ≥ 0.75        |
| Ralenti               | 🟡 Jaune  | 0.35 – 0.75   |
| Congestionné          | 🟠 Orange | 0.15 – 0.35   |
| Très congestionné     | 🔴 Rouge  | < 0.15         |
| Fermé                 | ⬛ Rouge foncé | road_closure  |

## Installation

### 1. Clé API TomTom (gratuite)

1. Créer un compte sur [developer.tomtom.com](https://developer.tomtom.com/)
2. Créer une application → copier la **API Key**
3. Dans le repo GitHub : **Settings → Secrets → New repository secret**
   - Nom : `TOMTOM_API_KEY`
   - Valeur : votre clé

### 2. Activer le workflow

Le workflow démarre automatiquement via cron. Pour un lancement manuel :
**Actions → TomTom Traffic Capture (Vector Flow) → Run workflow**

## Développement local

```bash
export TOMTOM_API_KEY="votre_clé"
pip install requests Pillow
python capture.py
```

## Captures

Les captures sont sur la branche `captures` :
- **Naviguer** : [branche captures](../../tree/captures)
- **ZIP complet** : [télécharger](../../archive/refs/heads/captures.zip)
