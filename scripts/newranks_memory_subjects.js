let databases = require("../server/dbConnection");

let start = new Date();

for (let i = 0; i < 9; ++i) {
    databases.ZNAM.query("SELECT ID, Rank, Score FROM tbl_scoreboard WHERE Subject = ?", i, (err, rows) => {
        if (typeof rows == "undefined" || rows.length == 0) {
            return;
        }
        
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
}