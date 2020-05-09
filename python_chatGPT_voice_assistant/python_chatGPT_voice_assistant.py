import openai
import pyttsx3
import speech_recognition as sr
import random
from openai import OpenAI
import sounddevice as sd

model_id = 'gpt-3.5-turbo'

openai_client = OpenAI(api_key="")
# Initialize the text-to-speech engine
engine = pyttsx3.init('dummy')

# Change speech rate
engine.setProperty('rate', 180)

# Get the avaiable voice
voices = engine.getProperty('voices')

# Choose a voice based on the voice id
engine.setProperty('voice', voices[0].id)

# Counter just for interacting purposes
interaction_counter = 0


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")
            # print('Skipping unknown error')


def ChatGPT_conversation(conversation):
    completion = openai_client.chat.completions.create(
        model=model_id,
        messages=conversation
    )
    response = completion.choices[0].message.content
    print(response)
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


# Starting conversation
conversation = []
conversation.append({'role': 'user',
                     'content': 'You are a language assistant to help teach tamil sst'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())


def activate_assistant():
    starting_chat_phrases = ["how may I assist you?"]

    continued_chat_phrases = ["yes", "yes, sir", "yes, boss", "I'm all ears"]

    random_chat = ""
    if (interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else:
        random_chat = random.choice(continued_chat_phrases)

    return random_chat


def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")


while True:

    # wait for users to say "Friend"
    print("Say 'Friend' to start...")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        print("!!!")
        try:
            transcription = recognizer.recognize_google(audio)
            print(transcription)
            if "friend" in transcription.lower():
                interaction_counter += 1
                # Record audio
                filename = "input.wav"
                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                # Transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print(f"You said: {text}")
                    append_to_log(f"You: {text}\n")

                    # Generate response using chatGPT
                    print(f"Friday says: {conversation}")

                    prompt = text
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGPT_conversation(conversation)

                    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")

                    # Read response using text-to-speech
                    speak_text(conversation[-1]['content'].strip())

                    # In future maybe a conversation.clear to decrease input tokens as the conversation evolves ...

        except Exception as e:
            continue
            # print("An error occurred: {}".format(e))
