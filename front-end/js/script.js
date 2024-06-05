function imc() {
    const nom = document.getElementById("nom").value;
    const hauteur = document.getElementById("hauteur").value;
    const poids = document.getElementById("poids").value;
    const resultat = document.getElementById("resultat");
  
    if (nom !== "" && hauteur !== "" && poids !== "") {
      const ValeurIMC = (poids / (hauteur * hauteur)).toFixed(1);
  
      let classification = "";
  
      if (ValeurIMC < 18.5) {
        classification = "Sous poids";
      } else if (ValeurIMC < 25) {
        classification = "à votre poids idéal, félicitations !!!";
      } else if (ValeurIMC < 30) {
        classification = "légèrement au-dessus du poids idéal.";
      } else if (ValeurIMC < 35) {
        classification = "avec obésité de grade I.";
      } else if (ValeurIMC < 40) {
        classification = "avec obésité de grade II (sévère).";
      } else {
        classification = "avec l'obésité III (morbide), soyez prudent !!!";
      }
  
      resultat.textContent = `${nom}, votre IMC est ${ValeurIMC} et vous êtes ${classification}`;
    } else {
      alert("Remplissez tous les champs!!");
    }
  }
  
  document.getElementById("calculer").addEventListener("click", imc);
  
  //UX in the field of height
  document.getElementById("hauteur").addEventListener("input", function (event) {
    let hauteur = event.target.value;
  
    hauteur = hauteur.replace(/[^\d]/g, "");
    if (!hauteur.includes(".") && hauteur.length > 1) {
      hauteur = hauteur.slice(0, 1) + "." + hauteur.slice(1);
    }
    event.target.value = hauteur;
  });
  
  //UX in the field of weight
  document.getElementById("poids").addEventListener("input", function (event) {
    let poids = event.target.value;
  
    poids = poids.replace(",", ".");
  
    poids = poids.replace(/[^\d.]/g, "");
  
    if (poids.indexOf(".") !== -1) {
      const parts = poids.split(".");
      poids = parts[0].slice(0, 3) + "." + parts.slice(1).join("").slice(0, 2);
    } else {
      poids = poids.slice(0, 3);
    }
  
    event.target.value = poids;
  });
  
  document.getElementById('btn').addEventListener('click', () => {
    window.location.href = '/'; // Redirect to the homepage
  });
  
  document.getElementById('action-button').addEventListener('click', () => {
    window.location.href = '/TesterDiabet'; // Redirect to the homepage
  });