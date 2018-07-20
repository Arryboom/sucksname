#coding:utf-8
from lxml import etree
import requests
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

x=requests.get("http://www.resgain.net/xmdq.html")
lx=etree.HTML(x.text)
z=lx.xpath("/html/body/div[3]/div/div/div[2]/a[@*]/@href")
Xinglist={}
Minglist={}
mMinglist=[]
fMinglist=[]
for each in z:
    Xinglist[each.getparent().text]="http:"+str(each)

for eachxing in Xinglist.keys():
    mMinglist=[]
    fMinglist=[]
    m_count = 1
    fm_count=1
    curl = Xinglist[eachxing].replace(r"/name_list.html",  "/name/boys_{page}.html".format(page=m_count))
    boy=requests.get(curl)
    while(boy.status_code==200):
        boyx=etree.HTML(boy.text)
        boyx=boyx.xpath("/html/body/div[@class='main_']/div[@class='container'][2]/div[@class='row'][1]/div[@class='col-xs-12']/a[@class='btn btn-link'][@*]")
        print "allcount:"+str(len(boyx))
        print "currentpage"+str(m_count)
        if len(boyx)==0:
            break
        for a in boyx:
            mMinglist.append(a.text)
        m_count=m_count+1
        boy.close()
        curl = Xinglist[eachxing].replace(r"/name_list.html", "/name/boys_{page}.html".format(page=m_count))
        boy = requests.get(curl)
    boy.close()
    curl = Xinglist[eachxing].replace(r"/name_list.html",  "/name/girls_{page}.html".format(page=fm_count))
    girls=requests.get(curl)
    while(girls.status_code==200):
        girlx=etree.HTML(girls.text)
        girlx=girlx.xpath("/html/body/div[@class='main_']/div[@class='container'][2]/div[@class='row'][1]/div[@class='col-xs-12']/a[@class='btn btn-link'][@*]")
        print "allcount:"+str(len(girlx))
        print "currentpage"+str(m_count)
        if len(girlx)==0:
            break
        for xa in girlx:
            fMinglist.append(xa.text)
        fm_count=fm_count+1
        girls.close()
        curl = Xinglist[eachxing].replace(r"/name_list.html", "/name/girls_{page}.html".format(page=fm_count))
        girls = requests.get(curl)
    girls.close()
    Minglist[eachxing+"-男"]=mMinglist
    Minglist[eachxing + "-女"] = fMinglist
for eachxingming in Minglist.keys():
    namelist="namelist/"+eachxingming+".txt"
    with open(namelist,"w") as ffff:
        ffff.writelines([line + '\r\n' for line in Minglist[eachxingming]])
