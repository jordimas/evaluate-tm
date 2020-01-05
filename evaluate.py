#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import nltk
import warnings
warnings.filterwarnings("ignore")

def show_bleu2(reference_file, hypotesis_file):
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        strings_ref = tf_ref.readlines()
        strings_hyp = tf_hyp.readlines()

        if len(strings_ref) != len(strings_hyp):
            print("Different number of lines in files")
            return

        bleu_score = nltk.translate.bleu_score.corpus_bleu(strings_ref, strings_hyp)
        print("Bleu score:" + str(bleu_score))


def show_bleu(reference_file, hypotesis_file):
    cumulative_bleu_score = 0
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        lines_ref = tf_ref.read().splitlines()
        lines_hyp = tf_hyp.read().splitlines()
        lines_ref = lines_ref[0:470]
        lines_hyp = lines_hyp[0:470]

        if len(lines_ref) != len(lines_hyp):
            print("Different number of lines in files")
            return

        # Str -> to tokens
        strings_ref = []
        for i in range(0, len(lines_ref)):
            strings_ref.append([(lines_ref[i].split())])# Double list

        strings_hyp = []
        for i in range(0, len(lines_hyp)):
            strings_hyp.append(lines_hyp[i].split())

        scored = 0
        for i in range(0, len(strings_ref)):
#            print("Ref->" + str(strings_ref[i]))
#            print("Hyp->" + str(strings_hyp[i]))

            bleu_score = nltk.translate.bleu_score.sentence_bleu(strings_ref[i], strings_hyp[i])
            cumulative_bleu_score += bleu_score
            scored = scored + 1

    average_blue = cumulative_bleu_score/len(strings_ref)
    print("** Bleu score (average): {0} (sentences {1})".format(str(average_blue), scored))
    bleu_score = nltk.translate.bleu_score.corpus_bleu(strings_ref, strings_hyp)
    print("** Bleu score (corpus): " + str(bleu_score))

def _test():
#    reference = [['this', 'is', 'a', 'test', 'test2']]
#    candidate = ['thisx', 'isx', 'a',  'test2']
    reference = list('Creative Commons'.split())
    candidate = 'Creative Commons'.split()

    reference = ['this is a test test2'.split()]
    candidate = 'this is a test test2'.split()
    reference2 = [['this', 'is', 'a', 'test', 'test2']]
    candidate2 = ['thisx', 'is', 'a',  'test2']


#    for i in range(0, len(reference)):
#        print("Ref:" + reference[i])
#        print("Can:" + candidate[i])

    print("Reference:" + str(reference))
    print("Candidate:" + str(candidate))

    score = nltk.translate.bleu_score.sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))
    print(score)
    print(score * 100)
    exit(1)


def main():

#    _test()
    print("Apertium (local)")
    show_bleu('input/gnome-user-manual-ca.txt', 'translated/gnome-user-manual-apertium-local-ca.txt')

    print("Apertium (Softcatalà)")
    show_bleu('input/gnome-user-manual-ca.txt', 'translated/gnome-user-manual-apertium-ca.txt')

    print("Yandex")
    show_bleu('input/gnome-user-manual-ca.txt', 'translated/gnome-user-manual-yandex-ca.txt')

    print("Google")
    show_bleu('input/gnome-user-manual-ca.txt', 'translated/gnome-user-manual-google-ca.txt')

    print("OpenNMT")
    show_bleu('input/gnome-user-manual-ca.txt', '/home/jordi/sc/OpenNMT/nmt-softcatala/ApplyToPoFile/output.txt')


if __name__ == "__main__":
    main()
