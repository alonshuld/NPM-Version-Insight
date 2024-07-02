# NPM Version Insight

This project will get a name of a npm package and a number that represents the amount of last versions we want to look at.
The program will get the README file for each version, analyze and compare them and it will output a summery and the identification of the breaking changes in the relevant versions.

You can choose if you want to check unofficial versions and what AI you want to use (Google or ChatGPT) by uncommenting the lines in the code

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sys, re, requests, openai, google-generativeai.

```bash
pip install sys
pip install re
pip install requests
pip install openai
pip install google-generativeai
```

## Usage

Add your API KEY of the chosen AI module

```bash
python main.py {npm_package_name} {number_of_versions}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
