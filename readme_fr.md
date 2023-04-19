## BaitGPT : Emails automatisés anti-escrocs avec GPT3.5

Avec les récents progrès des LLM et leur utilisation plus large par le grand public, beaucoup ont craint une augmentation de leur utilisation à des fins d'escroquerie [1](https://www.mcafee.com/blogs/internet-security/chatgpt-a-scammers-newest-tool/)[2](https://medium.com/geekculture/chatgpt-the-new-frontier-of-scamming-and-fraud-6884da6e2ff1). Bien qu'il s'agisse d'un risque, l'objectif de ce projet est de tester le contraire : utiliser les IA pour inonder les escrocs et les "catfishes" de réponses automatisées.

À ce stade, le projet vise les courriels frauduleux tels que les escroqueries à l'avance de frais, les escrocs ou d'autres usurpations d'identité.

Cette idée n'est pas nouvelle et a été tentée avec humour par James Veitch dans sa [série Youtube](https://www.youtube.com/playlist?list=PLjaZD_N3WCf-SzY9lQqsUNbubksD_KCPT).

Le but de ce projet est d'automatiser le processus dans l'espoir de lutter efficacement contre les escroqueries.

### Comment utiliser BaitGPT ?
#### En tant qu'utilisateur :

- Parcourez votre boîte aux lettres (et votre dossier spam) et identifiez les escroqueries qui correspondent au projet (potentiellement des escroqueries à l'avance, des hameçonnages, ou d'autres usurpations d'identité. Les courriels d'hameçonnage demandant de cliquer sur un lien ne sont pas inclus).
- Téléchargez les courriels identifiés sous forme de fichiers `.eml` (Tutoriel pour [Gmail et Outlook](https://www.codetwo.com/kb/export-email-to-file/#outlook-on-the-web)).
- Envoyez un courriel à [BaitGPT.reports@outlook.com](mailto:BaitGPT.reports@outlook.com?subject=[GitHub]%20Scams%20report)], en y joignant les fichiers `.eml`.
- Supprimez les fichiers `.eml` sur votre ordinateur.

#### En tant qu'expéditeur :
- clonez le dépôt
- obtenir une [api key](https://platform.openai.com/account/api-keys) d'OpenAI la stocker dans `GPTkey.json` comme `{"api_key" : "Votre_clé"}`.
- Créez plusieurs adresses email, et obtenez la connexion associée dans `credential_head.json` et `credential.json` comme `{"users" : [{"email" : "example@outlook.com", "password" : "safe_password", "imap_server" : "outlook.office365.com", "smtp_server" : "smtp-mail.outlook.com", "smtp_port" : 587}]}`. Le chef est l'adresse électronique qui recueille les courriels, les autres sont ceux qui envoient les réponses et maintiennent la discussion.
- Pour des raisons de sécurité (téléchargement de pièces jointes et envoi de faux courriels à des escrocs), utilisez un environnement distant pour l'exécution.

### Comment cela fonctionne-t-il ?
- Tout d'abord, les courriels frauduleux sont extraits de la boîte aux lettres principale.
- Ensuite, pour chaque courriel, le corps du texte est extrait, ainsi que les informations d'en-tête nécessaires pour la réponse.
- GPT3.5 est appelé une première fois pour évaluer s'il s'agit d'un courriel frauduleux. En cas de réponse négative ou de doute, l'e-mail est ignoré.
- Un courriel de réponse est rédigé avec GPT3.5, en suivant une invite personnalisée qui peut être adaptée.
- L'une des boîtes aux lettres de "sortie" envoie l'e-mail de réponse en essayant de respecter les conventions RFC.
- À chacune de ces étapes, une vérification humaine peut être ajoutée (elle est actuellement active avant l'envoi).
- Indépendamment, une boucle similaire s'exécute sur la boîte aux lettres "output" afin de poursuivre la discussion au cas où l'appât fonctionnerait.

### FAQ
- Que faisons-nous de vos données ?
Temporairement, les courriels peuvent être stockés temporairement à des fins de débogage et d'évaluation de l'efficacité.
Vos données (adresse électronique et informations personnelles contenues dans les courriels) ne seront pas exploitées ni partagées avec des tiers.
Les courriels sont supprimés après avoir reçu une réponse et ne contiennent pas votre adresse électronique. Seul le corps du document est envoyé, qui peut contenir des informations personnelles telles que des noms ou des informations d'identification divulguées.
- Combien cela coûte-t-il ?
Pour l'utilisateur : rien. Pour l'expéditeur : environ 0,003 $ par courriel. Pour les escrocs : un temps précieux non consacré à l'escroquerie de personnes réelles.

### Développement ultérieur :
Parmi toutes les escroqueries, celle dont il est question ici ne représente qu'une part mineure, à côté du phishing, des pièces jointes malveillantes, etc.

L'une des principales limites est le support : les courriels semblent dépréciés par rapport aux messageries privées sur les réseaux sociaux tels qu'Instagram ou Facebook. La mise en œuvre sur ces médias ouvrirait des possibilités mais représenterait une étape importante en termes de complexité.
L'objectif premier de ce projet est d'évaluer l'efficacité d'une telle méthode. Toute idée d'amélioration est la bienvenue.
