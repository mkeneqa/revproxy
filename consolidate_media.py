import os.path
from os import path
from os.path import dirname, basename
from shutil import copyfile
import hashlib
import sqlite3
from sqlite3 import Error
import db_lite

PROXY_DIR = "media/proxies"
ORIG_DIR = "media/originals"
MESSAGE = {
    'success': [],
    'info': [],
    'warning': [],
    'error': [],
}

VIDEO_FILES = [{
    "src_path": "/Volumes/Cinematography/FOOTAGE/2018/Javen 2018/ClearWaterAugustLong/August11/proxies/P1133324_proxy.mp4",
    "proxy_file": 1
}]


def get_full_file_path(full_file_path):
    file_name = os.path.basename(full_file_path)
    dest_dir = os.getcwd()
    return "{}/{}".format(dest_dir, file_name)


def file_exists_in_location(dest_file_path):
    if path.exists(dest_file_path):
        return True
    else:
        return False


def process_video_collection(video_collection, dest_dir):
    for video_path in video_collection:
        if file_exists_in_location(video_path):
            base_name = os.path.basename(video_path)
            video_dest = f"{dest_dir}/{base_name}"
            if file_exists_in_location(video_dest):
                MESSAGE['warning'].append("SKIPPING, File Already Copied: {}".format(video_dest))
                return True
            else:
                copy_media(video_path, video_dest)

            return True

    MESSAGE['warning'].append(f"No file found in video collection. first el: {video_collection[0]}")
    return False


def get_file_checksum(file_path):
    md5_check = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(900000000), b""):
            md5_check.update(chunk)
    return md5_check.hexdigest()


def copy_media(_source, _dest):
    try:
        print("source checksum ...")
        src_checksum = get_file_checksum(_source)
        copyfile(_source, _dest)

        print("copied from: {} to: {}".format(_source, _dest))

        print("destination checksum ...")
        dest_checksum = get_file_checksum(_dest)

        checksum_msg = 'Checksums MATCH: {}'.format(src_checksum)
        if src_checksum != dest_checksum:
            checksum_msg = 'WARNING: Checksums DO NOT MATCH! {} != {}'.format(src_checksum, dest_checksum)
            MESSAGE['warning'].append(checksum_msg)
        else:
            MESSAGE['success'].append(f"Successfully copied {os.path.basename(_dest)}")

        print(checksum_msg)
        print('_______________________________________________________')
        print(" ")

    except Exception as e:
        print("ERR: Could Not Copy File! {}".format(str(e)))
        print("ERR SRC File: {}".format(_source))
        print("ERR DEST File: {}".format(_dest))
        print('_______________________________________________________')
        print('')
        MESSAGE['error'].append("Could Not Copy File! {}".format(str(e)))


def test():
    pass


def strip_file_meta(file_name):
    stripped_name = file_name.replace('file://', '')
    return stripped_name.replace('%20', r' ')


def strip_proxy_for_original_name(proxy_name):
    original_name = proxy_name.replace('_proxy', '')
    original_name = original_name.replace('_Proxy', '')
    return original_name


def remove_proxy_in_path(dirs):
    dir_parts = dirs.split('/')

    if 'proxy' in dir_parts:
        dir_parts.remove('proxy')

    if 'proxies' in dir_parts:
        dir_parts.remove('proxies')

    if 'Proxy' in dir_parts:
        dir_parts.remove('Proxy')

    if 'Proxies' in dir_parts:
        dir_parts.remove('Proxies')

    return r"/".join(dir_parts)


def get_video_list():
    db = db_lite.DBLite(db_file="MEDIA.db", use_dict=True)
    qry = "SELECT `src_path`,`proxy_file` FROM media WHERE `notes`='media-rep'"

    return db.fetch_all(qry)


def main():
    videos = get_video_list()
    # videos = VIDEO_FILES
    total = len(videos)

    # for _file in VIDEO_FILES:ss
    for idx, col in enumerate(videos):

        print("copying {} / {} files . . . ".format(idx + 1, total))
        _file = strip_file_meta(col['src_path'])
        _proxy_file = col['proxy_file']

        file_no_ext = os.path.splitext(_file)
        file_parent_dir = dirname(_file)
        file_name_parts = file_no_ext[0].split("/")
        base_file_name_no_ext = file_name_parts[-1]
        original_file_name = strip_proxy_for_original_name(base_file_name_no_ext)
        original_parent_directory = remove_proxy_in_path(file_parent_dir)
        original_file_name_with_src_path = file_parent_dir + "/" + original_file_name

        # proxy_file, src_path
        if _proxy_file == 1:
            print("Proxy Detected")
            proxy_video_collection = [
                f"{original_parent_directory}/{base_file_name_no_ext}.mov",
                f"{original_parent_directory}/{base_file_name_no_ext}.MOV",
                f"{original_parent_directory}/{base_file_name_no_ext}.mp4",
                f"{original_parent_directory}/{base_file_name_no_ext}.MP4",
                f"{original_parent_directory}/Proxy/{base_file_name_no_ext}.mov",
                f"{original_parent_directory}/Proxy/{base_file_name_no_ext}.MOV",
                f"{original_parent_directory}/Proxy/{base_file_name_no_ext}.mp4",
                f"{original_parent_directory}/Proxy/{base_file_name_no_ext}.MP4",
                f"{original_parent_directory}/proxy/{base_file_name_no_ext}.mov",
                f"{original_parent_directory}/proxy/{base_file_name_no_ext}.MOV",
                f"{original_parent_directory}/proxy/{base_file_name_no_ext}.mp4",
                f"{original_parent_directory}/proxy/{base_file_name_no_ext}.MP4",
                f"{original_parent_directory}/proxies/{base_file_name_no_ext}.mov",
                f"{original_parent_directory}/proxies/{base_file_name_no_ext}.MOV",
                f"{original_parent_directory}/proxies/{base_file_name_no_ext}.mp4",
                f"{original_parent_directory}/proxies/{base_file_name_no_ext}.MP4",
                f"{original_parent_directory}/Proxies/{base_file_name_no_ext}.mov",
                f"{original_parent_directory}/Proxies/{base_file_name_no_ext}.MOV",
                f"{original_parent_directory}/Proxies/{base_file_name_no_ext}.mp4",
                f"{original_parent_directory}/Proxies/{base_file_name_no_ext}.MP4"
            ]

            proxy_file_exists = process_video_collection(proxy_video_collection, PROXY_DIR)

            if not proxy_file_exists:
                print("ERR: {}".format(_file))
                print("FILE DOESN'T Exist!")
                print('_______________________________________________________')
                print(' ')
                MESSAGE['info'].append("FILE DOESN'T EXIST: {}".format(_file))

        original_video_collection = [
            f"{original_parent_directory}/{original_file_name}.mov",
            f"{original_parent_directory}/{original_file_name}.MOV",
            f"{original_parent_directory}/{original_file_name}.mp4",
            f"{original_parent_directory}/{original_file_name}.MP4",
        ]

        original_file_exists = process_video_collection(original_video_collection, ORIG_DIR)

        if not original_file_exists:
            print("ERR: {}".format(original_file_name_with_src_path))
            print("FILE DOESN'T Exist!")
            print('_______________________________________________________')
            print(' ')

    print("PROCESS COMPLETE")
    print(" ")
    print(
        f"{len(MESSAGE['success'])} / {total} files successfully copied | {len(MESSAGE['error'])} files had errors | {len(MESSAGE['warning'])} warnings found")

    print(" ")
    if len(MESSAGE['error']) > 0:
        print("ERRORS:")
        for err in MESSAGE['error']:
            print("   {}".format(err))

    if len(MESSAGE['warning']) > 0:
        print("WARNINGS:")
        for warn in MESSAGE['warning']:
            print("   {}".format(warn))
        print(" ")


if __name__ == '__main__':
    print(" ")
    print("Starting Hi-Res-Proxy Copying . . . ")
    print(" ")
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
    print(" ")
    print("_______________________________________________________")
    print(" ")
    print(". . . Completed Hi-Res-Proxy  Copying")
    print(" ")
    print("GOOD BYE!")
    print(" ")
    print(" ")
