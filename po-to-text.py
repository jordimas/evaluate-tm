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

import json
import polib
import re
import os
import fnmatch

    
def clean_string(text):
    text = re.sub('[_&~]', '', text)
    text = re.sub('<[^>]*>', '', text) # Remove HTML tags
    return text

def main():

    print("Converts GNOME User Manual into Text")
    print("and cleans the strings")

    po_file = 'raw/gnome-user-manual-ca.po'
    txt_en_file = 'input/gnome-user-manual-en.txt'
    txt_ca_file = 'input/gnome-user-manual-ca.txt'

    strings = 0
    with open(txt_en_file, 'w') as tf_en, open(txt_ca_file, 'w') as tf_ca:
        source_po = polib.pofile(po_file)
        for entry in source_po:
            src = clean_string(entry.msgid)
            trg = clean_string(entry.msgstr)
            if '\t' in src or '\t' in trg:
                continue

            if '\n' in src or '\n' in trg:
                continue

            tf_en.write("{0}\n".format(src))
            tf_ca.write("{0}\n".format(trg))
            strings = strings + 1

    print("Wrote {0} strings".format(strings))
        

if __name__ == "__main__":
    main()
