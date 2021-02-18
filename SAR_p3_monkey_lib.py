#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres: Andrés Marín Galán, Rocío García

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k][1].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]|[\n]{2}')
        self.r2 = re.compile('\W+')


    def index_sentence(self, sentence, tri):
        """
           indexa una palabra en el indice de bigramas y trigramas si tri es true
        """
        sentence = sentence.lower()
        sentence = self.r2.sub(" ", sentence)
        sentence = '$ ' + sentence +  ' $'
        sentence = sentence.split()
        if len(sentence) is 2:
            return
        i=1
        for word1 in sentence:
            if word1 not in self.index['bi']:
                    self.index['bi'][word1] = [1,{}]
            else:
                self.index['bi'][word1][0] = self.index['bi'][word1][0] + 1
            if i < len(sentence):
                if sentence[i] not in self.index['bi'][word1][1]:
                    self.index['bi'][word1][1][sentence[i]] = 1
                else:
                    self.index['bi'][word1][1][sentence[i]] = self.index['bi'][word1][1][sentence[i]] + 1
            i += 1

        if tri:
            i=1
            for word1 in sentence:
                if i < len(sentence)-1:
                    if (word1,sentence[i]) not in self.index['tri']:
                        self.index['tri'][(word1, sentence[i])] = [1, {}]
                    else:
                        self.index['tri'][(word1,sentence[i])][0] = self.index['tri'][(word1,sentence[i])][0] + 1
                    if sentence[i+1] not in self.index['tri'][(word1,sentence[i])][1]:
                        self.index['tri'][(word1,sentence[i])][1][sentence[i+1]] = 1
                    else:
                        self.index['tri'][(word1,sentence[i])][1][sentence[i+1]] = self.index['tri'][(word1,sentence[i])][1][sentence[i+1]] + 1
                i += 1
        pass


    def compute_index(self, filename, tri):
        """
        recoge un archivo y lo divide en frases para asi llamar a index_sentence por cada una
        """
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        fh = open(filename, 'r')
        oof = fh.read()
        oof = self.r1.split(oof)
        for sentence in oof:
            self.index_sentence(sentence, tri)
        sort_index(self.index['bi'])
        if tri:
            sort_index(self.index['tri'])
        

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)


    def generate_sentences(self, n=10):
        """
           Genera n frases o oraciones
        """
        if len(self.index.keys()) is 3:
            vilmetal = 0
            for tupla in self.index['tri'].keys():
                if tupla[0] is '$':
                    vilmetal += 1
            i=0
            while i < n:
                ale = random.random()
                aux = 0
                for tupla in self.index['tri'].keys():
                    if tupla[0] is '$':
                        prob = 1/vilmetal
                        aux += prob
                        if ale < aux:
                            print(tupla[1], end =' ')
                            word = tupla
                            break

                total = self.index['tri'][word][0]
                ale = random.random()
                aux = 0
                j=0
                for tupla in self.index['tri'][word][1]:
                    prob = self.index['tri'][word][1][j][0] / total
                    aux += prob
                    if ale < aux:
                        print(tupla[1], end = ' ')
                        break
                    j+=1

                j=0
                while j < 20:
                    aux = 0
                    total = len(self.index['tri'].keys())- vilmetal
                    ale = random.random()
                    for tupla in self.index['tri'].keys():
                        if tupla[0] is not '$':
                            prob = self.index['tri'][tupla][0]/total
                            aux += prob
                            if ale < aux:
                                print(tupla[0] + ' ' + tupla[1], end=' ')
                                word = tupla
                                break
                    k=0
                    aux = 0
                    total = self.index['tri'][word][0]
                    ale = random.random()
                    for tupla in self.index['tri'][word][1]:
                        prob = tupla[0] / total
                        aux += prob
                        if ale < aux:
                            if tupla[1] is '$':
                                j = 20
                                break                          
                            print(tupla[1], end = ' ')
                            break
                        k+=1
                    j+=1
                print('')
                i += 1
        else:
            i=0
            while i < n:
                total = self.index['bi']['$'][0]
                ale = random.random()
                aux = 0
                j=0
                for element in self.index['bi']['$'][1]:
                    prob = element[0]/total
                    aux += prob
                    if ale < aux:
                        word = self.index['bi']['$'][1][j][1]
                        if word is '$':
                            break
                        print(self.index['bi']['$'][1][j][1], end=' ')
                        break
                    j+=1
                j=0
                while j < 20:
                    if word is '$':
                        break
                    else:
                        aux =0
                        total = self.index['bi'][word][0]
                        ale = random.random()
                        k=0
                        for element in self.index['bi'][word][1]:
                            if word is '$':
                                break
                            prob = element[0]/total
                            aux += prob
                            if ale < aux:
                                if self.index['bi'][word][1][k][1] is '$':
                                    break
                                print(self.index['bi'][word][1][k][1], end=' ')
                                word = self.index['bi'][word][1][k][1]
                                break
                            k+=1
                    j+=1
                print('')
                i += 1
            


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


