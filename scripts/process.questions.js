const fs = require('fs');

let process = (FILE_NAME) => {
    let start = new Date();

    let defaultEntry = {
        Subject: 8,
        Question: "",
        Answer_1: "",
        Answer_2: "",
        Answer_3: "",
        Answer_4: "",
        Truth: 0,
        Rating: 1500,
        Valid: 1,
        Origin: "matura",
        Origin_Info: undefined
    }

    let indexes = {
        'A. ': 1,
        'Б. ': 2,
        'В. ': 3,
        'Г. ': 4
    };

    let entries = [];

    let objectCopy = (object) => {
        return JSON.parse(JSON.stringify(object));
    }

    fs.readFile("./raw/closedques/" + FILE_NAME + ".txt", 'utf-8', (err, fullFile) => {
        let currentYear = "";
        let currentEntry = objectCopy(defaultEntry);

        let lines = fullFile.split('\n');
        
        for (let key in lines) {
            let line = lines[key];
            let lineLength = line.length;

            if (lineLength == 1) continue;

            if (line[0] == "#") {
                // start a new year
                currentYear = line.substring(1, lineLength - 1);
                continue;
            } else if (line[0] == "!") {
                // that's the true answer
                let index = line.substring(1, 4);
                // console.log(index);
                currentEntry.Truth = indexes[index];

                line = line.substring(1, lineLength - 1);
                lineLength -= 1;
            }

            // set the origin
            currentEntry.Origin = "matura";
            currentEntry.Origin_Info = JSON.stringify({
                matura: currentYear
            });

            let index = line.substring(0, 3);

            if (typeof indexes[index] === "undefined") {
                currentEntry.Question += line + " ";
            } else {
                let nindex = indexes[index];
                currentEntry['Answer_' + nindex] = line.substring(3, lineLength - 1);

                if (nindex == 4) {
                    currentEntry.Question = currentEntry.Question.replace("\r ", "");
                    if (currentEntry.Question.length <= 150) {
                        entries.push(currentEntry);
                    }
                    
                    currentEntry = objectCopy(defaultEntry);
                }
            }
        }

        fs.writeFile("./processed/closedques/" + FILE_NAME + ".json", JSON.stringify({ databaseEntries: entries }), (err) => {
            if (err) console.log(err);
        });

        let end = new Date() - start;
        console.info('Execution time: %dms', end);
    });
}

module.exports.process = process;