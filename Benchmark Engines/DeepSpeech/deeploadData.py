import soundfile
import os
import pandas as pd
import editdistance
from loadData import *
import json
import string
import subprocess
import time
import uuid
import numpy as np
import requests
from enum import Enum
import nltk

nltk_stopwords = nltk.corpus.stopwords.words('english')

def Punctuation(string): 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
    return string

def StopWordRem(article):
    tokens = nltk.tokenize.word_tokenize(article)
    tokens = [token for token in tokens if not token in nltk_stopwords]
    return " ".join(tokens)

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
        test_dir = os.path.join(recordings_dir, 'deeptest')
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


