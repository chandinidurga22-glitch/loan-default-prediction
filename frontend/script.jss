function predict() {

const result = document.getElementById("result");
const sound = document.getElementById("clickSound");

sound.play();

// Loader
result.innerHTML = '<div class="loader"></div>';

let age = document.getElementById("age").value;
let income = document.getElementById("income").value;
let loan = document.getElementById("loan").value;
let score = document.getElementById("score").value;

// Dummy logic (replace with API later)
setTimeout(() => {

if(score > 650 && income > loan) {
result.innerHTML = "✔ Low Risk (Safe)";
result.className = "safe";
}
else {
result.innerHTML = "❌ High Risk (Risky)";
result.className = "risky";
}

},1500);

}