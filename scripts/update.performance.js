let databases = require("../server/dbConnection");

let start = new Date();

databases.ZNAM.query("UPDATE tbl_scoreboard SET Rank = Rank + 1 WHERE Score < 300", (err, rows) => {
    let end = new Date();
    console.log("Execution time: " + (end - start) + "ms");
});