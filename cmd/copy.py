import os

from cleo import Command
import utils.consolidate_media as CMedia


class CopyCommand(Command):
    """
    Executes a Reverse Proxy Command

    copy
    """

    def handle(self):
        _clips = [
            "00000-ProRes-422-Proxy-GH2-CEREMONY.mp4",
            "00003.mp4",
            "00005.mp4",
            "00009.mp4",
            "00016-Ceremony.mp4",
            "00016.mp4",
            "00017-Ceremony.mp4",
            "00018.mp4",
            "00020.mp4",
            "00021-ProRes-422-Proxy-GH2-CEREMONY.mp4",
            "00021.mp4",
            "00024.mp4",
            "00026 2.mp4",
            "00026.mp4",
            "00027 2.mp4",
            "00027.mp4",
            "00029.mp4",
            "00030.mp4",
            "00033.mp4",
            "00046-ProRes-422-Proxy-GH2-CEREMONY.mp4",
            "00046-ProRes-422-Proxy-GH2-CEREMONY_proxy.mp4",
            "P1033517-ProRes-422-Proxy-GH5-CRANE-CEREMONY_proxy.mp4",
            "P1033532-ProRes-422-Proxy-GH5-CRANE-LIFESTYLE_proxy.mp4",
            "P1033550-ProRes-422-Proxy-GH5-CRANE-LIFESTYLE_proxy.mp4",
            "P1033572-ProRes-422-Proxy-GH5-CRANE-RECEPTION_proxy.mp4",
            "P1033573-ProRes-422-Proxy-GH5-CRANE-RECEPTION_proxy.mp4",
            "P1090791-ProRes-422-Proxy-GH4-SIGMA-CEREMONY_proxy.mp4",
            "P1090793-ProRes-422-Proxy-GH4-SIGMA-CEREMONY_proxy.mp4",
            "P1090796-ProRes-422-Proxy-GH4-SIGMA-CEREMONY_proxy.mp4",
            "P1100034-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100036-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100037-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100038-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100039-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100049-ProRes-422-Proxy-GH4-SIGMA-LIFESTYLE_proxy.mp4",
            "P1100077-ProRes-422-Proxy-GH4-SIGMA-RECEPTION_proxy.mp4",
            "P1100078-ProRes-422-Proxy-GH4-SIGMA-RECEPTION_proxy.mp4",
            "P1100096-ProRes-422-Proxy-GH4-SIGMA-RECEPTION_proxy.mp4",
            "P1133564_NR_proxy.mp4",
            "P1133633_NR_proxy.mp4",
            "P1133634_NR_proxy.mp4",
            "P5010184-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010225-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010226-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010232-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010246-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010247-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010249-ProRes-422-GH4-SIGMA_proxy.mp4",
            "P5010251-ProRes-422-GH4-SIGMA_proxy.mp4",
            "SE_WDG_DJI_0078_proxy.mp4",
            "SE_WDG_DJI_0079_proxy.mp4",
            "SE_WDG_DJI_0090_proxy.mp4",
            "SE_WDG_DJI_0092_proxy.mp4",
            "SE_WDG_P1000681_proxy.mp4",
            "SE_WDG_P1000685_proxy.mp4",
            "SE_WDG_P1000686_proxy.mp4",
            "SE_WDG_P1000688_proxy.mp4",
            "SE_WDG_P1000693_proxy.mp4",
            "SE_WDG_P1000694_proxy.mp4",
            "SE_WDG_P1000696_proxy.mp4",
            "SE_WDG_P1000706_proxy.mp4",
            "SE_WDG_P1000716_proxy.mp4"
        ]

        clips = [str(c).split('.')[0].split('_proxy')[0] for c in _clips]
        clips_count = len(clips)

        dest = "/Users/mkeneqa/Movies/PerhapsLove/FullRes"
        search_dirs = ['/Volumes/KENETICMEDIA/']
        bad_exts = ['jpg', 'jpeg', 'ds_store', 'txt', "lpmd"]
        searchables = ['.mp4', '.mov', '.MP4', '.MOV']
        clips_not_found = []
        for _dir in search_dirs:
            for root, dirs, files in os.walk(_dir):
                # found = [f for f in files if [c for c in clips if c in files] and "proxy" not in f]
                if files:
                    for f in files:
                        try:
                            name_no_ext, ext = os.path.splitext(f)
                            if ext in searchables:
                                found = [x for x in clips if x.lower() == name_no_ext.lower()
                                         and "_proxy" not in name_no_ext.lower()
                                         and ext.lower() not in bad_exts]

                                if found:
                                    src_file = os.path.join(root, f)
                                    dest_file = os.path.join(dest, f)
                                    print("File Found: " + src_file)
                                    if os.path.exists(dest_file):
                                        print(str(f) + ' in dest - skipping ... ')
                                    else:
                                        CMedia.copy_media(src_file, dest_file)
                                    # remove item from list
                                    clips.remove(found[0])
                                    print(len(clips), "clips remain")
                        except Exception as e:
                            print("ERR: " + str(e), "| file: " + str(f))

        if len(clips) > 0:
            print(f"{len(clips)} clips were not found ...")
            for c in clips:
                print(str(c))
