let databases = require("./../server/dbConnection");

for (let i = 0; i < 9; ++i) {
    databases.ZNAM.query("SELECT COUNT(*) AS Count FROM tbl_questions WHERE Subject_ID = ?", i, (err, rows) => {
        let count = rows[0].Count;
        databases.ZNAM.query("INSERT INTO tbl_subjects SET ?", {
            Subject_ID: i,
            Count_Questions: count
        });
    });
}