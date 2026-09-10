const form = document.getElementById("house-form");
const areaInput = document.getElementById("area");
const bedroomsInput = document.getElementById("bedrooms");
const locationInput = document.getElementById("location");
const submitButton = form.querySelector("button[type='submit']");
const result = document.getElementById("result");

function showError(message) {
  result.className = "error";
  result.textContent = message;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const area = Number(areaInput.value);
  const bedrooms = Number(bedroomsInput.value);
  const location = locationInput.value;

  if (areaInput.value.trim() === "" || !Number.isFinite(area) || area < 0) {
    showError("Please enter a valid area.");
    return;
  }

  if (
    bedroomsInput.value.trim() === "" ||
    !Number.isInteger(bedrooms) ||
    bedrooms < 0
  ) {
    showError("Please enter a valid number of bedrooms.");
    return;
  }

  const query = new URLSearchParams({
    area: String(area),
    bedrooms: String(bedrooms),
    location,
  });

  result.className = "";
  result.textContent = "Calculating...";
  submitButton.disabled = true;

  try {
    // The relative URL uses the same origin that served this page.
    const response = await fetch(`/predict?${query.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `Request failed with status ${response.status}`);
    }

    const formattedPrice = Number(data.predicted_price).toLocaleString("vi-VN");
    result.className = "";
    result.textContent = `Predicted price: ${formattedPrice} VND`;
  } catch (error) {
    console.error(error);
    showError("Unable to get the prediction. Please check that the FastAPI server is running.");
  } finally {
    submitButton.disabled = false;
  }
});
