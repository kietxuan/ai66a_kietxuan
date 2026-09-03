let bedroom = 3;
const taxRate = 0.08;

if (bedroom > 3) {
    console.log("This is a large house.");
} else {
    console.log("This is a small house.");
    console.warn("This is a small house.");
    console.error("This is a small house.");
}

for (let i = 0; i < 5; i++) {
    console.log(i);
}

let sample = { id: 1, name: "Sample",type: "Example" };

console.log(sample.name);
console.log(sample["name"]);

let arr = [1, 2, 3, 4, 5];
console.log(arr.length);

// Lab 1: Core JS Syntax on Array/Object Data
const predictionSamples = [
    { id: 1, name: "House Price", result: 0.91 },
    { id: 2, name: "Weather Forecast", result: 0.76 },
    { id: 3, name: "Customer Churn", result: 0.88 },
    { id: 4, name: "Movie Recommendation", result: 0.95 },
];

const highConfidenceSamples = [];
for (let i = 0; i < predictionSamples.length; i++) {
    if (predictionSamples[i].result >= 0.9) {
        highConfidenceSamples.push(predictionSamples[i]);
    }
}

function sumField(samples, field) {
    let total = 0;

    for (let i = 0; i < samples.length; i++) {
        total += samples[i][field];
    }

    return total;
}

function findLargestByField(samples, field) {
    if (samples.length === 0) {
        return null;
    }

    let largest = samples[0];

    for (let i = 1; i < samples.length; i++) {
        if (samples[i][field] > largest[field]) {
            largest = samples[i];
        }
    }

    return largest;
}

const sumResults = (samples) => sumField(samples, "result");

console.log("High-confidence samples:", highConfidenceSamples);
console.log("Total result:", sumField(predictionSamples, "result"));
console.log("Largest result:", findLargestByField(predictionSamples, "result"));
console.log("Total result (arrow function):", sumResults(predictionSamples));
