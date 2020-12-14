import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import db_lite


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
        row = (None, node.attrib['sig'], node.attrib['kind'], name_ext[1], name_ext[0], full_path, node.tag, within_fcp, proxy_file)
        rows.append(row)

    _db.insert_many_into(rows)


if __name__ == '__main__':
    db = db_lite.DBLite('javen5.db')
    tree = ET.parse('WIP_Javen_Year5_1920x960.fcpxml')
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
