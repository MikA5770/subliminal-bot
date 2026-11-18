# Subliminal – robot de publication

Deux fois par jour, ce robot crée une nouvelle vidéo « satisfaisante », puis la publie sur TikTok, Instagram (Reel) et YouTube (Short) via Buffer. Tout est gratuit.

## Ce que fait chaque passage

1. **Choix du format.** Le robot prend l'un des 10 formats, jamais un des 3 derniers publiés. Il favorise ceux qui ont été le moins utilisés.
2. **Variation.** Il tire au hasard l'accroche, l'instrument, la mélodie, le mot secret (mode Mystery) et parfois les couleurs.
3. **Contrôle qualité.** Il simule jusqu'à 40 parties et garde la plus intéressante : victoire de justesse, Color War serrée sans égalité, durée correcte.
4. **Vidéo.** Il fabrique le MP4 en 1080 × 1920, avec le son et le numéro d'épisode de la série.
5. **Hébergement.** Il dépose la vidéo sur la branche `media` du dépôt. Seules les 8 dernières sont gardées.
6. **Publication.** Il programme la publication dans Buffer sur les 3 réseaux, avec la légende et les hashtags.

## Installation (une seule fois)

1. **Buffer** (gratuit) : crée un compte sur buffer.com et connecte tes 3 comptes, TikTok, Instagram (compte Créateur) et YouTube.
2. **Clé API Buffer** : va sur https://publish.buffer.com/settings/api et crée une clé.
3. **GitHub** : dans ce dépôt, ouvre Settings > Secrets and variables > Actions > New repository secret. Nom : `BUFFER_API_KEY`. Valeur : la clé.
4. **Premier test** : onglet Actions > « Créer et publier une vidéo » > Run workflow, en laissant « Publier » décoché. La vidéo apparaît dans les fichiers du passage, rubrique Artifacts, sans rien publier.
5. **Premier vrai passage** : refais Run workflow en cochant « Publier ». Ensuite, tout se fait seul aux heures prévues.

## Régler les heures

Les heures se trouvent dans `.github/workflows/publish.yml` (lignes `cron`) et sont en UTC :

- `0 17 * * *` = 18 h à Paris en hiver (19 h en été) ;
- `0 0 * * *` = 1 h à Paris en hiver, soit 19 h à New York.

GitHub peut lancer un passage avec quelques minutes de retard.

## Modifier les textes

Les accroches, les questions, les hashtags et les mots secrets sont dans `bot/content.py`.

## Mettre en pause

Onglet Actions > « Créer et publier une vidéo » > menu « ⋯ » > Disable workflow.
