const webcam = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const predictionText = document.getElementById('prediction-text');

// Start webcam stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        webcam.srcObject = stream;

        // Once webcam is ready, start detection automatically
        webcam.onloadedmetadata = () => {
            predictionText.textContent = "Detecting...";

            setInterval(async () => {
                ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
                let imageData = canvas.toDataURL("image/jpeg");

                // Mock AI prediction
                predictionText.textContent = "AI says: Face detected";

                // Example Roboflow API call (uncomment when ready):
                
                let response = await fetch("face-recognize-gqgba/4", {
                    method: "POST",
                    body: imageData.split(",")[1], // send base64 without prefix
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                });
                let result = await response.json();
                predictionText.textContent = "AI says: " + JSON.stringify(result);
                
            }, 2000); // capture every 2 seconds
        };
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
        predictionText.textContent = "Webcam access failed.";
    });
