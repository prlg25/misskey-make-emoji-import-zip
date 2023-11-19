# misskey-make-emoji-import-zip
Misskeyのカスタム絵文字をバルクインポートするためのZIPファイルを作成するスクリプト

## 環境
- Python3.11(古いバージョンでも動くかもですが動作確認してないです)
- Windows11(他のOSでも動くと思いますが動作確認してないです)

## 機能
- 所定の形式のyamlと画像を用意すれば、絵文字import用zipを生成できます
- [pykakasi](https://pypi.org/project/pykakasi/)を使って読み仮名のタグを自動生成します
    - pykakasiの癖を御しきれていないので"どぅ"などの特殊表記を中心に変な自動生成になります

## 使い方
1. 以下のようなyaml形式のフォーマットで絵文字申請してもらう
    - 半角スペースを抜かさないようにしてもらいましょう
    ```
    ====ここからテンプレ====
    emojiname:
      テキスト: テキスト
      読み仮名: てきすと
      その他つけたいタグ: タグ1,タグ2
      カテゴリ名: Japanese_words
      使用フォント: フォント名(ある場合)
    ====ここまでテンプレ====
    ```
2. 以下のように画像ファイルを配置する
    - 画像ファイル名とyamlのemojinameを対応させるようにしましょう
    ```
    .emojidir
        emoji1.png
        emoji2.png
        emoji3.gif
    ```
3. CLIを開いてスクリプトを実行する
    ```
    # Windowsの場合
    python C:\path\to\scriptfile\make_import_zipfile.py --datadir C:\path\to\emojidir --yamlpath C:\path\to\yamlpath.yaml
    ```
    - C:\path\to\emojidir\meta.jsonが生成されるので問題ないか確認します

4. 生成されたzipファイルをMisskeyにインポートする
    1. C:\path\to\emojidir\import_zipfile.zipにインポート用ZIPファイルが生成されます
    2. コントロールパネルのカスタム絵文字ページの「・・・」をクリック
    3. インポート⇒アップロード

## 備考
- 対応する拡張子を増やすときはpyファイルをいじってください

## ライセンス
- pykakasiがGPLライセンスのためGPLライセンスとしています

## 参考
- https://scrapbox.io/defaultcf/Misskey%E3%81%A7%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E7%B5%B5%E6%96%87%E5%AD%97%E3%82%92%E4%B8%80%E6%B0%97%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B
- https://misskey-hub.net/en/docs/admin/emoji.html#bulk-emoji-import
