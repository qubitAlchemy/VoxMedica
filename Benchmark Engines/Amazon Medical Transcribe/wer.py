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
import ast

def Punctuation(string): 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
    return string

class Dataset:
    def __init__(self):
        self._data = dict()
    
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
        test_dir = os.path.join(recordings_dir, 'testen')
        transcript_path = os.path.join(root, 'overview-of-recordings.csv')
        transcripts = pd.read_csv(r'C:\Users\Amit\Desktop\Cure.Fit\Week2\Data\overview-of-recordings.csv')
        transcripts = transcripts[['file_name', 'phrase']]
        transcripts.set_index('file_name', inplace = True)
        transcripts = (transcripts.to_dict())['phrase']
        for wav_file in os.listdir(test_dir):
                wav_path = os.path.join(test_dir, wav_file)
                if not os.path.exists(wav_path):
                    continue
                self._data[wav_file] = transcripts[wav_file]
        #print(self._data)

if __name__ == '__main__':
    dataset = Dataset()
    dataset.create() 
    word_error_count = 0
    word_count = 0
    c = 0
    root = os.path.join(os.path.dirname(__file__), 'medical')
    for filename in os.listdir(root):
        ref_transcript = dataset.get(filename[12:-5])
        c += 1
        print("File ",c," - ",end=" ")
        js_path = os.path.join(root, filename)
        f = open(js_path)
        data = json.load(f)
        #print(data)
        transcript = data['results']['transcripts'][0]['transcript']
        if(transcript is not None):
            ref_transcript = Punctuation(ref_transcript)
            transcript = Punctuation(transcript)
            ref_words = ref_transcript.strip('\n ').lower().split()
            words = transcript.strip('\n ').lower().split()
            print(ref_words," -=- ",words,end=" ")
            word_error_count += editdistance.eval(ref_words, words)
            word_count += len(ref_words)
            print('WER - : %.2f' % (100*float(word_error_count)/word_count))

    f = open('aws.txt', 'r')
    lines = f.readlines()
    for line in lines:
        c += 1
        print("File ",c," - ",end=" ")
        js = ast.literal_eval(line)
        ref_transcript = dataset.get(js['jobName'][12:])
        transcript = js['results']['transcripts'][0]['transcript']
        if(transcript is not None):
            ref_transcript = Punctuation(ref_transcript)
            transcript = Punctuation(transcript)
            ref_words = ref_transcript.strip('\n ').lower().split()
            words = transcript.strip('\n ').lower().split()
            print(ref_words," -=- ",words,end=" ")
            word_error_count += editdistance.eval(ref_words, words)
            word_count += len(ref_words)
            print('WER - : %.2f' % (100*float(word_error_count)/word_count))
    f.close()
    print('######################################################################')
    print('FINALword error rate : %.2f' % (100*float(word_error_count)/word_count))


"""
import wave
filename = 'Data/recordings/deeptest/1249120_44142156_61923551.wav'
w = wave.open(filename, 'r')
rate = w.getframerate()
frames = w.getnframes()
buffer = w.readframes(frames)
print(rate)
"""
"""
import os
root = os.path.join(os.path.dirname(__file__), 'Data')
recordings_dir = os.path.join(root, 'recordings')
test_dir = os.path.join(recordings_dir, 'deeptest')
for filename in os.listdir(test_dir):
    fname = os.path.join(test_dir, filename)
    if not fname.endswith('.wav.wav'):
        os.remove(fname)
    else:
        continue

for filename in os.listdir(test_dir):
    fname = os.path.join(test_dir, filename)
    os.rename(fname, fname[:-4])
"""
