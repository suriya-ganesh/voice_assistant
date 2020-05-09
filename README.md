GPT based speech assistant

use `python 3.9` to run this project

## Installation
```bash
pip install -r requirements.txt
```

## Usage
add openai api key in line 6, `main.py`

```bash
python main.py
```
then enter the file name and wait for response.
for example, if you're starting with file `input/3.wav`, you can enter `3` and press enter.

The bot is in an infinite loop and will keep asking for the file name until you exit the program.
it also remembers the previous conversation and will continue from where it left off.



## supporting scripts in the project:
- `recorder.py` for recording audio
    - run `python recorder.py <file_name> ` to record audio in wav format. it will be stored under input
