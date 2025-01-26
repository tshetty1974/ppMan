document.addEventListener("DOMContentLoaded", () => {
    const optionsDiv = document.getElementById("options");
    const storeFormDiv = document.getElementById("store-password-form");
    const retrieveFormDiv = document.getElementById("retrieve-password-form");
  
    const storePasswordBtn = document.getElementById("store-password-btn");
    const retrievePasswordBtn = document.getElementById("retrieve-password-btn");
    const backToOptionsBtn = document.getElementById("back-to-options");
    const backToOptionsRetrieveBtn = document.getElementById("back-to-options-retrieve");
    const storeForm = document.getElementById("store-form");
  
    // Show store password form
    storePasswordBtn.addEventListener("click", () => {
      optionsDiv.style.display = "none";
      storeFormDiv.style.display = "block";
    });
  
    // Show retrieve password form
    retrievePasswordBtn.addEventListener("click", () => {
      optionsDiv.style.display = "none";
      retrieveFormDiv.style.display = "block";
    });
  
    // Back to options from store password form
    backToOptionsBtn.addEventListener("click", () => {
      storeFormDiv.style.display = "none";
      optionsDiv.style.display = "block";
    });
  
    // Back to options from retrieve password form
    backToOptionsRetrieveBtn.addEventListener("click", () => {
      retrieveFormDiv.style.display = "none";
      optionsDiv.style.display = "block";
    });
  
    // Handle store password form submission
    storeForm.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const password = document.getElementById("password").value;
      const app = document.getElementById("app").value;
      const chain = "ethereum"; // Fixed as Ethereum for now
      const scheme = document.getElementById("scheme").value;
  
      if (scheme === "Scheme 1") {
        try {
          // Backend call for Scheme 1
          const response = await fetch("http://127.0.0.1:5000/store-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password, app, chain }),
          });
  
          if (!response.ok) {
            throw new Error("Failed to store password");
          }
  
          const data = await response.json();
          displayJson(data);
        } catch (error) {
          console.error("Error storing password:", error);
          alert("An error occurred while storing the password.");
        }
      } else {
        alert("Only Scheme 1 is supported currently.");
      }
    });
  
    // Display JSON data and provide a download option
    function displayJson(data) {
      alert("Password stored successfully! Generating JSON file...");
      console.log("Generated JSON:", data);
  
      // Create a downloadable JSON file
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "password_data.json";
      link.innerText = "Download JSON";
      document.body.appendChild(link);
  
      // Auto-click the download link
      link.click();
  
      // Cleanup
      setTimeout(() => {
        URL.revokeObjectURL(url);
        document.body.removeChild(link);
      }, 1000);
    }
  });
  