# SchoolNet Utilities
Repository for scripts and miscellaneous stuff for SchoolNet

## Wikipedia Words Processing

We get the [Macedonian Wikipedia Database Dump](https://dumps.wikimedia.org/mkwiki/) and process it to find a dataset of words with frequency of usage.

### Overview of the steps when processing words

1. Download the `.xml` wikipedia dump
2. Convert each article from the `.xml` file to it's own `.txt` file while filtering the articles of unnecessary data
3. Create a `.json` dataset of words
4. Split the `.json` file
4. Test to find an example
5. Index in a DB (* still in works)

---

## Scripts

These scripts are created for certain automations in the SchoolNet system.
The scripts are not used directly by the SchoolNet server.

* **process.questions.js** - Processes certain files with questions into a json dataset
* **post.questions.js** - Inserts the json dataset into a database
* **dbstate.js** - This file shows that the `database.state` attribute in the MySQL module is not updated fast enough, so the callback from the `.end()` function can check it. Don't rely upon it.

## Python

We use Python for data processing and AI.

### Tests

There are a couple of tests in the `wikipedia` folder to test the modules. In the future we will implement some more.