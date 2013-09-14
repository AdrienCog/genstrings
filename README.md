# genstrings - update xcode translations

## Why

In Xcode projects, genstrings command erases completely Localizable.strings files. This means that you lose all changes you manually on the files.
This script wraps genstrings command to collect and set existing translations.


## How it works

- collects the existing translations in dictionary (key - translation)
- executes genstrings command recursively on full project
- collects the new strings and set existing translation when exists


## How to use

Put the script in your project root.
Execute the script with the following arguments:
-l --lang: language to update ("en",  ...), use this parameter as many times as necessary
-p --project: path of directory which contains all language directory ("en.lproj", ...)

## Next

This script is very basic, some improvements will be made later to be more flexible.
