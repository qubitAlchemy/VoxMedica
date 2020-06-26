from loadData import *
import speech_recognition as sr

from os.path import join, dirname 
from ibm_watson import SpeechToTextV1 
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ASREngines(Enum):
    GOOGLE_SPEECH_TO_TEXT = "GOOGLE_SPEECH_TO_TEXT"

class ASREngine(object):
    def transcribe(self, path):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    @classmethod
    def create(cls, engine_type):
        if engine_type is ASREngines.GOOGLE_SPEECH_TO_TEXT:
            return GoogleSpeechToText()
        elif engine_type is ASREngines.IBM_WATSON:
            return IBM_Watson()
        else:
            raise ValueError("cannot create %s of type '%s'" % (cls.__name__, engine_type))

class GoogleSpeechToText(ASREngine):
    def __init__(self):
        self._client = sr.Recognizer()

    def transcribe(self, path):    
        res = None
        with sr.AudioFile(path) as source: 
            audio = self._client.record(source)   
        try: 
            res = self._client.recognize_google(audio)   
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))         
        return res

    def __str__(self):
        return 'Google Speech-to-Text'

if __name__ == '__main__':
    engine_name = "GOOGLE_SPEECH_TO_TEXT"
    dataset = Dataset()
    dataset.create()
    print('loaded %s with %.2f hours of data' % (str(dataset), dataset.size_hours()))
    engine = ASREngine.create(ASREngines[engine_name])
    print('created %s engine' % str(engine))  
    word_error_count = 0
    word_count = 0
    c = 0
    for i in range(dataset.size()):
        path, ref_transcript = dataset.get(i)
        c += 1
        print("File ",c," - ",end=" ")
        transcript = engine.transcribe(path)

        if(transcript is not None):
           
            ref_transcript = Punctuation(ref_transcript)
            transcript = Punctuation(transcript)
           
            ref_words = ref_transcript.strip('\n ').lower().split()
            words = transcript.strip('\n ').lower().split()
            print(ref_words," -=- ",words,end=" ")
            word_error_count += editdistance.eval(ref_words, words)
            word_count += len(ref_words)
            print('WER2 - : %.2f' % (100*float(word_error_count)/word_count))
    print('######################################################################')
    print('FINALword error rate2 : %.2f' % (100*float(word_error_count)/word_count))
