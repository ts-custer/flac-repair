# __main__.py

"""
A program to to repair a .flac file which tag information can't be read by Clementine audio player.

Usage: flac_repair.py <flac file>
"""
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Tuple
import mutagen
import mutagen.flac
from datetime import date
import subprocess



def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('flac_file',
                        type=str,
                        help='Name of the flac audio file')
    args = parser.parse_args()

    # TODO check if file exists
    folder = os.path.dirname(args.flac_file)
    # print(folder)

    flac_file = mutagen.File(args.flac_file)
    # TODO Check if it's really a flac file

    # Delete all tag information
    # mutagen.flac.delete(args.flac_file)

    # Print out all tag information
    # for frame_id in flac_file.keys():
    #     print(f"{frame_id} -> {flac_file.get(frame_id)}")

    fetch_first_picture(flac_file)

    # extract_first_picture(flac_file, folder)

    # Copy with "sox" the flac file to '_.flac' (into the same folder)
    subprocess.run(['sox', args.flac_file, folder + os.sep + '_.flac'])

    # frame_ids = set([s[:4] for s in mp3_file.tags.keys()])
    # for frame_id in frame_ids:
    #     copy_frame(mp3_file, flac_file, frame_id)
    # copy_picture(mp3_file, flac_file)
    # set_description(flac_file)
    # flac_file.save()

def extract_first_picture(flac_file, folder):
    if flac_file.pictures:
        picture = flac_file.pictures[0]
        with open(folder + os.sep + picture.desc, 'wb') as f:
            f.write(picture.data)

def fetch_first_picture(flac_file):
    if flac_file.pictures:
        # global picture
        picture = flac_file.pictures[0]
        global picture_type
        picture_type = picture.type
        global picture_mime
        picture_mime = picture.mime
        global picture_name
        picture_name = picture.desc
        global picture_data
        picture_data = picture.data
        print(f'picture_type {picture_type}')
        print(f'mime {picture_mime}')
        print(f'picture_name {picture_name}')
        # print(f'picture_data {picture_data}')



def copy_frame(mp3_file, flac_file, frame_id):
    field_name = frame_id_mapping.get(frame_id)
    if field_name:
        content = mp3_file.tags.get(frame_id) and mp3_file.tags.get(frame_id).text[0]
        if content:
            flac_file[field_name] = str(content)


def copy_picture(mp3_file: mutagen.File, flac_file: mutagen.File):
    apic_list = mp3_file.tags.getall('APIC')
    if apic_list:
        first_apic = apic_list[0]
        if first_apic:
            set_picture(flac_file, first_apic.type, first_apic.mime, first_apic.desc, first_apic.data)


def set_picture(flac_file: mutagen.File, type, mime, description, picture_data):
    picture = mutagen.flac.Picture()
    picture.type = type
    picture.mime = mime
    picture.desc = description
    picture.data = picture_data
    update_picture(flac_file, picture)


def update_picture(flac_file: mutagen.File, picture: mutagen.flac.Picture):
    flac_file.clear_pictures()
    flac_file.add_picture(picture)


def set_description(flac_file, comment: str = str(date.today())):
    flac_file['DESCRIPTION'] = comment





if __name__ == '__main__':
    main()
