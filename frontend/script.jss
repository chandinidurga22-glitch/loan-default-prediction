async function predict() {

const result = document.getElementById("result");

result.innerHTML = '<div class="loader"></div>';

let age = document.getElementById("age").value;
let income = document.getElementById("income").value;
let loan = document.getElementById("loan").value;
let score = document.getElementById("score").value;

if(!age || !income || !loan || !score){
    result.innerHTML="Please enter all values";
    return;
}

age = Number(age);
income = Number(income);
loan = Number(loan);
score = Number(score);

// ✅ LOGIC

if(score >= 700){
    result.innerHTML = "✔ Low Risk - Loan approval chances high";
    result.className = "safe";
    return;
}

if(score < 600){
    result.innerHTML = "❌ High Risk - Loan may be rejected (Low Credit Score)";
    result.className = "risky";

    const alarm = document.getElementById("alarm");
    alarm.currentTime = 0;
    alarm.play().catch(() => {});

    return;
}

// API for medium scores
let data = {
    age: age,
    income: income,
    loanamount: loan,
    creditscore: score
};

try {

    let response = await fetch("https://loan-api-fltv.onrender.com/predict",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    });

    let res = await response.json();

    console.log("API:", res);

    if(res.prediction === 0 || res.prediction === "Low Risk"){
        result.innerHTML = "✔ Low Risk - Loan approval chances high";
        result.className = "safe";
    }
    else{
        result.innerHTML = "❌ High Risk - Loan may be rejected";
        result.className = "risky";

        const alarm = document.getElementById("alarm");
        alarm.currentTime = 0;
        alarm.play().catch(() => {});
    }

}
catch(error){
    result.innerHTML="Server Error";
}

}
