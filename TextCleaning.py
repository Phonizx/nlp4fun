import nltk
from nltk.stem.snowball import SnowballStemmer
import os,glob
import re
import string
import json


#Cleaning iniziale da dare in pasto al PreEmbedder
class TextPreparation:

    unique_words = set()
    vocab_size = 0

    word2int = {}
    int2word = {}

    stopWords = {}
    #no white-space, no dot
    puncts = ['!','?',',',';',':','(',')']


    def __init__(self,path):
        self.path = path
        #self.stemmer = SnowballStemmer("italian")
        self.stemmer = nltk.stem.snowball.ItalianStemmer()

    def no_punctuation(self,sentence): #erase puncts
        sentence = sentence.translate({ord(c) : '' for c in self.puncts})
        return sentence

    def load_stopWord(self,path):
        i = 0
        with open(path,"r") as fstopword:
            for line in fstopword:
                l = line.replace('\n','')
                if l not in self.stopWords.keys():
                    self.stopWords[l] = i
                    i += 1
        print("Stop Words loaded.")

    def build_dicts(self):
        if(self.vocab_size > 0):
            for i,word in enumerate(self.unique_words):
                self.word2int[word] = i
                self.int2word[i] = word
        self.save_dicts()

    def save_dicts(self):

        dizionari = []
        dizionari.append(self.word2int)
        dizionari.append(self.int2word)
        dizionari.append(self.vocab_size)

        dict_file = open(self.path + "/dizionari.json", "w")
        dict_file.write(json.dumps(dizionari))
        dict_file.close()
        print("Data writed in: " + self.path + "dizionari.json")


    def prepare_texts(self):
        os.chdir(self.path)
        for file in glob.glob("*.txt"):
            with open(file,"r") as f:
                print("Text PreProcessing on: " + file.title())
                sentences = []
                for line in f:
                    line = self.no_punctuation(line)
                    l = line.split()
                    for iword in l:
                        if(iword not in self.stopWords.keys()):
                            iword = self.stemmer.stem(iword)
                            self.unique_words.add(iword) #aggiunge una parola non stop-word e stemmata al set di parole globali
                            sentences.append(iword + " ") #stemming not stopwords

            with open(file,"w") as f:
                f.writelines(sentences)
        self.vocab_size = len(self.unique_words)
        self.build_dicts()



tp = TextPreparation("/home/phinkie/Scrivania/psychic-octo-system/data/")
tp.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt") #path
tp.prepare_texts()
