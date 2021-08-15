import re
import xml.etree.ElementTree as ET
from utils import db_lite
from datetime import datetime


def term_in_file(search_term, full_path):
    parts = full_path.split('/')
    path_string = " ".join(parts)
    if str(search_term).lower() in str(path_string).lower():
        return 1
    else:
        return 0


def get_file_name_ext_from_source(full_path: str):
    parts = full_path.split('/')
    name_ext = parts[len(parts) - 1]
    return name_ext.split('.')


def parse_asset_nodes(_db: db_lite.DBLite, _nodes: list):
    rows = []
    for node in _nodes:
        # [(UID, kind, file_ext, file_name, src, notes, within_fcp, proxy_file)]
        row = (None, node.attrib['uid'], '', '', node.attrib['name'], '', node.tag, '', '')
        rows.append(row)

    _db.insert_many_into(rows)


def parse_media_nodes(_db: db_lite.DBLite, _nodes: list):
    rows = []
    for node in _nodes:
        # uid,kind,file_ext,file_name,src_path, notes
        full_path = node.attrib['src']
        name_ext = get_file_name_ext_from_source(full_path)
        proxy_file = term_in_file('_proxy', full_path)
        within_fcp = term_in_file('.fcpbundle', full_path)
        # [(UID, kind, file_ext, file_name, src, notes, within_fcp, proxy_file)]
        row = (None, node.attrib['sig'], node.attrib['kind'], name_ext[1], name_ext[0], full_path, node.tag, within_fcp,
               proxy_file)
        rows.append(row)

    _db.insert_many_into(rows)


def save_to_db():
    db = db_lite.DBLite('mymedia.db')
    tree = ET.parse('WIP_Year5_1920x960.fcpxml')
    root = tree.getroot()
    media_dict = {}
    media_list = []
    # print(root)
    nodes = root.findall(".")
    asset_nodes = root.findall("./resources/asset")
    media_rep_nodes = root.findall("./resources/asset/media-rep")

    parse_asset_nodes(db, asset_nodes)
    parse_media_nodes(db, media_rep_nodes)

    db.close_conn()


def read_update_file():
    filename = "MIKE_EXPORT_TEST.fcpxml"
    data = []
    with open(filename, 'r') as file:
        d = file.read().split("\n")
        # data = list(filter(None, d.strip()))
        for line in d:
            # data = list(filter(None, line.strip()))
            if line:
                data.append(line)

    for idx, line in enumerate(data):
        if '<media-rep' in line and 'src=' in line:
            str_replace = re.search('src="(.*)', line)
            # print(str_replace.group(1))
            str_replace = str_replace.group(1)
            str_replace = str_replace.replace('">', '')
            if str_replace:
                file_path = line.split("/")
                video_file_name = file_path[-1].replace('">', '')
                video_file_name = video_file_name.replace('-_proxy', '')
                video_file_name = video_file_name.replace('-_Proxy', '')
                video_file_name = video_file_name.replace('_proxy', '')
                video_file_name = video_file_name.replace('_Proxy', '')
                new_location = f'/Volumes/SEAGTE/FullRes/media/originals/{video_file_name}'
                new_str = line.replace(str_replace, new_location)
                data[idx] = new_str

    now = datetime.now()
    now_ts = now.strftime("%d%m%Y%H%M%S")
    xml_str = "".join(data)
    # tree = ET.ElementTree(ET.fromstring(xml_str))
    # ET.tostring(tree)).toprettyxml(indent="   ")
    # pretty = ET.ElementTree.tostring(tree, encoding="unicode", pretty_print=True)
    # root = ET.fromstring(xml_str)
    # pretty = ET.tostring(tree, print())
    ET.tostring(ET.fromstring(xml_str))
    f = open(f"NEW_MODD_{now_ts}.fcpxml", "x")
    f.write(xml_str)
    f.close()


def parse_and_update_src():
    tree = ET.parse('WIP_FINAL_EXPORT_MIKEDIT.fcpxml')
    root = tree.getroot()
    nodes = root.findall(".")
    asset_nodes = root.findall("./resources/asset")
    media_rep_nodes = root.findall("./resources/asset/media-rep")

    # for e in media_rep_nodes.iter("attrib"):
    #     print(f"{e}")
    # asset_clip_node =


if __name__ == '__main__':
    # save_to_db()
    # parse_and_update_src()
    try:
        read_update_file()
    except Exception as e:
        print("ERROR: {e}")

    # for asset in root.findall('asset'):
    #     for media in asset.findall('media-rep'):
    #         media_kind = media.get('kind')
    #         media_src = media.get('src')
    #         media_uid = media.get('sig')
    #
    #         media_dict = {
    #             "media_kind": media_kind,
    #             "media_src": media_src,
    #             "uid": "1234",
    #             "ext": "mp4",
    #             "is_proxy": True,
    #
    #
    #         }
