import requests

# https://movie.douban.com/explore#!type=movie&tag=%E5%96%9C%E5%89%A7&sort=recommend&page_limit=20&page_start=120

url = "https://movie.douban.com/?type=movie&tag=%E5%96%9C%E5%89%A7&sort=recommend&page_limit=20&page_start=0"
session = requests.session()
ret = session.get(url)
print(ret.content.decode())
with open("d:/1.txt", "w", encoding="utf-8") as f:
    f.write(ret.content.decode())

rl = "https://movie.douban.com/?type=movie&tag=%E5%96%9C%E5%89%A7&sort=recommend&page_limit=20&page_start=20"
ret = session.get(url)
print(ret.content.decode())
with open("d:/2.txt", "w", encoding="utf-8") as f:
    f.write(ret.content.decode())
