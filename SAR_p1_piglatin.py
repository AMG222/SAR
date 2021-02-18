#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

#Autor: Andrés Marín Galán

import sys
import re


class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            self.re = re.compile("(\w+)([.,;?!]*)")
        else:
            self.re = re.compile("(\w+)(["+punt+"]*)")

    def translate_word(self, word):
        """
        Este método recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        uppert = False
        upperk = False
        if word.isupper():
            uppert = True
        if word[0].isupper():
            upperk = True
        if word[0].isalpha():
            if word[0] in "aeiouAEIOU":
                word = word + "yay"
            else: 
                aux = ""
                i = 0
                for let in word:
                    if let not in "aeiouAEIOU":
                        if let.isupper():
                            let = let.lower()
                        aux = aux + let
                    else: 
                        if word[len(word)-1] is ",":
                            word = word[i: len(word)-1] + aux + "ay,"
                            break
                        if word[len(word)-1] is ";":
                            word = word[i: len(word)-1] + aux + "ay;"
                            break
                        word = word[i: len(word)] + aux + "ay"
                        break
                    i += 1
        new_word = word
        if uppert:
            return new_word.upper() 
        if upperk:
            new_word = new_word[0].upper() + new_word[1: len(new_word)]
            return new_word
        return new_word

    def translate_sentence(self, sentence):
        """
        Este método recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        sentence = sentence.split()
        new_sentence = []
        for word in sentence:
            new_sentence.append(self.translate_word(word))
        new_sentence = " ".join(new_sentence) + "\n"
        return new_sentence

    def translate_file(self, filename):
        """
        Este método recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        try:
            files = filename
            name = filename.split(".")
            if len(name) > 1:
                name = name[0] + "_latin." + name[1]
            else:
                name = filename + "_latin"
            files = open(name, 'w')
            fh = open(filename, 'r')
            for line in fh:
                #print(self.translate_sentence(line))
                #print(self.translate_sentence(line))
                files.write(self.translate_sentence(line))
            files.close()
            return True
        except:
            print("NO, se ha podido traducir")
            return False



if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('Syntax: python %s [filename]' % sys.argv[0])
        exit
    else:
        t = Translator()
        if len(sys.argv) == 2:
            t.translate_file(sys.argv[1])
        else:
            while True:
                sentence = input("ENGLISH: ")
                if len(sentence) < 2:
                    break
                print("PIG LATIN:", t.translate_sentence(sentence))
