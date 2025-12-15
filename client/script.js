 function getGreeting() {
      const lang = navigator.language || navigator.userLanguage;
    console.log('lang',lang);
    
      if (lang.startsWith("fr")) return "Bonjour 👋";
      if (lang.startsWith("es")) return "Hola 👋";
      if (lang.startsWith("de")) return "Hallo 👋";
      return "Hello 👋";
    }
    document.getElementById("greeting").innerText = getGreeting();
    document.getElementById("info").innerText = `
Langue: ${navigator.language}
User-Agent: ${navigator.userAgent}
Referer: ${document.referrer || "Aucun"}
    `;

