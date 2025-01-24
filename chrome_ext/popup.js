document.getElementById("encryption-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the form from reloading the popup

    // Get form data
    const password = document.getElementById("password").value;
    const chain = document.getElementById("chain").value;
    const encryptionScheme = document.getElementById("encryption-scheme").value;

    // Payload to send to the backend
    const payload = {
        password: password,
        chain: chain,
        schema: encryptionScheme,
    };

    try {
        // Send data to the backend
        const response = await fetch("http://localhost:5000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        // Display the backend response (or error)
        alert(result.message || "Error: Something went wrong");
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the backend. Check the console for details.");
    }
});
