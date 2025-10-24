const predictionText = document.getElementById("prediction-text");

// Function to send a frame to Flask
async function sendFrame(endpoint) {
    try {
        let res = await fetch(endpoint, { method: "POST" });
        let data = await res.json();

        predictionText.textContent = data.status === "success"
            ? `${data.name} ${data.action.replace("_", " ")} at ${data.time}`
            : data.message;
        
        if (data.status === "success") {
            updateLogs();  // Call if you implement this
        }
    } catch (err) {
        predictionText.textContent = `Error: ${err.message}`;
        console.error("Fetch error:", err);
    }
}
// Placeholder for updateLogs (expand if you want to fetch full CSV/logs via a new endpoint)
function updateLogs() {
    // Example: Fetch logs from a new '/logs' endpoint and append to a <div id="logs">
    // fetch('/logs').then(res => res.json()).then(logs => { ... });
    console.log("Logs updated (implement as needed)");
}

// Button events (these will now attach reliably)
document.addEventListener("DOMContentLoaded", () => {  // Use DOMContentLoaded for safety
    document.getElementById("timein-btn").addEventListener("click", () => sendFrame("/timein"));
    document.getElementById("timeout-btn").addEventListener("click", () => sendFrame("/timeout"));
    updateLogs();  // Initial call
});