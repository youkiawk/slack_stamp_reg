# Study!
# https://www.youtube.com/watch?v=5XdS0HmVfKM
# https://qiita.com/sukesuke/items/1ac92251def87357fdf6

from slackbot.bot import default_reply
from slackbot.bot import respond_to

import requests
from bs4 import BeautifulSoup
import json
import sys


def imageUrl(link, imagename):
    """
    画像をダウンロードし、保存
    """
    # get HTML
    res = requests.get(link)
    # get beautifulsoup object
    soup = BeautifulSoup(res.text, 'html.parser')
    # extract lists of stamp
    found = soup.find_all('li', class_='mdCMN09Li FnStickerPreviewItem')
    # extract urls or image
    url_list = [json.loads(found[i]['data-preview'])['staticUrl'] for i in range(len(found))]
    # scrap images
    for i, url in enumerate(url_list):
        image = requests.get(url).content
        dst = "output/" + imagename + "/" + str(i) + ".png"
        with open(dst, "wb") as f:
            print("download to: " + dst)
            f.write(image)

def getImageUrl(res):
    """
    スタンプ画像のUrlを返す
    """
    # get HTML
    # res = requests.get(link)
    # get beautifulsoup object
    soup = BeautifulSoup(res.text, 'html.parser')
    # extract lists of stamp
    found = soup.find_all('li', class_='mdCMN09Li FnStickerPreviewItem')
    # extract urls or image
    url_list = [json.loads(found[i]['data-preview'])['staticUrl'] for i in range(len(found))]

    return url_list

@respond_to('使い方')
def respond_func(message):
    message.send("LINE STOREで、好きなスタンプのページのURLをコピーして僕に送信すると、全てのスタンプの画像のURLを返信します。 \
        \nLINE STOREはコチラ https://store.line.me/stickershop/\
        \nスタンプの登録はまだできないよ！\
        \n＜NEW!＞ [数字][半角スペース][URL]と入力すると、先頭から[数字]番目のスタンプのURLだけ取得できます。")  

@default_reply()
def default_func(message):
    text = message.body['text']
    text = text.replace("<","").replace(">","")
    texts = text.split(" ")
    text_url = ""
    text_stampidx = -1
    print(texts)
    if len(texts) > 2:
        message.send("おっと、何か間違えてるようです。使い方は、「使い方」と送信してください。")
        return
    elif len(texts) == 2:
        valid_num = [str(i) for i in range(1,41)]
        if texts[0] not in valid_num:
            message.send("スタンプの番号は、半角数字で1から40のうちから一つ入力してください。使い方は、「使い方」と送信してください。")
            return
        text_stampidx = int(texts[0])
        text_url = texts[1]
    elif len(texts) == 1:
        text_url = texts[0]

    if "https://store.line.me" not in text_url:
        message.send("スタンプのページのURLを指定してください。使い方は、「使い方」と送信してください。")
        return

    res = requests.get(text_url)
    if res.status_code == 200:
        url_list = getImageUrl(res)
        url_onetext = ""
        for i, imgurl in enumerate(url_list):
            if text_stampidx != -1 and text_stampidx != i + 1:
                continue
            url_onetext = url_onetext + "\n" + imgurl
        message.send(url_onetext)
    else:
        message.send("無効なURLのようです！\n`status code = {}`".format(res.status_code))


if __name__ == "__main__":
    pass
