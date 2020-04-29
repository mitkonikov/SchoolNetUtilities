let databases = require("./../server/dbConnection");

databases.ZNAM.query("SELECT * FROM tbl_questions", (err, questions) => {
    let IDs = [];
    let Lengths = [];
    for (let q of questions) {
        Lengths.push(q.Question.length);
        if (q.Question.length > 150) {
            IDs.push(q.ID);
        }
    }

    console.log(JSON.stringify(IDs));
    console.log(JSON.stringify(Lengths));

    databases.ZNAM.query("DELETE FROM tbl_questions WHERE ID IN (" + IDs.join() + ")", (err, rows) => {
        console.log(rows);
    });
});