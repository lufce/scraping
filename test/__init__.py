import requests as webs
import lxml

req = webs.get("a")
req.encoding = req.apparent_encoding
print(req.text)
