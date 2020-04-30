const fs = require("fs");

let databases = require("./../server/dbConnection");

let post = (FILE_NAME, ID) => {
    fs.readFile("./processed/closedques/" + FILE_NAME + ".json", 'utf-8', (err, fullFile) => {
        if (err) {
            console.trace(err);
            return;
        }

        let object = JSON.parse(fullFile).databaseEntries;
        let count = 0;

        for (let entry of object) {
            count += 1;
            databases.ZNAM.query("INSERT INTO tbl_questions SET ?", entry);
        }

        console.log("Inserted " + count + " questions.");
    });
}

module.exports.post = post;