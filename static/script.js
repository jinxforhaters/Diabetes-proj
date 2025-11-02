console.log("🚀 Frontend loaded successfully!");

// Reference to form and result container
const form = document.getElementById("prediction-form");
const resultBox = document.getElementById("result-container");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Collect and convert form data
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  for (const key in data) data[key] = parseFloat(data[key]);

  console.log("Form Data:", data);

  // Send POST request to FastAPI
  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Server Error");

    const predictionData = await response.json();
    console.log("Prediction:", predictionData);

    const label = predictionData.prediction_label;
    const nonDiabetic = (predictionData.confidence_scores.Non_Diabetic * 100).toFixed(2);
    const diabetic = (predictionData.confidence_scores.Diabetic * 100).toFixed(2);

    // Display Result
    resultBox.classList.remove("hidden", "success", "danger");
    resultBox.classList.add(label === "Diabetic" ? "danger" : "success");

    resultBox.innerHTML = `
      <h2>${label === "Diabetic" ? "⚠️ Diabetic Risk Detected" : "✅ Non-Diabetic"}</h2>
      <p>Confidence Scores:</p>
      <p>Non-Diabetic: ${nonDiabetic}%<br>Diabetic: ${diabetic}%</p>
    `;
  } catch (err) {
    console.error("Error:", err);
    resultBox.classList.remove("hidden", "success", "danger");
    resultBox.classList.add("danger");
    resultBox.innerHTML = `<p>❌ Error connecting to the prediction API.</p>`;
  }
});
