from deeploadData import *
from deepspeech import Model

class ASREngines(Enum):
    MOZILLA_DEEP_SPEECH = 'MOZILLA_DEEP_SPEECH'

class ASREngine(object):
    def transcribe(self, path):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    @classmethod
    def create(cls, engine_type):
        if engine_type is ASREngines.MOZILLA_DEEP_SPEECH:
            return MozillaDeepSpeechASREngine()
        else:
            raise ValueError("cannot create %s of type '%s'" % (cls.__name__, engine_type))

class MozillaDeepSpeechASREngine(ASREngine):
    def __init__(self):
        deepspeech_dir = os.path.join(os.path.dirname(__file__), 'deepspeech-0.6.0-models')
        model_path = os.path.join(deepspeech_dir, 'output_graph.pbmm')
        #alphabet_path = os.path.join(deepspeech_dir, 'alphabet.txt')
        language_model_path = os.path.join(deepspeech_dir, 'lm.binary')
        trie_path = os.path.join(deepspeech_dir, 'trie')
        lm_alpha = 0.75
        lm_beta = 1.85
        # https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py
        self._model = Model(model_path, 500)
        self._model.enableDecoderWithLM(language_model_path, trie_path, lm_alpha, lm_beta)

    def transcribe(self, path):
        pcm, sample_rate = soundfile.read(path)
        pcm = (np.iinfo(np.int16).max * pcm).astype(np.int16)
        res = self._model.stt(pcm)

        return res

    def __str__(self):
        return 'Mozilla DeepSpeech'

if __name__ == '__main__':
    dataset = Dataset()
    dataset.create()
    print('loaded %s with %.2f hours of data' % (str(dataset), dataset.size_hours()))
    engine = ASREngine.create(ASREngines['MOZILLA_DEEP_SPEECH'])
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
            print('WER - : %.2f' % (100*float(word_error_count)/word_count))
    print('######################################################################')
    print('FINALword error rate : %.2f' % (100*float(word_error_count)/word_count))
