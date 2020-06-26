import editdistance
import soundfile
import os
import numpy as np
import pandas as pd
import json
import string
import subprocess
import time
import uuid
from enum import Enum
import boto3
import requests

def Punctuation(string): 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
    return string

class Dataset:
    def __init__(self):
        self._data = list()
    
    def size_hours(self):
        return sum(soundfile.read(self.get(i)[0])[0].size / (16000 * 3600) for i in range(self.size()))

    def size(self):
        return len(self._data)

    def get(self, index):
        return self._data[index]

    def __str__(self):
        return 'Dataset'

    def create(self):
        return self.generate(os.path.join(os.path.dirname(__file__), 'Data'))

    def generate(self, root):
        recordings_dir = os.path.join(root, 'recordings')
        test_dir = os.path.join(recordings_dir, 'test1')
        transcript_path = os.path.join(root, 'overview-of-recordings.csv')
        transcripts = pd.read_csv(r'C:\Users\Amit\Desktop\Cure.Fit\Week2\Data\overview-of-recordings.csv')
        transcripts = transcripts[['file_name', 'phrase']]
        transcripts.set_index('file_name', inplace = True)
        transcripts = (transcripts.to_dict())['phrase']
        for wav_file in os.listdir(test_dir):
                wav_path = os.path.join(test_dir, wav_file)
                if not os.path.exists(wav_path):
                    continue
                self._data.append((wav_path, transcripts[wav_file]))

class ASREngines(Enum):
    AMAZON_TRANSCRIBE = "AMAZON_TRANSCRIBE"

class ASREngine(object):
    def transcribe(self, path):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
    @classmethod
    def create(cls, engine_type):
        if engine_type is ASREngines.AMAZON_TRANSCRIBE:
            return AmazonTranscribe()
        else:
            raise ValueError("cannot create %s of type '%s'" % (cls.__name__, engine_type))

class AmazonTranscribe(ASREngine):
    def __init__(self):
        self._s3 = boto3.client('s3')
        #UNCOMMENT TO PROGRAMATICALLY CREATE A BUCKET
        #self._s3_bucket = 'bucket'+str(uuid.uuid4())[0:3]
        #session = boto3.session.Session()
        #current_region = session.region_name
        #print(current_region)
        #self._s3.create_bucket(
            #ACL='private',
            #Bucket=self._s3_bucket,
            #CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
        self._s3_bucket = 'testdocsapp'
        self._transcribe = boto3.client('transcribe')

    def transcribe(self, path):
        cache_path = path.replace('.wav', '.aws')
        if os.path.exists(cache_path):
            with open(cache_path) as f:
                return f.read()
        job_name = 'testdocsapp_'+ (path.split('\\'))[-1]
        s3_object = os.path.basename(path)
        self._s3.upload_file(path, self._s3_bucket, s3_object)
        self._transcribe.start_medical_transcription_job(
            MedicalTranscriptionJobName=job_name,
            Media={'MediaFileUri': 'https://s3.us-east-1.amazonaws.com/%s/%s' % (self._s3_bucket, s3_object)},
            MediaFormat='wav',
            LanguageCode='en-US',
            OutputBucketName='testdocsappdata',
            Settings={
            'ShowSpeakerLabels': False,
            'ChannelIdentification': False,
            'ShowAlternatives': False
            },
            Specialty='PRIMARYCARE',
            Type='DICTATION')
        while True:
            status = self._transcribe.get_medical_transcription_job(MedicalTranscriptionJobName=job_name)
            if(status['MedicalTranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED'):
                break
            time.sleep(1)
        self._transcribe.delete_medical_transcription_job(MedicalTranscriptionJobName=job_name)
        return ""

    def __str__(self):
        return 'Amazon Transcribe'


if __name__ == '__main__':
    dataset = Dataset()
    dataset.create()
    print('loaded %s with %.2f hours of data' % (str(dataset), dataset.size_hours()))
    engine = ASREngine.create(ASREngines["AMAZON_TRANSCRIBE"])
    print('created %s engine' % str(engine))  
    c = 0
    for i in range(dataset.size()):
        path, ref_transcript = dataset.get(i)
        c += 1
        print("File ",c,"-",path)
        transcript = engine.transcribe(path)
        if os.path.exists(path):
            os.remove(path)
