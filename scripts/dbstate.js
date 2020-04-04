let databases = require("../server/dbConnection");

setTimeout(() => console.log(databases.network.state), 200);

let time = 0;

process.on("SIGINT", () => { 
    databases.network.end(() => console.log("callback: ", databases.network.state));
    console.log("out: ", databases.network.state);
    time++;
    if (time == 3) process.exit();
})