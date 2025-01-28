document.addEventListener("DOMContentLoaded", () => {
  const optionsDiv = document.getElementById("options");
  const storeFormDiv = document.getElementById("store-password-form");
  const retrieveFormDiv = document.getElementById("retrieve-password-form");

  const storePasswordBtn = document.getElementById("store-password-btn");
  const retrievePasswordBtn = document.getElementById("retrieve-password-btn");
  const backToOptionsBtn = document.getElementById("back-to-options");
  const backToOptionsRetrieveBtn = document.getElementById("back-to-options-retrieve");

  const storeForm = document.getElementById("store-form");
  const retrieveForm = document.getElementById("retrieve-form");

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
        // Backend call for storing password
        const response = await fetch("http://127.0.0.1:5000/store-password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ password, app, chain }),
        });

        if (!response.ok) throw new Error("Failed to store password.");

        const data = await response.json();
        generateAndDownloadJson(data);
      } catch (error) {
        console.error("Error storing password:", error);
        alert("An error occurred while storing the password.");
      }
    } else {
      alert("Only Scheme 1 is supported currently.");
    }
  });

  // Handle retrieve password form submission
  retrieveForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const txHash = document.getElementById("tx-hash").value;

    try {
      const response = await fetch("http://127.0.0.1:5000/retrieve-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transaction_hash: txHash }),
      });

      if (!response.ok) throw new Error("Failed to retrieve password.");

      const data = await response.json();
      
      if (data.error) {
        alert("Error retrieving password: " + data.error);
        return;
      }

      alert(`Retrieved Password: ${data.password}`);
    } catch (error) {
      console.error("Error retrieving password:", error);
      alert("An error occurred while retrieving the password.");
    }
  });

  // Generate and download JSON file
  function generateAndDownloadJson(data) {
    try {
      console.log("Generated JSON:", data);

      // Create JSON file
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      // Create a download link
      const link = document.createElement("a");
      link.href = url;
      link.download = "password_data.json";
      document.body.appendChild(link);

      // Simulate click to start download
      link.click();

      // Cleanup
      link.remove();
      URL.revokeObjectURL(url);

      alert("JSON file generated and downloaded successfully!");
    } catch (error) {
      console.error("Error generating JSON:", error);
      alert("An error occurred while generating the JSON file.");
    }
  }
});
