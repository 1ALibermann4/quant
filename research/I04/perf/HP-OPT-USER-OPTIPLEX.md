# I04-CAL Runner — instructions OptiPlex (L10)

## Pour l’ami qui prête la machine

1. Copier `quant-I04-CAL-runner.zip` sur le PC (clé USB OK).
2. Décompresser dans un dossier local (ex. `Desktop\quant-I04-CAL-runner`).
3. Double-cliquer **`START_WINDOWS.cmd`**.
4. Accepter l’installation **locale** (venv `.venv` — pas besoin d’admin).
5. Laisser tourner jusqu’à l’arrêt automatique (~16 h, marge 20 min).
6. À la fin, copier tout le dossier (surtout `results\`, `checkpoints\`, `logs\`, `reports\`) sur la clé USB et le rendre.

## Variables optionnelles (avant lancement)

```text
set I04_CAL_MACHINE=OPTIPLEX
set MAX_RUNTIME_HOURS=16
set SHUTDOWN_MARGIN_MINUTES=20
```

Sur l’ASUS : `set I04_CAL_MACHINE=ASUS` puis le même `START_WINDOWS.cmd`.

## Arrêt manuel

Fermer la fenêtre console : les checkpoints déjà écrits restent. Relancer `START_WINDOWS.cmd` reprend (`--resume`).

## Interdits

- Ne pas modifier les fichiers JSON à la main.
- Ne pas installer de « winner » ni de données de marché.
- Ne pas lancer deux fois le même `I04_CAL_MACHINE` sur deux PC (chevauchement).
