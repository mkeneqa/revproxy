import json
import os

import utils.consolidate_media as CMedia
from prodict import Prodict
# from bs4 import BeautifulSoup
from utils.fcpxml_loader import FcpXmlLoader


class Config(Prodict):
    project_location: str
    fcpxml_file: str
    proxy_location: str
    full_res_location: str
    copy_full_res_to_project_location: int
    reorg_proxies: int
    lowercase_exts: int
    export_new_fcpxml: int


def load_config():
    try:
        f = open('config.json', )
        config_json = json.load(f)
        f.close()
        my_config: Config = Config.from_dict(config_json)
        return my_config
    except Exception as e:
        print(f"ERR: {e}")
        return False


class ReverseProxyWorkflow:
    my_config: Config
    clip_collection = []

    @staticmethod
    def hello():
        print('Hello RProxy Class Reached!')

    def __init__(self):
        if not self._read_config():
            print("ERR: Please Check Config File")

    def run(self):
        export_new_fcpxml = False
        if self.my_config.export_new_fcpxml == 1:
            export_new_fcpxml = True

        self._parse_xml_file(export_new_fcpxml)

        if self.my_config.copy_full_res_to_project_location == 1:
            print("Copying Full Resolution Files ...")
            self._copy_full_res_files()

        if self.my_config.reorg_proxies == 1:
            print("Reorganizing Proxies ...")
            self._reorg_proxy_files()

        if self.my_config.lowercase_exts == 1:
            print("Convert Extensions To Lowercase ...")
            self._change_extensions_to_lowercase()

        print("Reverse Proxy Operations Complete!")
        print("Good Bye =) ")

    def _clip_pairing(self, line):
        clip_pair = {
            'full_res': '',
            'proxy': ''
        }
        bs_content = BeautifulSoup(line, "lxml")
        # parser strips out `clip-asset` so just use `asset` tag
        result = bs_content.find('asset')
        if result:
            clip_name = result.attrs['name']
            if 'proxy' in clip_name.lower():
                clip_pair['proxy'] = clip_name
                video_name = clip_name.replace('_Proxy', '')
                if '.mp4' in video_name:
                    video_name = video_name.replace('.mp4', '.MP4')
                clip_pair['full_res'] = video_name
                self.clip_collection.append(clip_pair)

    def _copy_full_res_files(self):
        if self.clip_collection:
            full_res_clips = [x['full_res'] for x in self.clip_collection]
            for root, dirs, files in os.walk(self.my_config.full_res_location):
                for name in files:
                    # ignore file extension
                    name_no_ext = name.split(".")[0]
                    found = [x for x in full_res_clips if x == name_no_ext]
                    if found:
                        src_file = os.path.join(root, name)
                        dest_file = os.path.join(self.my_config.project_location, name)
                        if not os.path.exists(dest_file):
                            CMedia.copy_media(src_file, dest_file)

    def _reorg_proxy_files(self):
        files = [f for f in os.listdir(self.my_config.project_location) if '_Proxy' in f]
        if files:
            for file in files:
                old_file_location = os.path.join(self.my_config.project_location, file)
                new_file_location = os.path.join(self.my_config.proxy_location, file)
                CMedia.move_file_to_dir(old_file_location, new_file_location)

    def _change_extensions_to_lowercase(self):
        files = [f for f in os.listdir(self.my_config.project_location) if 'MP4' in f]
        if files:
            for file in files:
                old_file = os.path.join(self.my_config.project_location, file)
                new_file = file.replace('.MP4', '.mp4')
                new_file = os.path.join(self.my_config.project_location, new_file)
                os.rename(old_file, new_file)

    def _parse_xml_file(self, export_file=False):

        xml_file = os.path.join(self.my_config.project_location, self.my_config.fcpxml_file)
        content = []

        fcp_reader = FcpXmlLoader(xml_file)
        fcp_reader.load()

        # tree = ET.parse(xml_file)
        # root = tree.getroot()
        #
        # for child in root:
        #     print(child.tag, child.attrib)
        #
        # xml_doc = parse(xml_file)
        # asset_list = xml_doc.getElementsByTagName('asset')
        #
        # with open(xml_file, 'r') as _file:
        #     # data = f.read()
        #     content = _file.readlines()
        #     content = "".join(content)
        #     tree = tree
        #     bs_content = BeautifulSoup(content, "lxml")
        #     results = bs_content.find('asset')
        #     # print('taddaa')
        # # bs_content = BeautifulSoup(line, "lxml")
        # # result = bs_content.find('asset')
        #
        # new_content = []
        # video_asset = False
        # video_asset = False
        # for line in content:
        #     if '<asset' in line:
        #         bs_content = BeautifulSoup(line, "lxml")
        #         result = bs_content.find('asset')
        #     elif 'width="1280"' in line:
        #         new_line = line.replace('width="1280"', 'width="3840"')
        #         new_content.append(new_line.replace('height="720"', 'height="2160"'))
        #
        #     elif "_proxy" in line.lower():
        #         new_content.append(line.replace("_Proxy", ""))
        #
        #     elif '<media-rep kind="original-media"' in line:
        #         pass

        # elif 'hasVideo="1"' in line:
        #     video_asset = True
        #     new_content.append(line.replace("_Proxy", ""))
        #     self._clip_pairing(line)
        # elif 'width="1280"' in line:
        #     # 3840 × 2160
        #     new_line = line.replace('width="1280"', 'width="3840"')
        #     new_content.append(new_line.replace('height="720"', 'height="2160"'))
        # else:
        #     new_content.append(line)

        if export_file:
            new_xml_file = os.path.join(self.my_config.project_location, 'converted.fcpxml')
            with open(new_xml_file, "w") as _file:
                _file.writelines(new_content)

            print("XML CONVERTED!")

    def _read_config(self):
        try:
            f = open('config.json', )
            config_json = json.load(f)
            f.close()
            self.my_config: Config = Config.from_dict(config_json)
            return True
        except Exception as e:
            print(f"ERR: {e}")
            return False
