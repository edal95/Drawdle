# Drawdle

A simple drawing tool for NYT's Wordle.

## Installation

1. Clone repository.
2. pip install requirements.txt in a virtual environment.
3. Run app.py from command line.
4. Web app will be available on localhost:5000.

Will be made available on my public website.

## Usage

* Click to cycle through colors for each square.
* Type in the 5-letter solution to today's Wordle.
* Click Draw.

## Notes

* Empty rows mean no match was found.
* Word repetition is avoided where possible.
* More commonly used matches are preferred.
* If no common match is found, obscure words not recognized by Wordle may be returned.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

This project utilizes the contents of Webster's Unabridged English Dictionary as made available in JSON form on [GitHub](https://github.com/adambom/dictionary) by *adambom* under the MIT License and in part under the Project Gutenberg License. Special thanks to Josh Wardle and the New York Times Games team for making and keeping this game alive.
