"""
Configuration — Notifications ntfy
===================================
Règles et seuils pour l'envoi de notifications via ntfy.sh

Ce fichier est séparé de config.py pour isoler la configuration des
notifications de la configuration de capture/rendu. capture.py fait
un import optionnel : si ce fichier est absent ou mal formé, le système
fonctionne sans notifications (tous les events restent quand même loggés
dans capture_errors.json).

Activation globale :
    Définir la variable d'environnement NTFY_TOPIC_URL
    → GitHub Secrets > NTFY_TOPIC_URL
    → valeur type : "https://ntfy.sh/ton-topic-secret-xYz123"

Si NTFY_TOPIC_URL est vide ou absent → aucune notif envoyée (silencieux).

Trois modes possibles par type d'événement :
    - "immediate"       : notif à chaque cycle où l'event apparaît
                          (agrégée si plusieurs events du même type sur le
                           même cycle, zones listées dans le body)
    - "batch_per_cycle" : max 1 notif/cycle résumant tous les events du type
    - "episode"         : notif à l'ouverture (après N cycles consécutifs),
                          silence pendant l'épisode,
                          notif à la clôture avec stats (1 cycle sans event
                          suffit pour clôturer)
"""

# ─── Seuil d'ouverture d'épisode ──────────────────────────────────────────────
# Nombre de cycles consécutifs d'apparition avant d'ouvrir un épisode.
# 1 seul cycle "propre" suffit ensuite à clôturer.
# Reset dur : un cycle sans l'event remet le compteur de streak à 0.
NTFY_EPISODE_OPEN_THRESHOLD = 3


# ─── Règles par type d'événement ──────────────────────────────────────────────
NTFY_NOTIFICATIONS = {
    # ─── Niveau 1 : événements immédiats (rares, critiques) ───────────────
    "data_freeze": {
        "enabled": True,
        "mode": "immediate",
        "priority": 4,                              # 1=min 5=max
        "tags": ["warning", "snowflake"],           # rendus en émojis par ntfy
        "title": "Gel API TomTom detecte",
    },
    "data_freeze_recovered": {
        "enabled": True,
        "mode": "immediate",
        "priority": 3,
        "tags": ["white_check_mark"],
        "title": "API TomTom rafraichie",
    },
    "zone_capture_failed": {
        "enabled": True,
        "mode": "immediate",
        "priority": 5,
        "tags": ["rotating_light"],
        "title": "Echec capture zone",
    },

    # ─── Niveau 2 : batch par cycle (événements fréquents bornés) ─────────
    "partial_capture": {
        "enabled": True,
        "mode": "batch_per_cycle",
        "priority": 2,
        "tags": ["warning"],
        "title": "Captures partielles",
    },
    "api_request_error": {
        "enabled": True,
        "mode": "batch_per_cycle",
        "priority": 3,
        "tags": ["warning"],
        "title": "Erreurs reseau TomTom",
    },

    # ─── Niveau 3 : mode épisode (événements massifs) ─────────────────────
    "api_http_error": {
        "enabled": True,
        "mode": "episode",
        "priority": 4,
        "tags": ["warning"],
        "title_open": "Erreurs HTTP TomTom (DEBUT episode)",
        "title_close": "Erreurs HTTP TomTom resolues",
    },
    "api_timeout": {
        "enabled": True,
        "mode": "episode",
        "priority": 3,
        "tags": ["hourglass"],
        "title_open": "Timeouts TomTom (DEBUT episode)",
        "title_close": "Timeouts TomTom resolus",
    },
}
