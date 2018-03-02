import sys, getopt,re,subprocess,os
opts, args = getopt.getopt(sys.argv[1:], "hs:v:")
mp4=""
srt=""
objpath=""
for op, value in opts:
    if op == "-s":
        srt = value
        print(srt)
    elif op == "-v":
        mp4 = value
        print(mp4)
    elif op == "-h":
        print('help')
        sys.exit()
def videotime(srttime):
    tmp=srttime.split('-->')
    tmp1=tmp[0].split('.')
    tmp1=tmp1[0].split(':')
    timestart=int(tmp1[0])*60*60+int(tmp1[1])*60+int(tmp1[2])
    tmp2=tmp[1].split('.')
    tmp2=tmp2[0].split(':')
    timeend=int(tmp2[0])*60*60+int(tmp2[1])*60+int(tmp2[2])
    return int((timeend-timestart)/2+timestart);
objpath=os.path.dirname(os.path.realpath(mp4))
isExists=os.path.exists(objpath+'/md')
if not isExists:
    os.makedirs(objpath+'/md')
    os.makedirs(objpath+'/md/img')
# else:
#     print('md目录已存在')
#     sys.exit()
savestr='';
file = open(srt)
tmptime=""
tmpis=0;tmpline='';tmphtml=''
for line in file:
    line=line.strip("\n")
    if line.find('-->')>-1:
        tmptime=line
        tmpis=1
    else:
        if line.find('[*]')>-1:
            #print(tmptime)
            tmps=videotime(tmptime)
            cmd = 'ffmpeg -i '+mp4+' -y -f image2 -ss '+str(tmps)+' -t 0.001 -s 1920x1080 '+objpath+'/md/img/'+str(tmps)+'.jpg'
            subprocess.call(cmd.encode(sys.getfilesystemencoding()), shell=True)
            #print(line)
            #line=line.replace("[*]", "");
            tmphtml+=line.replace("[*]", "<br>"+'<img src="img/'+str(tmps)+'.jpg" alt="">'+"<br>")  #+"\n"
            #print(savestr)
        else:
            if tmpis==1 and line:
                tmphtml+=line+"<br>"
    if line=='':
        tmpis=0
        tmphtml=tmphtml.replace("<br>", "");
        tmphtml=tmphtml.replace("<img", "</p><p><img");
        if tmphtml :
            savestr+="<p>"+tmphtml+"</p>\n"
        tmphtml=''
    pass # do something
#sys.exit()
htmlstr='<!DOCTYPE html>'+"\n"
htmlstr+='<html lang="en">'+"\n"
htmlstr+='<head>'+"\n"
htmlstr+='    <meta charset="UTF-8">'+"\n"
htmlstr+='    <meta name="viewport" content="width=device-width, initial-scale=1.0">'+"\n"
htmlstr+='    <meta http-equiv="X-UA-Compatible" content="ie=edge">'+"\n"
htmlstr+='    <link rel="stylesheet" href="style.css">'+"\n"
htmlstr+='    <script src="main.js"></script>'+"\n"
htmlstr+='    <title>Document</title>'+"\n"
htmlstr+='</head>'+"\n"
htmlstr+='<body>'+"\n"
tmphtmls=savestr.split('<img')
for index in range(len(tmphtmls)):
    tmphtml=tmphtmls[index]
    tmphtml=tmphtml.replace("<p>", "");
    tmphtml=tmphtml.replace("</p>", "");
    if tmphtml.find('alt="">')>-1:
        tmphtml="<img"+tmphtml;
        tmphtmls2=tmphtml.split('alt="">')
        htmlstr+="<p>"+tmphtmls2[0]+" alt=""></p>"
        htmlstr+="<p>"+tmphtmls2[1]+"</p>"
    else:
        htmlstr+="<p>"+tmphtml+"</p>"
htmlstr+='</body>'+"\n"
htmlstr+='</html>'+"\n"
file.close()
file = open(objpath+'/md/srt.html','w')
file.write(htmlstr)
file.close()
# 运行命令
# python hello.py -s 3.srt -v 3.mp4
#saa='123abc123abc123abc'
#print(saa)
#print(re.findall(r'123',saa))
# file = open("hello.py")
# for line in file:
#     print(line)
#     pass # do something
# file.close()
#print(os.path.dirname(os.path.realpath(mp4)))

# cmd = 'ffmpeg -i 3.mp4 -y -f image2 -ss 8 -t 0.001 -s 480x360 test.jpg'
# subprocess.call(cmd.encode(sys.getfilesystemencoding()), shell=True)
