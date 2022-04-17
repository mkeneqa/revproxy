import os.path
import xml.etree.ElementTree as ET
from moviepy.editor import VideoFileClip
import reverse_proxy_workflow as wflow
from timecode import Timecode
from moviepy.editor import VideoFileClip
from utils.ffmpeg_class import FFMpeg
import pathlib


def frames_to_timecode(fn: float, frame_rate: float):
    ff = fn % frame_rate
    s = fn // frame_rate
    # HH,MM,SS,FF
    return int(s // 3600), int(s // 60 % 60), int(s % 60), int(ff)


# Converts the '64bit/32bits' timecode format into seconds
def parse_fcp_time_seconds(time_str, fps):
    vals = [float(n) for n in time_str.replace('s', '').split('/')]
    if 1 == len(vals):
        seconds = vals[0]
    else:
        seconds = vals[0] / vals[1]
    val = (seconds - int(seconds)) * fps

    return val


def get_clean_name(name, new_extension=None):
    name = name.replace("_Proxy", "")
    name = name.replace("_proxy", "")
    if new_extension is not None:
        # uppercase extension
        split = name.split(".")
        name = split[0] + "." + new_extension
    return name


class Clip:

    def start_time(self):
        pass

    def end_time(self):
        pass

    def duration(self):
        pass


class FcpXmlLoader:
    # https://www.datacamp.com/community/tutorials/python-xml-elementtree
    def __init__(self, fcp_file):
        self.source_location = r''
        self.dest_location = r''
        self._file = fcp_file
        self.tree = ET.parse(self._file)
        self.xml_root = ET.parse(fcp_file).getroot()
        self.config = wflow.load_config()
        self.clips_collection = {}

    def _get_unique_clip_name(self, clip_name):
        new_clip_name = clip_name
        # search if keuy already exists in collection
        # found = [f for f in self.clips_collection if f.get(clip_name)]
        if self.clips_collection.get(clip_name) is not None:
            # i = found + 1
            self.clips_collection[clip_name].append(True)
            new_clip_name = clip_name + "_" + str(len(self.clips_collection[clip_name]) - 1)
        else:
            # newly added to collection
            self.clips_collection[clip_name] = [True]

        return new_clip_name

    def _calculate_end_timecode(self, start_time, duration, fps):
        # find end time
        pass

    def print_ffmpeg_cmd(self, start_time, clip_name, duration_time):
        new_clip_name = self._get_unique_clip_name(clip_name)
        cmd = [
            f"ffmpeg -ss {str(start_time)}",
            f"-i {self.source_location}/{clip_name}.mov",
            f"-vcodec prores -profile:v 0 -acodec pcm_s16le -to {duration_time}",
            f"-c copy {self.dest_location}/{new_clip_name}.mov"
        ]

        print(str(" ".join(cmd)))

    def export_timeline_clips_metadata(self):
        print_once = True
        for rsrc in self.xml_root.findall("./library/event/project/sequence/spine/asset-clip"):
            # print(str(rsrc))

            duration_frames = rsrc.attrib['duration'][:-1]
            clip_name = rsrc.attrib['name']
            start_frames = rsrc.attrib['start'][:-1]

            cr_node = rsrc.find('conform-rate')
            fps = cr_node.attrib['srcFrameRate']

            # float(24) * (1000.0 / 1001)
            x, y = duration_frames.split('/')
            frames_duration = float(fps) * (int(x) / int(y))
            hh, mm, ss, ff = frames_to_timecode(frames_duration, float(fps))
            duration_tc = Timecode(float(fps), f"{hh}:{mm}:{ss}.{ff}")

            try:
                x, y = start_frames.split('/')
            except ValueError as e:
                x = start_frames.split('/')[0]
                y = 1

            starting_frames = float(fps) * (int(x) / int(y))
            hh, mm, ss, ff = frames_to_timecode(starting_frames, float(fps))
            starting_tc = Timecode(float(fps), f"{hh}:{mm}:{ss}.{ff}")

            end_tc = starting_tc + duration_tc

            clip_name = clip_name.replace("_Proxy", '')
            clip_name = clip_name.replace(".mov", '')
            self.print_ffmpeg_cmd(start_time=starting_tc, duration_time=duration_tc, clip_name=clip_name)

    def load(self):
        # tree = self.tree
        # root = tree.getroot()
        # [elem.tag for elem in root.iter()]
        # for rsrc in root.findall("./resources/format[@width]"):
        #     print(rsrc.attrib['id'])
        #     rsrc.set('width', '3500')
        #     rsrc.set('height', '4500')

        # full_res_path = r"file:///Users/mainuser/Movies/Soccer/FullRes"

        # for rsrc in root.findall("./resources/asset"):
        #     print(str(rsrc.attrib))

        # print("sig, kind, old_source, new_source")
        count = 1
        for rsrc in self.xml_root.findall("./resources/asset[@hasVideo='1']/media-rep"):
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
