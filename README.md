# misskey-make-emoji-import-zip
Misskeyのカスタム絵文字をバルクインポートするためのZIPファイルを作成するスクリプト

## 環境
- Python3.11(古いバージョンでも動くかもですが動作確認してないです)
- Windows11(他のOSでも動くと思いますが動作確認してないです)

## 使い方
1. 以下のように画像ファイルを配置する
    ```
    .emojidir
        emoji1.png
        emoji2.png
        emoji3.gif
    ```
2. CLIを開いてスクリプトを実行する
    ```
    # Windowsの場合
    python C:\path\to\scriptfile\make_import_zipfile.py --datadir C:\path\to\emojidir
    ```
3. Zipファイルが吐かれるのでこれをMisskeyにインポートする
    1. コントロールパネルのカスタム絵文字ページの「・・・」をクリック
    2. インポート⇒アップロード

## 備考
- 対応する拡張子を増やすときはpyファイルをいじってください

## 参考
- https://scrapbox.io/defaultcf/Misskey%E3%81%A7%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E7%B5%B5%E6%96%87%E5%AD%97%E3%82%92%E4%B8%80%E6%B0%97%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B
- https://misskey-hub.net/en/docs/admin/emoji.html#bulk-emoji-import
