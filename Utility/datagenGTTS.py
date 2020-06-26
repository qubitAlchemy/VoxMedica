import nltk
import string
import re
from gtts import gTTS 
import os
import pandas as pd

def text_lowercase(text): 
    return text.lower()

def remove_punctuation(text): 
    translator = str.maketrans('', '', string.punctuation) 
    return text.translate(translator)

def remove_special_chars_and_numbers(text):
    finalText = ''
    for k in text.split("\n"):
        final = re.sub(r"[^a-zA-Z.]+", ' ', k)
        preFinal = ''
        for word in final.split():
            if(len(word)>3 and word!='nan'):
                preFinal += word+' '
        finalText += (preFinal).strip()
    return finalText

def cleanText(text):
    return remove_special_chars_and_numbers(text_lowercase(text))

def generate(index, text):
    language = 'en'
    obj = gTTS(text=text, lang=language, slow=False) 
    obj.save(str(index)+".wav")

"""
if __name__ == '__main__':
    mtrecords = r'ScrapedMT.csv'
    records = r'RecordsMT.txt'
    #recordsFile = open(records, mode='w+', encoding='utf-8')
    df = pd.read_csv(mtrecords)
    ind = 0
    for index, row in df.iterrows():
        rowText = str(row['description'])+' '+str(row['medical_specialty'])+' '+str(row['sample_name'])+' '+str(row['keywords'])+' '+str(row['transcription'])
        prepText = cleanText(rowText)
        print(prepText)
        for line in prepText.split('.'):
            prepLine = cleanText(line)
            #print(prepLine)
            if (len(prepLine.strip())>0):
                ind += 1
                #recordsFile.write(prepLine+'\n')
                generate(ind, prepLine)
                print(' --- Completed '+str(ind)+' ---')
    #recordsFile.close()
    print(ind)
"""
#For 500 records test
if __name__ == '__main__':
    f = open('RecordsMT500.txt', 'r')
    lines = f.readlines()
    ind = 1
    for line in lines:
        generate(ind, line)
        print(' --- Completed '+str(ind)+' ---')
        ind += 1
    f.close()
    print(ind)
