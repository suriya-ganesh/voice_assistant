from pathlib import Path

from openai import OpenAI
from playsound import playsound

openai_client = OpenAI(api_key="")
messages = [
            {"role": "system", "content": "You are a helpful assistant who answers in tamil , your response should be kind and playful. " }]

def stt(audio_path):
    audio_file = open(audio_path, "rb")
    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(transcription.text)
    return transcription.text


def callgpt(messages):
    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages= messages,
    )
    print("!!!!!!")
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def tts(text):
    speech_file_path = Path(__file__).parent / "output/speech.mp3"
    with openai_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text
    ) as response:

        response.stream_to_file(speech_file_path)
    playsound(speech_file_path)


while True:
    file = input("Enter the file path: \n")
    user_speech = stt(f'input/{file}.wav')
    print("user_speech is converted to text:")
    print(user_speech)
    messages.append({"role": "user", "content": user_speech})
    gpt_response = callgpt(messages)
    print("gpt_response was:")
    print(gpt_response)
    messages.append({"role": "assistant", "content": gpt_response})
    tts(gpt_response)
    print("Assistant's response was spoken")
    print("-----------------------------------\n\n")
