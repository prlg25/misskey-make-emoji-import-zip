"""ディレクトリ内の画像ファイルからmeta.jsonを作成し、まとめてインポートする"""
import json
import zipfile
import argparse
from pathlib import Path

import yaml
import pykakasi
import re

kunrei2hepburn = [
    {
        r'sya': 'sha',
        r'si': 'shi',
        r'syu': 'shu',
        r'sye': 'she',
        r'syo': 'sho',
    },
    {
        r'zzya': 'jja',
        r'zzi': 'jji',
        r'zzyu': 'jju',
        r'zzye': 'jje',
        r'zzyo': 'jjo',
        r'zya': 'ja',
        r'zi': 'ji',
        r'zyu': 'ju',
        r'zye': 'je',
        r'zyo': 'jo',
    },
    {
        r'ttya': 'ccha',
        r'tti': 'cchi',
        r'ttyu': 'cchu',
        r'ttye': 'cche',
        r'ttyo': 'ccho',
        r'tya': 'cha',
        r'ti': 'chi',
        r'tyu': 'chu',
        r'tye': 'che',
        r'tyo': 'cho',
    },
    {
        r'tu': 'tsu',
    },
    {
        r'ffu': 'hhu',
        r'fu': 'hu',
    }
]

def read_emoji_info_text(text_file_path):
    with open(text_file_path, "r", encoding="utf-8") as f:
        loaded_yaml = yaml.safe_load(f)
        # print(loaded_yaml)
    return loaded_yaml

def replace_from_dict(input_string:str, replacement_patterns:dict):
    for pattern, replacement in replacement_patterns.items():
        input_string = re.sub(pattern, replacement, input_string)
        # print(input_string)
    return input_string

def generate_tag_text_from_hiragana(hiragana_text):
    kks = pykakasi.kakasi()
    tag_set = set()
    hiragana_text = hiragana_text.replace("ー", "-")
    hiragana_text = re.sub(r"(っ|ッ)(ぢ|ヂ)", "ddi", hiragana_text)
    hiragana_text = re.sub(r"(ぢ|ヂ)", "di", hiragana_text)
    hiragana_text = re.sub(r"(っ|ッ)(づ|ヅ)", "ddu", hiragana_text)
    hiragana_text = re.sub(r"(づ|ヅ)", "du", hiragana_text)
    # hiragana_text = hiragana_text.replace("ー", "-")
    result = kks.convert(hiragana_text)
    print(result)
    kunrei_text = ""
    for each in result:
        kunrei_text += each["kunrei"]
    tag_set.add(kunrei_text)
    print(tag_set)
    for each_pattern in kunrei2hepburn:
        append_text_list = []
        for each_text in tag_set:
            append_text_list.append(replace_from_dict(each_text, each_pattern))
        # print(each_pattern)
        # print(append_text_list)
        for each in append_text_list:
            tag_set.add(each)
    print(tag_set)
    return list(tag_set)


def main():
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=Path, required=True)
    parser.add_argument('--yamlpath', type=Path, required=False)
    args = parser.parse_args()
    
    # JSON作成
    emojis_list = []
    datadir = args.datadir
    filename_list = ["*.png", "*.gif", "*.jpg", "*.apng", "*.webp"] # 新しいファイル種別出てきたら追加する
    for fname in filename_list:
        for each_path in datadir.glob(fname):

            filename = each_path.name
            emojiname = each_path.stem
            each_json = {
                "downloaded": True,
                "fileName": filename,
                "emoji": {
                    "name": emojiname,
                    "category": None,
                    "aliases": []
                }
            }
            emojis_list.append(each_json)

    if args.yamlpath:
        # ファイル読み込み
        print("絵文字情報をロードします")
        loaded_emojiinfo = read_emoji_info_text(args.yamlpath)
        # print(loaded_emojiinfo)
        # each_jsonについて、fileNameがyamlに含まれる場合、
        for i, each_json in enumerate(emojis_list):
            print(f'{each_json["emoji"]["name"]}を処理中')
            if each_json["emoji"]["name"] in loaded_emojiinfo.keys():
                each_emojiinfo = loaded_emojiinfo[each_json["emoji"]["name"]]
                tag_text = []
                if each_emojiinfo["読み仮名"]:
                    yomigana_list = each_emojiinfo["読み仮名"].split(",")            
                    for yomigana in yomigana_list:
                        # 読み仮名のテキストからタグを生成
                        tag_text.extend(generate_tag_text_from_hiragana(yomigana))
                        # 読み仮名をタグに追加
                        tag_text.append(yomigana)
                if each_emojiinfo["テキスト"]:
                    # テキストをタグに追加
                    text_tags = str(each_emojiinfo["テキスト"]).split(",")
                    removed_blank_text_tags = []
                    for each in text_tags:
                        removed_blank_each = re.sub(r"( |　)", "", each)
                        removed_blank_text_tags.append(removed_blank_each)
                    # tag_text.extend(str(each_emojiinfo["テキスト"]).split(","))
                    tag_text.extend(removed_blank_text_tags)
                # その他つけたいタグがあればタグに追加
                if each_emojiinfo["その他つけたいタグ"]:
                    other_tags = str(each_emojiinfo["その他つけたいタグ"]).split(",")
                    removed_blank_other_tags = []
                    for each in other_tags:
                        removed_blank_other_each = re.sub(r"( |　)", "", each)
                        removed_blank_other_tags.append(removed_blank_other_each)
                    # tag_text.extend(str(each_emojiinfo["その他つけたいタグ"]).split(","))
                    tag_text.extend(removed_blank_other_tags)
                # 重複削除
                tag_text = sorted(set(tag_text), key=tag_text.index)
                emojis_list[i]["emoji"]["aliases"] = tag_text
                # カテゴリがあればカテゴリを追加
                if each_emojiinfo["カテゴリ名"]:
                    emojis_list[i]["emoji"]["category"] = each_emojiinfo["カテゴリ名"]
    
    output_base_json = {
        "emojis": emojis_list
    }
    # meta.json出力
    with open(datadir.joinpath("meta.json"), "w", encoding="utf-8") as f:
        json.dump(output_base_json, f, ensure_ascii=False)

    # zip出力
    zipfile_path = datadir.joinpath("import_zipfile.zip")
    filename_list.append("meta.json")

    with zipfile.ZipFile(zipfile_path, 'w') as zf:
        for fname in filename_list:
            for each_path in datadir.glob(fname):
                zf.write(each_path, arcname=each_path.name)


if __name__ == "__main__":
    main()
