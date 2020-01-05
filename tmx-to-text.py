# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
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

import xml.etree.ElementTree as ET
import polib


class ConvertTmx():

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        pofile = polib.POFile()


        tree = ET.parse(self.input_file)
        root = tree.getroot()
        sources = set()

        entries = 0
        for tu_entry in root.iter('tu'):

            entry_id = None
            if 'tuid' in tu_entry.attrib:
                if len(tu_entry.attrib['tuid']):
                    entry_id = 'id: {0}'.format(tu_entry.attrib['tuid'])

            source = ''
            translation = ''
            for tuv_entry in tu_entry:
                if tuv_entry.tag != 'tuv':
                    continue

                if '{http://www.w3.org/XML/1998/namespace}lang' in tuv_entry.attrib:
                    llengua = tuv_entry.attrib['{http://www.w3.org/XML/1998/namespace}lang'].lower()
                else:
                    llengua = tuv_entry.attrib['lang'].lower()

                for seg_entry in tuv_entry.iter('seg'):
                    if llengua == 'en' or llengua == 'en-us':
                        source = seg_entry.text
                    elif llengua == 'ca':
                        translation = seg_entry.text

            if source is None or source is '':
                continue

            if translation is None or translation is '':
                continue

            if source in sources:
                msgctxt = str(entries)
            else:
                msgctxt = None
                sources.add(source)

            entry = polib.POEntry(msgid=source, msgstr=translation,
                                  msgctxt=msgctxt, tcomment=entry_id)
            pofile.append(entry)
            entries = entries + 1

        pofile.save(self.output_file)

def main():

    print("Converts  into Text")
    print("and cleans the strings")

    txt_file = 'raw/GlobalVoices-ca-en.tmx'
    txt_en_file = 'input/gnome-user-manual-en.txt'
    txt_ca_file = 'input/gnome-user-manual-ca.txt'


    ConvertTmx


