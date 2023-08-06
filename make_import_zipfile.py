"""ディレクトリ内の画像ファイルからmeta.jsonを作成し、まとめてインポートする"""
import json
import zipfile
import argparse
from pathlib import Path


def main():
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=Path, required=True)
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

    output_base_json = {
        "emojis": emojis_list
    }
    # meta.json出力
    with open(datadir.joinpath("meta.json"), "w") as f:
        json.dump(output_base_json, f)

    # zip出力
    zipfile_path = datadir.joinpath("import_zipfile.zip")
    filename_list.append("meta.json")

    with zipfile.ZipFile(zipfile_path, 'w') as zf:
        for fname in filename_list:
            for each_path in datadir.glob(fname):
                zf.write(each_path, arcname=each_path.name)


if __name__ == "__main__":
    main()
