let calculateElo = (data) => {
    let expectedA = 1.00 / (1 + Math.pow(10, (data.B - data.A) / 400));
    let expectedB = 1.00 - expectedA;

    let factorA = (data.A_Win - expectedA);
    let factorB = (data.B_Win - expectedB);

    let timeFactorA = Math.log10(data.Time + 2) * 0.7;
    let timeFactorB = Math.log10(-data.Time + data.Time_Max + 1) * 1.1;

    if (timeFactorA > 1.00) timeFactorA = 1;
    if (timeFactorB > 1.00) timeFactorB = 1;

    if (timeFactorA < 0.00) timeFactorA = 0;
    if (timeFactorB < 0.00) timeFactorB = 0;

    if (data.A_Win == 1) {
        factorA *= timeFactorA;
        factorB *= timeFactorA;
    } else if (data.B_Win == 1) {
        factorA *= timeFactorB;
        factorB *= timeFactorB;
    }

    let newScoreA = Math.round(data.A + 32 * factorA);
    let newScoreB = Math.round(data.B + 32 * factorB);

    return {
        newScoreA,
        newScoreB
    };
}

let calculateEloRaw = (data) => {
    let expectedA = 1.00 / (1 + Math.pow(10, (data.B - data.A) / 400));
    let expectedB = 1.00 - expectedA;

    let factorA = (data.A_Win - expectedA);
    let factorB = (data.B_Win - expectedB);

    let newScoreA = Math.round(data.A + 32 * factorA);
    let newScoreB = Math.round(data.B + 32 * factorB);

    return {
        newScoreA,
        newScoreB
    };
}

let getRandomInt = (max) => {
    return Math.floor(Math.random() * Math.floor(max));
}

let ratingA = 1500;
let ratingB = 1500;
let winsA = 0;
let winsB = 0;

let Games = 100000;

let start = new Date();

let times = [];
for (let i = 0; i < 30; ++i) times[i] = 0;

let startPrinting = false;

for (let i = 0; i < Games; ++i) {
    let win = Math.random();
    let time = 30 - getRandomInt(5);

    times[time]++;

    if (win <= 0.2) {
        // wins A
        let newScores = calculateElo({
            A: ratingA,
            B: ratingB,
            A_Win: 1,
            B_Win: 0,
            Time: time,
            Time_Max: 30
        });

        ratingA = newScores.newScoreA;
        ratingB = newScores.newScoreB;

        if (ratingA < 300) {
            startPrinting = true;
        }

        winsA++;
    } else {
        // wins B
        let newScores = calculateElo({
            A: ratingA,
            B: ratingB,
            A_Win: 0,
            B_Win: 1,
            Time: time,
            Time_Max: 30
        });

        ratingA = newScores.newScoreA;
        ratingB = newScores.newScoreB;

        winsB++;
    }

    if (startPrinting) {
        console.log("[Game %i] A: %i , B: %i", i, ratingA, ratingB);
    }
}

let end = new Date();
console.log("Final Execution time: " + (end - start) + "ms");

console.log("Wins: A " + winsA + " - " + winsB + " B");
console.log("Final Rating of A: ", ratingA);
console.log("Final Rating of B: ", ratingB);

console.log(JSON.stringify(times));