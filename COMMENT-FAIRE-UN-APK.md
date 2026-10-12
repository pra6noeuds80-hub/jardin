# Jardin lunaire sur téléphone : application et APK

Je n'ai pas pu fabriquer le fichier APK moi-même (il faut les outils Android et internet, absents ici). Le site est en revanche prêt pour devenir une application : le dossier contient maintenant tout ce qu'il faut.

## Fichiers à mettre en ligne
`index.html`, `poster.jpg`, `manifest.webmanifest`, `sw.js`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`

Ne mettez pas `jardin_lunaire.py` (version Windows) ni vos musiques si vous ne voulez pas les rendre publiques.

## Étape 1 : mettre le site en ligne (GitHub Pages)
1. Sur github.com, créez un dépôt public, par exemple `jardin-lunaire`.
2. « Add file », puis « Upload files » : glissez les 8 fichiers ci-dessus, puis « Commit changes ».
3. « Settings », puis « Pages » : choisissez la branche `main`, dossier `/ (root)`, puis « Save ».
4. Après 1 à 2 minutes, le site est à une adresse du type `https://pra6noeuds80-hub.github.io/jardin-lunaire/`.

## Étape 2A : installer sans APK (le plus simple)
- **Android (Chrome)** : ouvrez l'adresse, puis menu ⋮, « Installer l'application » (ou « Ajouter à l'écran d'accueil »). Le menu ☰ du site propose aussi le bouton « 📲 Installer l'application ».
- **iPhone (Safari)** : bouton Partager, puis « Sur l'écran d'accueil ».

L'application s'ouvre ensuite en plein écran, avec son icône, et fonctionne hors ligne après la première ouverture.

## Étape 2B : obtenir un vrai fichier APK
1. Allez sur **pwabuilder.com**, collez l'adresse de votre site, puis « Start ».
2. Choisissez « Package for stores », puis « Android ».
3. Indiquez un nom et un identifiant de paquet (par exemple `io.github.pra6noeuds80.jardinlunaire`), puis « Generate ».
4. Téléchargez le fichier zip : il contient l'**APK**, une clé de signature et ses informations. **Gardez la clé précieusement** : elle sert à publier les futures mises à jour.
5. Copiez l'APK sur le téléphone, ouvrez-le et autorisez l'installation depuis cette source.

Si une barre d'adresse apparaît en haut de l'application, c'est que le site n'est pas encore « vérifié » : PWABuilder fournit un fichier `assetlinks.json` à publier dans `/.well-known/` à la racine du domaine. Avec GitHub Pages, cela se fait dans un dépôt nommé exactement `pra6noeuds80-hub.github.io`, avec un fichier vide `.nojekyll`. Je peux préparer ce fichier avec vous.

Je n'ai pas pu tester ces écrans : leurs intitulés peuvent avoir changé.

## Ce qui change dans l'application
- **Musique du dossier** : la lecture automatique des mp4 et mp3 « à côté du fichier » ne marche pas sur téléphone. Utilisez « Choisir des mp4 / mp3 » dans le menu ☰. Les radios fonctionnent avec internet.
- **Hors ligne** : le calendrier, les listes, le plan, les fiches fonctionnent sans internet. La météo, les radios et l'identification Pl@ntNet demandent une connexion.
- **Identification Pl@ntNet** : en ligne, le navigateur peut bloquer la requête. Elle est fiable avec l'application Python sur ordinateur.
- **Vos données** (notes, plans, plantes) restent sur le téléphone, dans l'application. Pour les passer d'un appareil à l'autre : page « Astro-jardin », « Exporter mes données », puis « Importer ».
- **PDF et fichier Google Agenda** : ils se téléchargent normalement.
- **Mises à jour** : après avoir modifié les fichiers, changez `jardin-lunaire-v1` en `jardin-lunaire-v2` dans `sw.js` pour que les téléphones prennent la nouvelle version.
