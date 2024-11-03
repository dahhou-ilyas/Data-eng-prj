document.addEventListener('DOMContentLoaded', () => {
    const products = document.querySelectorAll('.product-card');
    const purchaseCounts = {}; // Objet pour stocker les comptes d'achats
    let sessionStart = new Date();

    // Fonction pour obtenir l'horodatage actuel au format ISO 8601
    function getCurrentTimestamp() {
        return new Date().toISOString(); // Format ISO 8601
    }

    // Fonction pour obtenir des informations sur le navigateur et le système
    function getBrowserInfo() {
        const userAgent = navigator.userAgent;
        let browserName, browserVersion, osName, osVersion;

        // Détection basique du navigateur
        if (userAgent.indexOf("Chrome") > -1) {
            browserName = "Chrome";
            browserVersion = userAgent.split("Chrome/")[1].split(" ")[0];
        } else if (userAgent.indexOf("Firefox") > -1) {
            browserName = "Firefox";
            browserVersion = userAgent.split("Firefox/")[1];
        } else if (userAgent.indexOf("Safari") > -1) {
            browserName = "Safari";
            browserVersion = userAgent.split("Version/")[1].split(" ")[0];
        } else if (userAgent.indexOf("MSIE") > -1 || userAgent.indexOf("Trident") > -1) {
            browserName = "Internet Explorer";
            browserVersion = userAgent.split("MSIE ")[1] || userAgent.split("rv:")[1];
        } else {
            browserName = "Unknown";
            browserVersion = "Unknown";
        }

        // Détection du système d'exploitation
        if (userAgent.indexOf("Win") > -1) {
            osName = "Windows";
            osVersion = userAgent.split("Windows NT ")[1].split(";")[0];
        } else if (userAgent.indexOf("Mac") > -1) {
            osName = "Mac OS";
            osVersion = userAgent.split("Mac OS X ")[1].split(")")[0];
        } else if (userAgent.indexOf("Linux") > -1) {
            osName = "Linux";
            osVersion = "Unknown";
        } else {
            osName = "Unknown";
            osVersion = "Unknown";
        }

        return { browserName, browserVersion, osName, osVersion };
    }

    // Fonction pour créer un événement standardisé
    function createEvent(action, additionalInfo = {}) {
        const sessionDuration = Math.floor((new Date() - sessionStart) / 1000); // Durée de la session en secondes
        const viewportWidth = window.innerWidth; // Largeur de la fenêtre
        const viewportHeight = window.innerHeight; // Hauteur de la fenêtre
        const screenWidth = window.screen.width; // Largeur de l'écran
        const screenHeight = window.screen.height; // Hauteur de l'écran
        const isOnline = navigator.onLine; // État de la connexion
        const language = navigator.language || navigator.userLanguage; // Langue du navigateur
        const { browserName, browserVersion, osName, osVersion } = getBrowserInfo(); // Informations sur le navigateur et l'OS

        return {
            date: getCurrentTimestamp(),
            action,
            sessionDuration,
            viewportWidth,
            viewportHeight,
            screenWidth,
            screenHeight,
            isOnline,
            language,
            browserName,
            browserVersion,
            osName,
            osVersion,
            ...additionalInfo
        };
    }

    products.forEach(product => {
        product.addEventListener('click', () => {
            const productId = product.getAttribute('data-info-id');
            const productName = product.getAttribute('data-info-name');

            // Initialiser le compte pour ce produit si pas encore présent
            if (!purchaseCounts[productId]) {
                purchaseCounts[productId] = { name: productName, count: 0 };
            }

            // Incrémenter le compte d'achats
            purchaseCounts[productId].count++;

            const event = createEvent(`purchase`, {
                productId,
                productName,
                count: purchaseCounts[productId].count // Inclure le compte d'achats
            });

            // Afficher les informations dans la console, séparées par des points-virgules
            console.log(`Date: ${event.date}; Action: ${event.action}; Product ID: ${event.productId}; Product Name: ${event.productName}; Count: ${event.count}; Session Duration: ${event.sessionDuration}s; Viewport: ${event.viewportWidth}x${event.viewportHeight}; Screen: ${event.screenWidth}x${event.screenHeight}; Online: ${event.isOnline}; Language: ${event.language}; Browser: ${event.browserName} ${event.browserVersion}; OS: ${event.osName} ${event.osVersion}`);
            console.log('Current Purchase Counts:', purchaseCounts); // Affiche le nombre total d'achats
        });
    });

    // Suivi du défilement
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const event = createEvent('scroll', { scrollPosition });
        
        // Afficher les informations dans la console, séparées par des points-virgules
        console.log(`Date: ${event.date}; Action: ${event.action}; Scroll Position: ${event.scrollPosition}; Session Duration: ${event.sessionDuration}s; Viewport: ${event.viewportWidth}x${event.viewportHeight}; Screen: ${event.screenWidth}x${event.screenHeight}; Online: ${event.isOnline}; Language: ${event.language}; Browser: ${event.browserName} ${event.browserVersion}; OS: ${event.osName} ${event.osVersion}`);
    });

    window.addEventListener('beforeunload', () => {
        const event = createEvent('page_exit');
        console.log(`Date: ${event.date}; Action: ${event.action}; Session Duration: ${event.sessionDuration}s; Viewport: ${event.viewportWidth}x${event.viewportHeight}; Screen: ${event.screenWidth}x${event.screenHeight}; Online: ${event.isOnline}; Language: ${event.language}; Browser: ${event.browserName} ${event.browserVersion}; OS: ${event.osName} ${event.osVersion}`);
    });

    const pageVisitEvent = createEvent('page_visit', {
        pageTitle: document.title
    });
    console.log(`Date: ${pageVisitEvent.date}; Action: ${pageVisitEvent.action}; Page Title: ${pageVisitEvent.pageTitle}; Session Duration: ${pageVisitEvent.sessionDuration}s; Viewport: ${pageVisitEvent.viewportWidth}x${pageVisitEvent.viewportHeight}; Screen: ${pageVisitEvent.screenWidth}x${pageVisitEvent.screenHeight}; Online: ${pageVisitEvent.isOnline}; Language: ${pageVisitEvent.language}; Browser: ${pageVisitEvent.browserName} ${pageVisitEvent.browserVersion}; OS: ${pageVisitEvent.osName} ${pageVisitEvent.osVersion}`);
});

