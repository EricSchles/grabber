import grequests
import lxml.html
import requests
import os
import datetime
import shutil
import time
import pickle
def grabber():
    all_links = []
    urls = [
        "http://newyork.backpage.com/FemaleEscorts/",
        "http://sfbay.backpage.com/FemaleEscorts/",
        "http://northjersey.backpage.com/FemaleEscorts/",
        "http://arizona.backpage.com/FemaleEscorts/",
        "http://pennsylvania.backpage.com/FemaleEscorts/",
        "http://massachusetts.backpage.com/FemaleEscorts/",
        "http://montana.backpage.com/FemaleEscorts/"
        ]

    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    time.sleep(1500)
    for r in responses:
        text = r.text.encode("ascii","ignore")
        html = lxml.html.fromstring(text)
        links = html.xpath('//div[@class="cat"]/a/@href')
        all_links += links
    urlz = []
    for i in xrange(0,len(all_links),10):
        urlsz.append(all_links[i-10:i])
    all_responses = []
    for url_list in urlz:
        all_rs = (grequests.get(u) for u in url_list)
        all_responses += grequests.map(all_rs)
        time.sleep(15)
    return 


def save_files(all_responses):
    timestamp = str(datetime.datetime.now())
    timestamp = timestamp.split(".")[0]
    timestamp = timestamp.replace(":","_")
    timestamp = timestamp.replace(" ","_")
    dir_name = "bp_"+timestamp
    os.mkdir(dir_name)
    os.chdir(dir_name)
    for r in all_responses:
        text = r.text.encode("ascii","ignore")
        html = lxml.html.fromstring("text")
        html_imgs = html.xpath('//ul[@id="viewAdPhotoLayout"]/li/a/@src')
        img_rs = (grequests.get(u) for u in html_imgs)
        img_responses = grequests.map(img_rs)
        filename = r.url.split("/")[-1]
        allcontent = filename+"_"+timestamp
        os.mkdir(allcontent)
        os.chdir(allcontent)
        with open(filename,"w") as f:
            f.write(text)
        for img in img_responses:
            img_name = img.url.split("/")[-1]
            with open(img_name,"wb") as g:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw,g)
        os.chdir("../")

if __name__ == '__main__':
    responses = grabber()
    save_files(responses)
