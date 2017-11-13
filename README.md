# lexico

![lexical things](static/logo.png?raw=true)

The Command Line Tool to help expand your English vocabulary and familiarize you with those elusive words.

## What is `lexico`?

A fast and easily accessible tool for looking up English words.

![eleven](static/eleven.gif?raw=true)

### Motivation

In our day-to-day life, we (atleast Eleven) often encounter words whose meaning is not clear to us. We instinctively search the word up for meanings, synonyms, antonyms and what not. There are a lot of traditional ways I used to solve this problem:

1. **Dictionary Sites**

  The problem with dedicated vocabulary sites are twofold:  
    - the information is too overwhelming  
    - their is too much work to lookup

  These are the major impediments I faced while working with sites such as Vocabulary.com and other dictionaries.

2. **Search Engines**

  For some time I have used many `word meaning` Google searches to help me get the necessary information.
  However, this ad-hoc method is not a viable option from the point of longetivity since one is unable to record his progress.  
  Same goes for `define word` in DuckDuckGo.

3. **Physical Dictionary**

  - Not portable 
  - Save trees?

I built `lexico` as utility which will provide me with all the relevant information related to words while keeping track of my learnings. Hope this helps you as well!

### Features

- [x] Meanings
- [x] Synonyms
- [x] Antonyms
- [x] Examples
- [x] Phrases
- [x] Hyphenation
- [x] Audio
- [x] Text Pronunciations

## Usage

### Initialization and Setup

**Step 01**: Grab your Wordnik API key from the Settings in your Wordnik Account. Log into your account [here](https://www.wordnik.com/login); create one if you do not already have one.

**Step 02**: Initialize the vocabulary by running the command:  `$ lexico init`

**Step 03**: Provide the API key when prompted.

You will get a success message if the vocabulary was setup with no issues.  
However, if you face any issues, let me know [here](https://github.com/kshitij10496/lexico/issues).

### Search a word

Now that we have the application up and running, it's time to search for a word.  
There are 2 ways to lookup a word for your convenience.
            
1. Run : `$ lexico add`.    
   Enter the word when your are prompted to do so.

2. Try: `$ lexico add <your_word>`

### Viewing the vocabulary

The command `$ lexico view` displays all the words in your vocabulary with associated metadata.


## Installation

The latest version of the package is available on PyPI and can be installed via `pip` through:

`$ python3 -m pip install lexico`

 
## Development Guide

**Suggestion**: The use of a virtual environment is highly recommended.


### Set Up

**Step 01**: Fork and clone the repository.

**Step 02**: Change to the package folder: `$ cd lexico`

**Step 03**: Install the dependencies: `$ pip install -r requirements.txt`

**Step 04**: Install the package: `$ python3 setup.py install`

### Contributing

**Step 01**: Create a new branch based on the updated `master`.

**Step 02**: Make the changes and push it.

**Step 03**: Open up a PR against the `master` of this repository.

### TODOs

- [ ] Adding unit tests
- [ ] Import words from Kindle lookups
- [ ] Export current vocabulary in consumable format(e.g. CSV)
- [ ] Cusotmizable CLI

**NOTE**: The project is under heavy development and the code has only been tested manually.  
So, I won't be surprised if things break unexpectedly. Do report them as issues.  
The most common issue that you might face currently would be *connection timeouts*. 
