# TF1 Downloader

## Téléchargeur de replays TF1


<h1 align="center">
<a href="https://github.com/spel987/TF1-Downloader"><img src="https://i.imgur.com/YIkuCQc.png"></a>
</h1>

<h1 align="center">
<a href="https://github.com/spel987/TF1-Downloader/archive/refs/heads/main.zip"><img src="https://i.imgur.com/mqFcmoc.png" width="250"></a>
</h1>

## 🚀 Caractéristiques

- Télécharger les vidéos replays présentent sur le site [TF1](https://tf1.fr)
- Choisir la qualité voulue pour la vidéo replay téléchargée

TF1 Downloader est un script de téléchargement de vidéos de replays présentent sur le site [TF1](https://tf1.fr). 

## ⬇️ Installation

- Installer la dernière version de [Python](https://www.python.org/downloads/) : https://www.python.org/downloads/

- Installer la dernière version de [Firefox]("https://www.mozilla.org/en-US/firefox/new/") : https://www.mozilla.org/en-US/firefox/new/

- Installer [cette dépendance](https://learn.microsoft.com/fr-FR/cpp/windows/latest-supported-vc-redist?view=msvc-170), utilisée par le module Selenium : https://learn.microsoft.com/fr-FR/cpp/windows/latest-supported-vc-redist?view=msvc-170

<img src="https://i.imgur.com/IIUia2Y.png">

- Installer les paquets nécessaires à l'exécution du script.

```
pip install -r requirements.txt
```

- Lancer  `TF1_Downloader.py`.

## 🧪 Utilisation

### Télécharger à partir des serveurs de TF1 :

Il suffit de lancer le script Python, entrer un lien de replay TF1. Ensuite, le script va automatiquement l'ouvrir, il se connectera ensuite à un compte TF1 fait pour l'occasion et commencera le traitement. Ensuite, vous aurez le choix de la qualité désirée pour votre vidéo replay. Le script commencera automatiquement le téléchargement de tous les segments vidéo et audio, puis les assemblera avec `ffmpeg`. Pour plus de détail sur le fonctionnement du script, veuillez vous rendre à la rubrique <a href="#%EF%B8%8F-fonctionnement">Fonctionnement</a>.

TF1 Downloader se chargera du téléchargement et de l'assemblage :

- Des tous les segments vidéo
- Des tous les segments audio

Demonstration vidéo :

https://user-images.githubusercontent.com/89778476/226112718-d0f87680-9a9f-4d54-a7a6-98abbf4f2d05.mp4

<br>

**⚠️ ATTENTION : TF1 Downloader est limité au téléchargement de vidéos non protégées par DRM. Pour plus d'informations, veuillez vous rendre dans la rubrique <a href="#-limitations-drm">"Limitations DRM"</a>**.

## ⚙️ Fonctionnement

### Comment TF1 Downloader fonctionne-t-il ?

Lorsque nous lançons une vidéo depuis le site de TF1, le site fait une requête pour récupérer un fichier `.mpd` contenant toutes les informations nécessaires à la lecture de la vidéo replay. Voici cette requête visible via l'onglet "Réseau" de Firefox sur une vidéo replay aléatoire de TF1 :

<img src="https://i.imgur.com/sTCjRvj.png">

L'URL de cette requête est le suivant : 

https://vod-das.cdn-0.diff.tf1.fr/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaXAiOiI4OC4xNDAuNjIuODAiLCJjbWNkIjoiIiwiZXhwIjoxNjc5MTU3NzMyLCJnaWQiOiI3NTRjOTg0YmNjYzU0NzhhYjE4OTlhNjZlOTBhMmQ0MyIsImlhdCI6MTY3OTE0MzMzMiwiaXNzIjoiZGVsaXZlcnkiLCJtYXhiIjoyNzAwMDAwLCJzdGVtIjoiLzIvVVNQLTB4MC82Ni8wMC8xMzk2NjYwMC9zc20vNzQ5NmNhM2M3YTAyZGQzYWYzN2E1NTUzNTA0OTU0MmExYTBiOWQ0MzVmYTU2MGFhMDQ0Y2RlZTU1ZDRiN2VhMy5pc20vMTM5NjY2MDAubXBkIiwic3ViIjoiNzU0Yzk4NGJjY2M1NDc4YWIxODk5YTY2ZTkwYTJkNDMifQ.w2YTJ6yv0lIkCRGHfIQQ903eLsWOGnHNXsLjKIwiQwc/2/USP-0x0/66/00/13966600/ssm/7496ca3c7a02dd3af37a55535049542a1a0b9d435fa560aa044cdee55d4b7ea3.ism/13966600.mpd

La base de l'URL va être utile pour la suite, car c'est sur ce chemin que sont stockés tous les segments audios et vidéos. Pour l'obtenir, il faut simplement retirer le nom du fichier `.mpd` ainsi que son extension. Soit : `13966600.mpd`

Le fichier MPD (Media Presentation Description) est un fichier XML qui décrit les métadonnées d'une présentation multimédia utilisée pour la diffusion en continu (streaming) de contenus tels que des vidéos, de l'audio ou des images sur Internet. Le fichier MPD contient des informations telles que l'ordre de lecture des segments multimédias, leur durée, leur format et leur emplacement. Il permet également de décrire les caractéristiques techniques de la présentation, telles que la qualité de la vidéo, la résolution, la fréquence d'images, les codecs utilisés, etc.

On peut donc télécharger ce fichier MPD pour voir comment il est composé et l'analyser pour en retirer les informations nécessaires au téléchargement.

<img src="https://i.imgur.com/HARQ5B0.png" width=300> 

Sur cette capture d'écran, nous retrouvons toutes les informations concernant les noms de fichiers vidéos et leur qualité. Ceci va être utile pour le choix de qualité par la suite. Avec Python et la librairie `xml` il est assez simple d'analyser et d'extraire ces informations.

Nous avons besoin d'une information supplémentaire, le nom global de notre vidéo replay.

<img src="https://i.imgur.com/SFUYYJJ.png">

Dans l'attribut `media` de la balise `SegmentTemplate` se trouve cette information ainsi que la construction du nom du fichier.

```
7496ca3c7a02dd3af37a55535049542a1a0b9d435fa560aa044cdee55d4b7ea3-$RepresentationID$-$Number$.m4s
```

Nous retrouvons en premier l'ID du média, ensuite séparé d'un `-` le nom de la vidéo en fonction de la qualité, extraite depuis les balises `Representation` au-dessus. Puis, encore séparé par un `-` le chiffre du segment. En effet, la vidéo est découpée en de multiples segments vidéos, le script les téléchargent tous en essayant à chaque fois avec un numéro de segment plus élevé que le précédent. Et enfin le format vidéo, soit `.m4s`. Les fichiers `m4s` font partie d'un format de streaming appelé MPEG-DASH (Dynamic Adaptive Streaming over HTTP)

Donc voici un exemple de téléchargement du premier segment, en vidéo et qualité 720p :

https://vod-das.cdn-0.diff.tf1.fr/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaXAiOiI4OC4xNDAuNjIuODAiLCJjbWNkIjoiIiwiZXhwIjoxNjc5MTU3NzMyLCJnaWQiOiI3NTRjOTg0YmNjYzU0NzhhYjE4OTlhNjZlOTBhMmQ0MyIsImlhdCI6MTY3OTE0MzMzMiwiaXNzIjoiZGVsaXZlcnkiLCJtYXhiIjoyNzAwMDAwLCJzdGVtIjoiLzIvVVNQLTB4MC82Ni8wMC8xMzk2NjYwMC9zc20vNzQ5NmNhM2M3YTAyZGQzYWYzN2E1NTUzNTA0OTU0MmExYTBiOWQ0MzVmYTU2MGFhMDQ0Y2RlZTU1ZDRiN2VhMy5pc20vMTM5NjY2MDAubXBkIiwic3ViIjoiNzU0Yzk4NGJjY2M1NDc4YWIxODk5YTY2ZTkwYTJkNDMifQ.w2YTJ6yv0lIkCRGHfIQQ903eLsWOGnHNXsLjKIwiQwc/2/USP-0x0/66/00/13966600/ssm/7496ca3c7a02dd3af37a55535049542a1a0b9d435fa560aa044cdee55d4b7ea3.ism/7496ca3c7a02dd3af37a55535049542a1a0b9d435fa560aa044cdee55d4b7ea3-video=2501449-1.m4s

Pour le téléchargement des pistes audios, c'est exactement le même principe avec le nom du fichier audio correspondant trouvé dans le fichier `.mpd`.

<img src="https://i.imgur.com/klWk2pA.png" width=300>

Pour compiler tous les segments audio et vidéo, il faut un fichier d'initialisation. Pour le télécharger, il faut simplement retirer le chiffre du segment. Pour que ça soit compréhensible, je vais appeler le fichier audio d'initialisation `a_0.m4s` et le fichier vidéo d'initialisation `v_0.m4s`. Pour la suite, chaque segment téléchargé a un nom comprenant le chiffre précédent du segment plus un. Ainsi j'ai `v_0.m4s`, `v_1.m4s`, `v_2.m4s`, `v_3.m4s`... 

Enfin, je compile tous les segments audio et vidéo avec [FFMPEG](https://ffmpeg.org/). Voici la commande utilisée : 

```
ffmpeg -i "concat:v_0.m4s|v_1.m4s|v_2.m4s|v_3.m4s|..." -i "concat:a_0.m4s|a_1.m4s|a_2.m4s|a_3.m4s|..." -c copy output.mp4
```

Nous nous retrouvons donc avec `output.mp4` comprenant les pistes audio et vidéo synchronisées et lisibles.

## 🔒 Limitations DRM

Certaines vidéos présente sur le site de TF1 sont protégées par DRM. 

La protection DRM (Digital Rights Management) des médias est un système de sécurité qui empêche la copie et la redistribution non autorisées de contenu numérique, tels que des films, de la musique, des livres électroniques, etc. Les DRM fonctionnent en chiffrant le contenu numérique afin qu'il ne puisse être lu que sur des appareils ou des logiciels spécifiques avec des clés de déchiffrement appropriées. Cela permet aux fournisseurs de contenu de contrôler l'accès à leur contenu et de limiter la redistribution illégale, mais cela peut également restreindre l'utilisation légitime du contenu par les utilisateurs. 

Pour obtenir la clé de déchiffrement, le lecteur TF1 fait une requête au serveur de licences de TF1 et la clé se trouve dans la réponse. Malheureusement, cette réponse est chiffrée et je ne possède pas les capacités nécessaires au déchiffrement de ces données. Pour plus d'informations, je vous invite à lire mon topic sur NsaneForums ayant obtenu des réponses intéressantes d'un utilisateur, voici le [lien](https://nsaneforums.com/topic/438184-i-cant-find-the-drm-key-from-a-license-server-response/). 

Certains contenus (souvent des séries étrangères, comme Grey's Anatomy etc) sont donc protégés par DRM. Ils peuvent être téléchargés et assemblés, mais vous ne pourrez pas les lire.

## 🔧 Credits

- Spel<br>
    Discord : `spel987`<br>
    Email : `spel@usurp.in`<br>
    GitHub : https://github.com/spel987


## ❓ Suggestions

Si vous avez des questions ou des suggestions, veuillez ouvrir une [issue](https://github.com/spel987/TF1-Downloader/issues). 

## 💸Donations

Si vous aimez ce projet ou souhaitez le soutenir, vous pouvez faire des dons.

Ethereum : 
```
0x79024c8eA7Bfdef93cBa538eB6288a9bB40eFC97
```
Bitcoin :
```
bc1qua3qmrhlv3e53ydynwvfc2wq8q7wteqxwlewa4
```
