import os
# if you can't connect to openai, you may need to set your proxy options
os.environ["http_proxy"] = "http://127.0.0.1:8888"
os.environ["https_proxy"] = "http://127.0.0.1:8888"

# set the Azure Speech Service KEY and REGION
os.environ["SPEECH_KEY"] = ""
os.environ["SPEECH_REGION"] = ""

import openai

# set the openai ORG and KEY
openai.organization = ""
openai.api_key = ""



import azure.cognitiveservices.speech as speechsdk
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='zh-CN-YunxiNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def stt():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(
        'SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "en-US"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    print("[LISTENING...]")
    auto_detect_source_language_config = \
        speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["en-US", "zh-CN"])
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(
        result)
    detected_language = auto_detect_source_language_result.language
    print(f"[ME-{detected_language}]: {result.text}")
    return result.text

def tts(text):
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return True
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        return False

def chat(context):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context
    )
    return res["choices"][0]["message"]["content"]


def startConversation():
    context = []
    while(True):
        txt = stt()
        context.append({"role": "user", "content": txt})
        res = chat(context)
        print(f"[GPT]: {res}")
        tts(res)

startConversation()