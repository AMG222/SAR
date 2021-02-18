#! -*- encoding: utf8 -*-



## Nombres: Andrés Marín Galán
##Cuenta bigramas? Si

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto
            

        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """

        with open(filename, 'w') as fh:
            fh.write("Lines: " + str(stats['nlines']) + "\n")
            fh.write("Number words (including stopwords): " + str(stats['nwords']) + "\n")
            if use_stopwords:
                fh.write("Number words (without stopwords): " + str(stats['nwordssw']) + "\n")
            fh.write("Vocabulary size: " + str(stats['nwordsd']) + "\n")
            fh.write("Number of symbols: " + str(stats['nletters']) + "\n")
            fh.write("Number of different symbols: " + str(stats['nlettersd']) + "\n")
            fh.write("Words (alphabetical order):" + "\n")
            sbfw=sort_dic_by_values(stats['word'])
            sbaw=sorted(stats['word'].items())
            sbfs=sort_dic_by_values(stats['symbol'])
            sbas=sorted(stats['symbol'].items())
            if 'biword' in stats:
                bwf=sort_dic_by_values(stats['biword'])
                bwa=sorted(stats['biword'].items())
                blf=sort_dic_by_values(stats['bisymbol'])
                bla=sorted(stats['bisymbol'].items())
            if full:
                for word in sbaw:
                    fh.write("	" + word[0] + ": " + str(stats['word'][word[0]]) + "\n")
                fh.write("Words (by frequency):" + "\n")
                for word in sbfw:
                    fh.write("	" + word[0] + ": " + str(stats['word'][word[0]]) + "\n")
                fh.write("Symbols (alphabetical order):" + "\n")
                for letter in sbas:
                    fh.write("	" + letter[0] + ": " + str(stats['symbol'][letter[0]]) + "\n")
                fh.write("Symbols (by frequency):" + "\n")
                for letter in sbfs:
                    fh.write("	" + letter[0] + ": " + str(stats['symbol'][letter[0]]) + "\n")
                if 'biword' in stats:
                    fh.write("Word pairs (alphabetical order):" + "\n")
                    for tupla in bwa:
                        fh.write("	" + tupla[0][0] + " " + tupla[0][1]+ ": " + str(stats['biword'][tupla[0]]) + "\n")
                    fh.write("Word pairs (by frequency):" + "\n")
                    for tupla in bwf:
                        fh.write("	" + tupla[0][0] + " " + tupla[0][1]+ ": " + str(stats['biword'][tupla[0]]) + "\n")
                    fh.write("Symbol pairs (alphabetical order):" + "\n")
                    for tupla in bla:
                        fh.write("	" + tupla[0][0] + "" + tupla[0][1] + ": " + str(stats['bisymbol'][tupla[0]]) + "\n")
                    fh.write("Symbol pairs (by frequency):" + "\n")
                    for tupla in blf:
                        fh.write("	" + tupla[0][0] + "" + tupla[0][1] + ": " + str(stats['bisymbol'][tupla[0]]) + "\n")
            else:
                i=0
                for word in sbaw:
                    if i < 20:
                        fh.write("	" + word[0] + ": " + str(stats['word'][word[0]]) + "\n")
                        i +=1
                fh.write("Words (by frequency):" + "\n")
                i=0
                for word in sbfw:
                    if i < 20:
                        fh.write("	" + word[0] + ": " + str(stats['word'][word[0]]) + "\n")
                        i += 1
                fh.write("Symbols (alphabetical order):" + "\n")
                i = 0
                for letter in sbas:
                    if i < 20:
                        fh.write("	" + letter[0] + ": " + str(stats['symbol'][letter[0]]) + "\n")
                        i +=1
                fh.write("Symbols (by frequency):" + "\n")
                i = 0
                for letter in sbfs:
                    if i < 20:
                        fh.write("	" + letter[0] + ": " + str(stats['symbol'][letter[0]]) + "\n")
                        i +=1
                if 'biword' in stats:
                    fh.write("Word pairs (alphabetical order):" + "\n")
                    i=0
                    for tupla in bwa:
                        if i < 20:
                            fh.write("	" + tupla[0][0] + " " + tupla[0][1]+ ": " + str(stats['biword'][tupla[0]]) + "\n")
                            i += 1
                    fh.write("Word pairs (by frequency):" + "\n")
                    i=0
                    for tupla in bwf:
                        if i < 20:
                            fh.write("	" + tupla[0][0] + " " + tupla[0][1]+ ": " + str(stats['biword'][tupla[0]]) + "\n")
                            i += 1
                    fh.write("Symbol pairs (alphabetical order):" + "\n")
                    i=0
                    for tupla in bla:
                        if i < 20:
                            fh.write("	" + tupla[0][0] + "" + tupla[0][1]+ ": " + str(stats['bisymbol'][tupla[0]]) + "\n")
                            i += 1
                    fh.write("Symbol pairs (by frequency):" + "\n")
                    i=0
                    for tupla in blf:
                        if i < 20:
                            fh.write("	" + tupla[0][0] + "" + tupla[0][1]+ ": " + str(stats['bisymbol'][tupla[0]]) + "\n")
                            i += 1
            fh.close()
            pass


    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto
            

        :param 
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results
        sts = {
                'nwords': 0,
                'nwordssw':0,
                'nlines': 0,
                'nwordsd':0,
                'nletters':0,
                'nlettersd':0,
                'word': {},
                'symbol': {}
                }
        fh = open(filename, 'r')
        fh = fh.readlines()
        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}
            if stopwordsfile is not None:
                sts['nlines'] += len(fh)
                for line in fh:
                    if lower:
                        line = self.clean_re.sub(" ", line.lower()).split()
                    else:
                        line = self.clean_re.sub(" ", line).split()
                    sts['nwords'] += len(line)
                    antw = None
                    j=1
                    for wor in line:
                        if wor not in stopwords:
                            if 1 is len(line):
                                aux = ('$', wor)
                                if aux not in sts['biword']:
                                    sts['biword'][aux] = 1
                                else:
                                    sts['biword'][aux] = sts['biword'][aux] + 1
                                aux = (wor, '$')
                                if aux not in sts['biword']:
                                    sts['biword'][aux] = 1
                                else:
                                    sts['biword'][aux] = sts['biword'][aux] + 1
                            else:
                                if j is not 1:
                                    if antw is not None:
                                        aux = (antw, wor)
                                        if aux not in sts['biword']:
                                            sts['biword'][aux] = 1
                                        else:
                                            sts['biword'][aux] = sts['biword'][aux] + 1
                                    if j is len(line):
                                        aux = (wor, '$')
                                        if aux not in sts['biword']:
                                            sts['biword'][aux] = 1
                                        else:
                                            sts['biword'][aux] = sts['biword'][aux] + 1
                                else:
                                    aux = ('$', wor)
                                    if aux not in sts['biword']:
                                        sts['biword'][aux] = 1
                                    else:
                                        sts['biword'][aux] = sts['biword'][aux] + 1
                            antw=wor
                        else:
                            antw=None
                        if wor not in sts['word']:
                            if wor not in stopwords:
                                sts['word'][wor] = 1
                                sts['nwordsd'] += 1
                        else:
                            sts['word'][wor] = sts['word'][wor] + 1
                        if wor not in stopwords:
                            sts['nletters'] += len(wor)
                            sts['nwordssw'] += 1
                            antl = None
                            for letter in wor:
                                if antl is not None:
                                    auxl = (antl, letter)
                                    if auxl not in sts['bisymbol']:
                                        sts['bisymbol'][auxl] = 1
                                    else:
                                        sts['bisymbol'][auxl] = sts['bisymbol'][auxl] + 1
                                if letter not in sts['symbol']:
                                    sts['symbol'][letter] = 1
                                    sts['nlettersd'] += 1
                                else:
                                    sts['symbol'][letter] = sts['symbol'][letter] + 1
                                antl = letter
                        j += 1
            else:
                sts['nlines'] += len(fh)
                for line in fh:
                    if lower:
                        line = self.clean_re.sub(" ", line.lower()).split()
                    else:
                        line = self.clean_re.sub(" ", line).split()
                    sts['nwords'] += len(line)
                    antw = None
                    i=0
                    for wor in line:
                        if 1 is len(line):
                            aux = ('$', wor)
                            if aux not in sts['biword']:
                                    sts['biword'][aux] = 1
                            else:
                                sts['biword'][aux] = sts['biword'][aux] + 1
                            aux = (wor, '$')
                            if aux not in sts['biword']:
                                sts['biword'][aux] = 1
                            else:
                                sts['biword'][aux] = sts['biword'][aux] + 1
                        else:
                            if i is not 0:
                                aux = (antw, wor)
                                if wor is line[len(line)-1]:
                                    antw=None
                                if aux not in sts['biword']:
                                    sts['biword'][aux] = 1
                                else:
                                    sts['biword'][aux] = sts['biword'][aux] + 1
                                if i is len(line)-1:
                                    aux = (wor, '$')
                                    if aux not in sts['biword']:
                                        sts['biword'][aux] = 1
                                    else:
                                        sts['biword'][aux] = sts['biword'][aux] + 1
                            else:
                                aux = ('$', wor)
                                if aux not in sts['biword']:
                                    sts['biword'][aux] = 1
                                else:
                                    sts['biword'][aux] = sts['biword'][aux] + 1
                            antw=wor
                        i += 1
                        sts['nletters'] += len(wor)
                        if wor not in sts['word']:
                            if wor not in stopwords:
                                sts['word'][wor] = 1
                                sts['nwordsd'] += 1
                        else:
                            sts['word'][wor] = sts['word'][wor] + 1
                        antl=None
                        for letter in wor:
                            if antl is not None:
                                auxl = (antl, letter)
                                if auxl not in sts['bisymbol']:
                                    sts['bisymbol'][auxl] = 1
                                else:
                                    sts['bisymbol'][auxl] = sts['bisymbol'][auxl] + 1
                            if letter not in sts['symbol']:
                                sts['symbol'][letter] = 1
                                sts['nlettersd'] += 1
                            else:
                                sts['symbol'][letter] = sts['symbol'][letter] + 1
                            antl=letter
        else:
            if stopwordsfile is not None:
                sts['nlines'] += len(fh)
                for line in fh:
                    if lower:
                        line = self.clean_re.sub(" ", line.lower()).split()
                    else:
                        line = self.clean_re.sub(" ", line).split()
                    sts['nwords'] += len(line)
                    for wor in line:
                        if wor not in sts['word']:
                            if wor not in stopwords:
                                sts['word'][wor] = 1
                                sts['nwordsd'] += 1
                        else:
                            sts['word'][wor] = sts['word'][wor] + 1
                        if wor not in stopwords:
                            sts['nletters'] += len(wor)
                            sts['nwordssw'] += 1
                            for letter in wor:
                                if letter not in sts['symbol']:
                                    sts['symbol'][letter] = 1
                                    sts['nlettersd'] += 1
                                else:
                                    sts['symbol'][letter] = sts['symbol'][letter] + 1
            else:
                sts['nlines'] += len(fh)
                for line in fh:
                    if lower:
                        line = self.clean_re.sub(" ", line.lower()).split()
                    else:
                        line = self.clean_re.sub(" ", line).split()
                    sts['nwords'] += len(line)
                    for wor in line:
                        sts['nletters'] += len(wor)
                        if wor not in sts['word']:
                            if wor not in stopwords:
                                sts['word'][wor] = 1
                                sts['nwordsd'] += 1
                        else:
                            sts['word'][wor] = sts['word'][wor] + 1
                        for letter in wor:
                            if letter not in sts['symbol']:
                                sts['symbol'][letter] = 1
                                sts['nlettersd'] += 1
                            else:
                                sts['symbol'][letter] = sts['symbol'][letter] + 1
        auxfile = filename.split(".")
        codigo = ""
        if lower:
            codigo += "l"
        if stopwordsfile is not None:
            codigo += "s"
        if bigrams:
            codigo += "b"
        if full:
            codigo += "f"
        if codigo is not "":
            codigo = "_" + codigo
        new_filename = auxfile[0] + codigo + "_stats" + "." +auxfile[1]
        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto
            

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower', action='store_true', default=False, 
                    help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                    help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram', action='store_true', default=False, 
                    help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full', action='store_true', default=False, 
                    help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file, lower=args.lower, stopwordsfile=args.stopwords, bigrams=args.bigram, full=args.full)