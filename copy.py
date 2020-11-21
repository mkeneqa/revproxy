import os.path
from os import path
from shutil import copyfile
import hashlib


VIDEO_FILES = [
    "//Volumes/Cinematography/FOOTAGE/2018/OnstreamChristmasParty/P1110149-ProRes-422-LakeLouiseOnstream",
    "//Volumes/Cinematography/FOOTAGE/2018/OnstreamChristmasParty/P1110164-ProRes-422-LakeLouiseOnstream",
    "//Volumes/Cinematography/FOOTAGE/2018/OnstreamChristmasPartier/P1110229-ProRes-422-LakeLouiseOnstream"]


def get_dest_file_path(full_file_path):
    file_name = os.path.basename(full_file_path)
    # dest_dir = "//Volumes/DESKSTAR/JavenFullRes"
    dest_dir = os.getcwd()
    return "{}/{}".format(dest_dir, file_name)


def file_exists_in_dest(dest_file_path):
    if path.exists(dest_file_path):
        return True
    else:
        return False


def get_file_checksum(file_path):
    md5_check = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(900000000), b""):
            md5_check.update(chunk)
    return md5_check.hexdigest()


def test():
    pass


def main():
    success_count = 0
    error_count = 0
    warning_count = 0
    total = len(VIDEO_FILES)
    error_info = []
    warning_info = []

    for _file in VIDEO_FILES:

        file_count = error_count + success_count + 1
        print("copying {} / {} files".format(file_count, total))

        mov_file = "{}.mov".format(_file)
        mov2_file = "{}.MOV".format(_file)
        mp4_file = "{}.mp4".format(_file)
        mp42_file = "{}.MP4".format(_file)

        src_file_path = False

        if path.exists(mov_file):
            src_file_path = mov_file
        elif path.exists(mov2_file):
            src_file_path = mov2_file
        elif path.exists(mp4_file):
            src_file_path = mp4_file
        elif path.exists(mp42_file):
            src_file_path = mp42_file
        else:
            error_count = error_count + 1
            print("ERR: {}".format(_file))
            print("FILE DOESN'T Exist!")
            print('_______________________________________________________')
            print(' ')
            error_info.append("FILE DOESN'T EXIST: {}".format(_file))

        if src_file_path:
            dest_file_path = get_dest_file_path(src_file_path)
            if file_exists_in_dest(dest_file_path):
                msg = "SKIPPING, File Already Copied: {}".format(dest_file_path)
                warning_info.append(msg)
            else:
                try:
                    print("source checksum ...")
                    src_checksum = get_file_checksum(src_file_path)
                    copyfile(src_file_path, dest_file_path)

                    print("copied from: {} to: {}".format(src_file_path, dest_file_path))

                    print("destination checksum ...")
                    dest_checksum = get_file_checksum(dest_file_path)

                    checksum_msg = 'Checksums MATCH: {}'.format(src_checksum)
                    if src_checksum != dest_checksum:
                        checksum_msg = 'WARNING: Checksums DO NOT MATCH! {} != {}'.format(src_checksum, dest_checksum)
                        warning_info.append(checksum_msg)

                    print(checksum_msg)
                    print('_______________________________________________________')
                    print(" ")

                    success_count = success_count + 1

                except Exception as e:
                    print("ERR: Could Not Copy File! {}".format(str(e)))
                    print("ERR SRC File: {}".format(src_file_path))
                    print("ERR DEST File: {}".format(src_file_path))
                    print('_______________________________________________________')
                    print('')
                    error_info.append("Could Not Copy File! {}".format(str(e)))
                    error_count = error_count + 1

    print("PROCESS COMPLETE")
    print(" ")
    print("{} / {} files successfully copied.  | {} files had errors | {} warnings found ".
          format(success_count, total, len(error_info), len(warning_info)))

    print(" ")
    if len(warning_info) > 0:
        print("WARNINGS:")
        for warn in warning_info:
            print("   {}".format(warn))
        print(" ")

    if len(error_info) > 0:
        print("ERRORS:")
        for err in error_info:
            print("   {}".format(err))


if __name__ == '__main__':
    print("Starting Full-Res Copying . . . ")
    # main()
    print(" ")
    print("_______________________________________________________")
    print(" ")
    print("COMLEPETED Full-Res Copying")
    print(" ")
    print("GOOD BYE!")
    print(" ")
    print(" ")
