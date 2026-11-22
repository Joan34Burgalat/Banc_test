/*
On déclare dans les constatntes les éléments constitutif de notre IHM web
La fonction loadChannel récupère ou stock les paramètres sélectionnés par l'utilisateur
La fonction saveChannel sauvegarde les paramètre du channel choisit par l'utilisateur de manière à ce que le changement de channel ne change pas les paramètres
*/

// On déclare les références vers les éléments HTML de l'IHM grâce à l'id (par exemple frequence) 
const Canaux = document.getElementById("Canaux");          // On gère la combobox des channel du générateur
const Forme_du_signal = document.getElementById("Forme_du_signal");        // On gère la combobox des signaux du générateur
const frequence = document.getElementById("frequence");      // On gère la valeur des fréquences du générateur
const amplitude = document.getElementById("amplitude");      // On gère la valeur des amplitudes du générateur

// Ajout des Offsets Phase et gestion de l'activation de la sortie
const decallage = document.getElementById("decallage");            // On gère la valeur de l'offset en V du générateur
const phase = document.getElementById("phase");              // On gère la valeur de la phase eb ° du générateur
const enabled = document.getElementById("enabled");          // On gère l'activation de la sortie

// Déclaration des éléments bouton "Appliquer" et affichage du l'état du channel (chargé ou pas)
const button = document.getElementById("apply");
const status = document.getElementById("status");

// Afficher les paramètres d'un canal
async function loadChannel() {
/*
Permet de lire la configuration mémorisé de l'état d'un channel choisit par l'utilisateur et de l'afficher 
    Propriété retourné de l'objet channel : 
        const config : correspond au channel choisit dans l'IHM c'est l'élément de la liste channels
        frequence.value : stock la valeur de la fréquence choisit par l'utilisateur ,
        amplitude.value : stock la valeur de l'amplitude choisit par l'utilisateur ,
        decallage.value : stock la valeur de l'offset choisit par l'utilisateur ,
        phase.value : stock la valeur de la phase choisit par l'utilisateur ,
        enabled.checked : stock l'état de la sortie choisit par l'utilisateur  
*/
    const selectedChannel = Canaux.value;

    try {
        const response = await fetch(
            `/channels/${selectedChannel}`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const config = await response.json();

        // Vérifier que l'utilisateur n'a pas changé de canal
        if (Canaux.value !== selectedChannel) {
            return;
        }

        // Afficher les valeurs provenant de Python
        Forme_du_signal.value = config.waveform;
        frequence.value = config.frequency;
        amplitude.value = config.amplitude;
        decallage.value = config.offset;
        phase.value = config.phase;
        enabled.checked = config.enabled;

        status.textContent =
            `CH${selectedChannel} chargé depuis Python`;

    } catch (error) {
        status.textContent =
            `Erreur de chargement : ${error.message}`;
    }
}


// Enregistrer les paramètres du canal sélectionné
async function saveChannel() {
/*
Permet de sauvegarder l'état d'un channel choisit par l'utilisateur
    Arg : 
        const config : correspond au channel choisit dans l'IHM c'est l'élément de la liste channels
        frequence.value : stock la valeur de la fréquence choisit par l'utilisateur ,
        amplitude.value : stock la valeur de l'amplitude choisit par l'utilisateur ,
        decallage.value : stock la valeur de l'offset choisit par l'utilisateur ,
        phase.value : stock la valeur de la phase choisit par l'utilisateur ,
        enabled.checked : stock l'état de la sortie choisit par l'utilisateur  
*/

    // Mémoriser le canal sélectionné
    const selectedChannel = Canaux.value;

    // Récupérer les paramètres de l'IHM
    const config = {
        waveform: Forme_du_signal.value,
        frequency: Number(frequence.value),
        amplitude: Number(amplitude.value),
        offset: Number(decallage.value),
        phase: Number(phase.value),
        enabled: enabled.checked
    };

    // Vérification des paramètres
    if (
        !Number.isFinite(config.frequency) ||
        !Number.isFinite(config.amplitude) ||
        !Number.isFinite(config.offset) ||
        !Number.isFinite(config.phase) ||
        config.frequency < 0 ||
        config.amplitude < 0 ||
        (config.waveform !== "dc" && config.frequency === 0)
    ) {
        status.textContent = "Configuration invalide.";
        return;
    }

    try {
        // Envoyer les paramètres à FastAPI
        const response = await fetch(
            `/channels/${selectedChannel}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(config)
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();

        status.textContent =
            `CH${selectedChannel} enregistré sur le serveur`;

        console.log("Réponse API :", result);

    } catch (error) {
        status.textContent =
            `Erreur de communication : ${error.message}`;
    }
}



// Événements
Canaux.addEventListener("change", loadChannel);   // On utilise le design pattern Listener pour voir si l'utilisateur changes des paramètres du channel
button.addEventListener("click", saveChannel);   // On utilise le design pattern Listener pour voir si l'utilisateur click sur le bouton "Appliquer"

// Initialisation
loadChannel();
