# SchoolNet Utilities
Repository for scripts and miscellaneous stuff for SchoolNet

## Scripts

These scripts are created for certain automations in the SchoolNet system.
The scripts are not used directly by the SchoolNet server.

* **process.questions.js** - Processes certain files with questions into a json dataset
* **post.questions.js** - Inserts the json dataset into a database
* **tests.js** - Used for temporary Javascript syntax testing
* **dbstate.js** - This file shows that the `database.state` attribute in the MySQL module is not updated fast enough, so the callback from the `.end()` function can check it. Don't rely upon it.

## Python

We use Python for data processing and AI.