from loadData import *
import speech_recognition as sr

from os.path import join, dirname 
from ibm_watson import SpeechToTextV1 
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ASREngines(Enum):
    IBM_WATSON = "IBM_WATSON"

class ASREngine(object):
    def transcribe(self, path):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    @classmethod
    def create(cls, engine_type):
        if engine_type is ASREngines.IBM_WATSON:
            return IBM_Watson()
        else:
            raise ValueError("cannot create %s of type '%s'" % (cls.__name__, engine_type))

class IBM_Watson(ASREngine):
    def __init__(self):
        # Insert API Key in place of  
        # 'YOUR UNIQUE API KEY' 
        self._authenticator = IAMAuthenticator('API_key')  
        self._service = SpeechToTextV1(authenticator = self._authenticator) 
        #Insert URL in place of 'API_URL'  
        self._service.set_service_url('URL')    

    def transcribe(self, path):      
        with open(path, 'rb') as audio_file: 
            dic = json.loads(json.dumps( 
                    self._service.recognize( 
                    audio=audio_file, 
                    content_type='audio/wav',    
                    model='en-US_NarrowbandModel', 
                    continuous=True).get_result(), indent=2))   
    
        transc = "" 
        while bool(dic.get('results')): 
            transc = dic.get('results').pop().get('alternatives').pop().get('transcript')+transc[:] 
        return transc 

    def __str__(self):
        return 'IBM WATSON'

if __name__ == '__main__':
    engine_name = "IBM_WATSON"
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
