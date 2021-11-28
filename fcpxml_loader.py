import os
import xml.etree.ElementTree as ET
from moviepy.editor import VideoFileClip
import reverse_proxy_workflow as wflow


def get_clean_name(name, new_extension=None):
    name = name.replace("_Proxy", "")
    name = name.replace("_proxy", "")
    if new_extension is not None:
        # uppercase extension
        split = name.split(".")
        name = split[0] + "." + new_extension
    return name


class FcpXmlLoader:
    # https://www.datacamp.com/community/tutorials/python-xml-elementtree
    def __init__(self, fcp_file):
        self._file = fcp_file
        self.tree = ET.parse(self._file)
        self.config = wflow.load_config()

    def load(self):
        tree = self.tree
        root = tree.getroot()
        # [elem.tag for elem in root.iter()]
        # for rsrc in root.findall("./resources/format[@width]"):
        #     print(rsrc.attrib['id'])
        #     rsrc.set('width', '3500')
        #     rsrc.set('height', '4500')

        full_res_path = r"file:///Users/mainuser/Movies/Soccer/FullRes"

        # for rsrc in root.findall("./resources/asset"):
        #     print(str(rsrc.attrib))

        print("sig, kind, old_source, new_source")
        count = 1
        for rsrc in root.findall("./resources/asset[@hasVideo='1']/media-rep"):
            if rsrc.attrib['kind'] == 'original-media':
                media_file = get_clean_name(os.path.basename(rsrc.attrib['src']), new_extension="MP4")
                new_file_path = os.path.join(full_res_path, media_file)
                clip = VideoFileClip(new_file_path)
                old_clip_duration = 0
                time_denom = 0
                # print(clip.duration)
                new_clip_duration = clip.duration
                uid = rsrc.attrib['sig']
                asset_id = -1
                old_src = rsrc.attrib['src']
                asset = root.find(f"./resources/asset[@uid='{uid}']")
                if asset:
                    asset_id = asset.attrib['id']
                    t = asset.attrib['duration']
                    splits = t.split("/")
                    old_clip_duration = splits[0]
                    time_denom = splits[1][:-1]
                    new_clip_duration = clip.duration * int(time_denom)  # remove the s
                    asset.set('duration', f"{int(new_clip_duration)}/{time_denom}s")

                rsrc.set('src', new_file_path)
                print(str({'itr': count,
                           "asset_id": asset_id,
                           'uid': uid,
                           'old_src': old_src,
                           'new_src': str(new_file_path),
                           'new_time': int(new_clip_duration),
                           'old_time': int(old_clip_duration),
                           'time_denom': time_denom
                           }))
                count += 1

        # remove all proxy media
        for node in root.findall("./resources/asset[@hasVideo='1']/media-rep[@kind='proxy-media']"):
            # root.remove(node)
            print(f"Delete Proxy Media @ {node.attrib['sig']}")

        names = root.findall(".//*[@name]")
        for node in names:
            if 'proxy' in str(node.attrib['name']).lower():
                node.set('name', get_clean_name(node.attrib['name']))

        # if 'name' in child.attrib and 'proxy' in str(child.attrib['name']).lower():
        #     child.set('name', get_clean_name(child.attrib['name']))
        # for parent in root:
        #     if parent.tag == 'resources':
        #         for child in parent.findall("./format[@width='1920']"):
        #             child.set('width', '3500')
        #             child.set('height', '4500')

        tree.write(os.path.join(self.config.project_location, 'soccer_import.fcpxml'))
        print("FCPXML Completed")

    def load_resources(self, resources_tag):
        # r = [elem.tag for elem in resources_tag.iter()]
        for parent in resources_tag.findall("./format[@width='1920']"):
            parent.set('width', '3500')
            parent.set('height', '4500')

        resources_tag.write('mike_test.xml')
        print("TEST WRITTEN")
        # videos = resources_tag.findall("./asset[@hasVideo='1']")
        # for parent in resources_tag.findall("./asset[@hasVideo='1']"):
        #     for child in parent:
        #         print(child)
        # child.set()
        # if child.attrib:
        #     if 'width' in child.attrib and 'height' in child.attrib:
        #         print(str(child.attrib["width"]), str(child.attrib["height"]))
        #     print(child.tag, child.attrib)
