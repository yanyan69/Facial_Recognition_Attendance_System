const predictionText = document.getElementById("prediction-text");

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing webcam:", err);
    });

// Function to send a frame to Flask
async function sendFrame(endpoint) {
    let res = await fetch(endpoint, { method: "POST" });
    let data = await res.json();

    predictionText.textContent = data.status === "success"
        ? `${data.name} ${data.action.replace("_", " ")} at ${data.time}`
        : data.message;
    
    if (data.status === "success") {
        updateLogs();
    }
}

// Call on load
window.addEventListener("load", updateLogs);
// Button events
document.getElementById("timein-btn").addEventListener("click", () => sendFrame("/timein"));
document.getElementById("timeout-btn").addEventListener("click", () => sendFrame("/timeout"));