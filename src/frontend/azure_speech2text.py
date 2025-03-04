import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import fonctions_db as fdb


load_dotenv('../../.env')
 # Configuration du service Azure (utilise les constantes "SPEECH_KEY" and "SPEECH_REGION")
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_recognition_language="fr-FR"


def recognize_from_microphone():
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        fdb.write_msg_DB("ERROR", "recognize_from_microphone(): {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        fdb.write_msg_DB("ERROR", "recognize_from_microphone(): {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
            fdb.write_msg_DB("ERROR", "recognize_from_microphone(): {}".format(cancellation_details.error_details))
    return(speech_recognition_result)

def text2speech(text : str = "Bonjour, comment ça va ?"):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Synthèse vocale réussie.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Synthèse vocale annulée: {}".format(cancellation_details.reason))
        fdb.write_msg_DB("ERROR", "text2speech(): {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
            fdb.write_msg_DB("ERROR", "text2speech(): {}".format(cancellation_details.error_details))
    return result




if __name__ == "__main__":
    x = recognize_from_microphone()
    print(x)
    text2speech(x.text)
    print("Done")
    

