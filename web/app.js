/*
On déclare dans les constatntes les éléments constitutif de notre IHM web
La constante channels est un "dictionnaire" qui permet ce gérer les channel indépendemment de sorte à faire 4 configurations différentes à l'aide de la fonction createDefaultChannel.
La fonction createDefaultChannel donne un état par défaut aux channel de l'IHM ce qui permet d'initialiser notre élément de l'IHM 
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

// Configuration indépendante des quatre canaux  (version js du dictionnaire)
const channels = {
    1: createDefaultChannel(),
    2: createDefaultChannel(),
    3: createDefaultChannel(),
    4: createDefaultChannel()
};

// Configuartion de l'IHM par défaut
function createDefaultChannel() {
/*
Gestion  de l'état par défaut d'un canal
    Propriété retourné de l'objet canal : 
        Forme_du_signal : forme du signal
        frequence : valeur de la fréquence en Hz,
        amplitude: valeur de l'amplitude en V,
        decallage: Décallage en V,
        phase: phase en ° j'imagine que ça correspond à la phase d'un courant électrique ,
        enabled: état de la sortie activé ou désactivé
*/
    return {
        Forme_du_signal: "sine",
        frequence : 1000,
        amplitude : 5,
        decallage : 0,
        phase: 0,
        enabled: false
    };
}

// Afficher les paramètres d'un canal
function loadChannel() {
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
    const config = channels[Canaux.value];

    Forme_du_signal.value = config.Forme_du_signal;
    frequence.value = config.frequence;
    amplitude.value = config.amplitude;
    decallage.value = config.decallage;
    phase.value = config.phase;
    enabled.checked = config.enabled;

    status.textContent = "CH" + Canaux.value + " chargé.";
}

// Enregistrer les paramètres du canal sélectionné
async function loadChannel() {
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
    const selectedChannel = Canaux.value;

    try {
        const response = await fetch(
            `/channels/${selectedChannel}`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const config = await response.json();

        // Éviter d'afficher la réponse d'un ancien canal
        if (Canaux.value !== selectedChannel) {
            return;
        }

        // Mise à jour de l'IHM avec les valeurs Python
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


// Événements
Canaux.addEventListener("change", loadChannel);   // On utilise le design pattern Listener pour voir si l'utilisateur changes des paramètres du channel
button.addEventListener("click", saveChannel);   // On utilise le design pattern Listener pour voir si l'utilisateur click sur le bouton "Appliquer"

// Initialisation
loadChannel();
