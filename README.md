# search-video-google-cloud-tech

Page de recherche dans les vidéos de la chaîne YouTube [Google Cloud Tech](https://www.youtube.com/@googlecloudtech), taguées automatiquement par technologie (BigQuery, Dataflow, GKE, Vertex AI, ADK...) et regroupées par famille (Data & Analytics, Bases de données, IA & Machine Learning, Compute...).

**Page :** https://xavinsky.github.io/search-video-google-cloud-tech/ — filtrage par famille, par tag (cumulables), par chaîne, par plage de dates, par mot du titre ; tri par titre, durée, vues ou date. Un seul fichier HTML autonome, qui fonctionne aussi hors ligne une fois généré dans `docs/index.html`.

## Publication automatique

Le workflow `.github/workflows/pages.yml` génère la page et la publie sur GitHub Pages :

| Déclencheur | Effet |
|-------------|-------|
| push sur `main` touchant les données, les scripts, le template ou `channels.json` | regénère et publie la page, sans crawl |
| le 1er de chaque mois | crawl des nouvelles vidéos, commit de `data/videos.json` s'il y a du nouveau, puis publication |
| lancement manuel (onglet Actions, « Run workflow ») | idem |

Le crawl en CI est toujours incrémental : il s'arrête dès qu'une page ne contient plus de nouveauté. Le parcours complet (`--full`) se lance uniquement en local, quand c'est nécessaire.

Le commit de la base n'a lieu que si des vidéos ont été ajoutées ou des dates précisées. Les vues rafraîchies seules ne créent pas de commit, mais la page publiée en tient compte. Si YouTube bloque le crawl depuis GitHub, l'étape échoue sans bloquer la publication de la base existante : lancer alors la mise à jour en local et pousser. Après un crawl mensuel ou manuel, faire `git pull` avant de pousser des modifications locales.

Les vidéos non classées apparaissent en avertissements dans le résumé de l'exécution.

GitHub Pages doit être configuré avec la source « GitHub Actions » (Settings, Pages).

## Mettre à jour en local

```bash
python3 scripts/update.py
```

Sans dépendance externe (Python 3 seulement). YouTube limite le débit : en cas de réponses 429 répétées, le script s'arrête et se relance plus tard, ou avec un `--delay` plus grand. Le script :

1. parcourt la playlist « uploads » de chaque chaîne de `channels.json`, de la plus récente vidéo vers le passé, et s'arrête dès qu'une page de 100 vidéos ne contient plus rien de nouveau ;
2. ajoute les nouvelles vidéos à `data/videos.json` avec une date approximative (déduite du « 3 days ago » affiché dans la liste), puis consulte la page de chaque nouvelle vidéo pour obtenir la date de publication exacte, la durée et le nombre de vues ;
3. régénère `docs/index.html`, et liste les vidéos qu'aucun tag ne couvre.

Options :

| Option | Effet |
|--------|-------|
| `--full` | parcourt toute la playlist même sans nouveauté (rattrapage, ajout d'une chaîne) |
| `--details N` | nombre maximum de pages vidéo consultées pour les dates exactes (défaut 200, `0` pour désactiver) |
| `--no-build` | ne régénère pas la page |
| `--delay S` | pause entre deux requêtes YouTube (défaut 0.5 s) |

Régénérer la page seule (après une modification des tags ou du template) : `python3 scripts/build.py`.

## Vidéos non classées

Règle : **aucun tag fourre-tout**. Quand `build.py` liste des vidéos sans tag, leur trouver un tag précis dans `scripts/tags.py` :

- sujet récurrent → ajouter un motif à la regex du tag concerné, ou créer un tag dans la bonne famille de `GROUPS` ;
- titre isolé → l'ajouter à `MANUAL_OVERRIDES` avec le tag existant le plus proche.

Tester une regex avant de l'ajouter : `python3 -c "import re; print(re.search(r'motif', 'Titre de la vidéo', re.I))"`.

## Ajouter une chaîne

Ajouter une entrée dans `channels.json` (`name`, `channel_id`, `uploads_playlist`, `url`) puis lancer `python3 scripts/update.py --full`. La playlist « uploads » d'une chaîne a pour identifiant `UU` suivi de l'identifiant de chaîne sans son préfixe `UC`. Un filtre « Chaînes » apparaît sur la page dès qu'il y a plus d'une chaîne.

## Fichiers

```
channels.json          chaînes à parcourir
data/videos.json       base des vidéos (id, titre, chaîne, durée, vues, date, précision de la date)
scripts/youtube.py     accès YouTube : listing d'une playlist par pages de 100, détails d'une vidéo
scripts/update.py      mise à jour incrémentale de la base + régénération
scripts/build.py       taggage et génération de docs/index.html
scripts/tags.py        taxonomie : familles → tags → regex sur le titre, corrections manuelles
scripts/db.py          lecture/écriture de data/videos.json
templates/index.html   template de la page (placeholders __DATA_JSON__, __GROUPS_JSON__, __CHANNELS_JSON__, __UPDATED__)
docs/index.html        page générée, non versionnée — ne jamais éditer à la main
.github/workflows/     génération et publication sur GitHub Pages, crawl mensuel ou manuel
```

## Comment ça marche

Le listing lit la page HTML de la playlist (`ytInitialData`) puis appelle l'API de continuation `youtubei/v1/browse` que le site utilise lui-même pour le défilement infini. Les métadonnées sont dans les blocs `lockupViewModel` (identifiant, titre, durée en badge, vues arrondies, date relative). La page d'une vidéo expose `publishDate`, `lengthSeconds` et `viewCount` exacts. Ces structures sont celles du site YouTube et peuvent changer sans préavis : si le listing renvoie 0 vidéo, c'est l'extraction de `scripts/youtube.py` qui est à adapter.

## Licence

[MIT](LICENSE).
