let databases = require("../server/dbConnection");

let start = new Date();

databases.ZNAM.query("SELECT ID, Rank, Score FROM tbl_scoreboard", (err, rows) => {    
    rows.sort((a, b) => (b.Score - a.Score));

    let newRows = [];

    let rank = 1;
    let score = rows[0].Score;
    for (let row of rows) {
        row.Old_Rank = row.Rank;
        if (score == row.Score) {
            row.Rank = rank;
        } else {
            rank++;
            row.Rank = rank;
            score = row.Score;
        }

        if (row.Old_Rank != row.Rank) {
            newRows.push(row);
        }
    }
    // EXEC TIME: 70ms

    // rows.sort((a, b) => (a.ID - b.ID));

    let count = 0;
    let query = "";
    for (let row of newRows) {
        query += "UPDATE tbl_scoreboard SET Rank='"+row.Rank+"' WHERE ID='"+row.ID+"'; ";
        count++;
    }

    if (query == "") {
        console.log("empty query!");
        return;
    }

    databases.ZNAM.query(query, (err, rows) => {
        let end = new Date();
        console.log("Execution time: " + (end - start) + "ms"); // 15s
        console.log("Queries: " + count);

        if (err) {
            console.log(err);
        }
    });
});

    /*
    let count = 0;
    let done = false;
    for (let row of rows) {
        databases.ZNAM.query("UPDATE tbl_scoreboard SET Rank = ? WHERE ID = ?", [row.Rank, row.ID], (err, rows) => {
            count++;
            if (row.Score == 0) {
                if (!done) {
                    let end = new Date();
                    console.log("Execution time: " + (end - start) + "ms"); // 13.5s - LOOONG
                    console.log("Queries: " + count);
                }
                done = true;
            }
        })
    }
*/
/*
    for (let i = 0; i < 10; ++i) {
        console.log(rows[i]);
    }*/