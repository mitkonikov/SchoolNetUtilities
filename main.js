const dotenv            = require('dotenv');
dotenv.config();

let processQs = require("./scripts/process.questions.js");
let postQs = require("./scripts/post.questions.js");

let FILE_NAME = "history";
processQs.process(FILE_NAME);
postQs.post(FILE_NAME);

// let test = require("./scripts/filter.questions.js");