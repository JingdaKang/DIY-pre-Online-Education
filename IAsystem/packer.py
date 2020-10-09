import requests


def packer(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        print(r.text[:1000])
    except Exception as e:
        return ("爬取失败")


packer("https://max.book118.com/html/2017/0712/121884545.shtm")
