#!/usr/bin/python3

"""
A script to to repair a .flac file which tag information can't be read by Clementine audio player.

Usage: flac_repair.py <flac file>

Prerequisites: Installed programs 'sox' and 'mutagen'
"""
from argparse import ArgumentParser
from pathlib import Path
from typing import List

import mutagen
import mutagen.flac
import subprocess
import os


def fetch_file_name() -> str:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('flac_file',
                        type=str,
                        help='Name of the flac audio file')
    args = parser.parse_args()
    return args.flac_file


def fetch_flac_file(file_name) -> mutagen.File:
    if not os.path.isfile(file_name):
        raise RuntimeError(f'File {file_name} does not exist')
    flac_file = mutagen.File(file_name)
    if type(flac_file) != mutagen.flac.FLAC:
        raise RuntimeError(f'File {file_name} is not a flac file')
    return flac_file


def fetch_absolute_directory_of_file(file_name: str) -> str:
    abs_path = os.path.abspath(file_name)
    file_name_length = len(Path(file_name).name)
    return abs_path[:-file_name_length]


def copy_flac_to_tmp_file(file_name) -> str:
    # Copy with "sox" the flac file to 'flac_repair.flac' (into the same folder)
    directory = fetch_absolute_directory_of_file(file_name)
    tmp_file_name = directory + 'flac_repair.flac'
    subprocess.run(['sox', file_name, tmp_file_name])
    return tmp_file_name


def save_pictures_of_tmp_file(pictures: List[mutagen.flac.Picture], tmp_file_name: str):
    tmp_flac_file = mutagen.File(tmp_file_name)
    tmp_flac_file.clear_pictures()
    if pictures:
        for picture in pictures:
            tmp_flac_file.add_picture(picture)
    tmp_flac_file.save()


def main():
    file_name = fetch_file_name()
    flac_file = fetch_flac_file(file_name)

    ## Delete all tag information
    # mutagen.flac.delete(file_name)

    ## Print out all tag information
    # for frame_id in flac_file.keys():
    #    print(f"{frame_id} -> {flac_file.get(frame_id)}")

    tmp_file_name = copy_flac_to_tmp_file(file_name)

    save_pictures_of_tmp_file(flac_file.pictures, tmp_file_name)

    # Rename tmp_file to the name of the to be repaired flag file
    os.rename(tmp_file_name, file_name)

    print(f'"{file_name}" repaired.')


if __name__ == '__main__':
    main()
