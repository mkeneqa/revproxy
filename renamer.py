import os
from os import listdir
from os.path import isfile, join


def main():
    PROXY = '_Proxy'
    mypath = r"/Volumes/TO/MY/FCPProject.fcpbundle/Sequences/Original Media"
    all_files = listdir(mypath)
    msg = {
        'pass': [],
        'fail': []
    }

    for afile in all_files:
        if PROXY in afile:
            print(f"OLD FILE: {afile}")
            new_file = afile.replace(PROXY, '')
            print(f"NEW FILE: {new_file}")
            print('')
            src = rf"{mypath}/{afile}"
            dst = rf"{mypath}/{new_file}"
            try:
                os.rename(src, dst)
                print('SUCCESS!')
                msg['pass'].append(f'Success: {src} ==> {dst}')
            except Exception as e:
                print('FAILED!')
                err = f"Check File: {src}. Error:{e}"
                print(f"{err}")
                msg['fail'].append(err)
            finally:
                print('')

    print("_____ SUMMARY _____")
    total = len(msg['pass']) + len(msg['fail'])
    print(f"TOTAL: {total} | {len(msg['pass'])} PASSED | {len(msg['fail'])} FAILED")

    print('')
    print('')

    if len(msg['pass']) > 0:
        print("PASS:")
        for note in msg['pass']:
            print(note)

    print('')
    print('')

    if len(msg['fail']) > 0:
        print("FAIL:")
        for note in msg['fail']:
            print(note)

    print('')


if __name__ == '__main__':
    main()
