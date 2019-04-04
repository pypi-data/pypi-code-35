# -*- coding: utf-8 -*-
import re
import os
import json
import markdown
import codecs

pattern = '#+\s'

heading = {
    'heading1': 0,
    'heading2': -1,
    'heading3': -1,
    'heading4': -1,
    'heading5': -1,
    'heading6': -1
}

htmlHead = u'''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<script>
$(document).ready(function (){
    //初始化动态加载控件
    ajax();

    //注册菜单展开收缩事件

    $(".parentnode_title_symbol").click(function () {

        shrinkage($(this));

    })

    //当没有子节点的div去除样式

    upclass();
});
function ajax() {
    //直接使用ajax访问
    data = $("#jsonContent").val();

    var hehe = { "tbFuncDic": JSON.parse(data) }
    // alert(hehe);
    databinding(hehe);//绑定数据
}


//菜单子节点展开关闭

function shrinkage(dom) {

    //改变图片背景
    if (!dom.hasClass('parentnode_title_nochildnode_symbol')) {
        switch (parseInt($(dom).children("b").html())) {

            case 1://关闭

                $(dom).css('background-image', 'url("https://github.com/yuleMeng/pyMd2Doc/blob/master/app/static/image/plus.png")');

                $(dom).children("b").html("2");

                $(dom).parent().siblings().hide();

                break;

            case 2://展开

                $(dom).css('background-image', 'url("https://github.com/yuleMeng/pyMd2Doc/blob/master/app/static/image/minus.png")');

                $(dom).children("b").html("1");

                $(dom).parent().siblings().show();

                break;

            default: break;

        }
    }

}

//循环绑定数据

function databinding(data) {

    //动态创建树形菜单

    var parentnodediv = $(".parentnode");

    for (var i = 0; i < data.tbFuncDic.length; i++) {

        //最上层父节点

        if (data.tbFuncDic[i].parentID == 0) {

            Cycledata(parentnodediv, data.tbFuncDic[i]);

        }

    }

    //创建子节点

    if (data.tbFuncDic.length > 0) {

        childnodes(data);

    }

}

//创建子节点

function childnodes(data) {

    for (var j = 0; j < $(".parentnode").find(".parentnode_title_name").length; j++) {

        for (var i = 0; i < data.tbFuncDic.length; i++) {

            if (data.tbFuncDic[i].parentID == $(".parentnode").find(".parentnode_title_name")[j].id) {

                var parentnodediv = $($(".parentnode").find(".parentnode_title_name")[j]).parent().parent();

                Cycledata(parentnodediv, data.tbFuncDic[i]);

            }

        }

    }

}



//绑定数据方法

function Cycledata(parentnodediv, data) {



    var parentnode_noe = document.createElement("div");//创建一个div

    parentnode_noe.className = " parentnode_noe";//为div添加class

    parentnodediv.append(parentnode_noe);//将其添加到div末尾



    var parentnode_title = document.createElement("div");//创建一个div

    parentnode_title.className = " parentnode_title ";//为div添加class

    parentnode_noe.appendChild(parentnode_title);//将其添加到div末尾



    var parentnode_title_symbol = document.createElement("div");//创建一个div

    parentnode_title_symbol.className = "parentnode_title_symbol parentnode_title_fix ";//为div添加class

    parentnode_title.appendChild(parentnode_title_symbol);//将其添加到div末尾

    var b = document.createElement("b");//创建一个b标签

    b.innerHTML = 1;//为b添加内容

    parentnode_title_symbol.appendChild(b);//将其添加到div末尾


    var parentnode_title_name = document.createElement("div");//创建一个div

    parentnode_title_name.className = "parentnode_title_name";//为div添加class

    if ( data.titleName.length > 30) {
        parentnode_title_name.innerHTML = "<a href='#a_" + data.titleID + "' title='" + data.titleName + "'>" + data.titleName.substr(0,30) + '...'  + "</a>";//为div添加class
    } else {
        parentnode_title_name.innerHTML = "<a href='#a_" + data.titleID + "' title='" + data.titleName + "'>" + data.titleName + "</a>";//为div添加class
    }
    parentnode_title_name.id = data.titleID;//为div添加ID
    parentnode_title_name.setAttribute("name", data.parentID);

    parentnode_title.appendChild(parentnode_title_name);//将其添加到div末尾

}



//当没有子节点的div去除样式

function upclass() {

    $(".parentnode_title").each(function () {

        var me = $(this);

        if (me.siblings().length == 0) {

            me.find(".parentnode_title_symbol b").css("display", "none");

            me.find(".parentnode_title_symbol").addClass("parentnode_title_nochildnode_symbol").removeClass("parentnode_title_symbol");

        }

    })

}
</script>
<style>
.content {
    padding-top: 50px;
    padding-bottom: 50px;
    padding-left: 5%;
    padding-right: 5%;
    /* background-color: #f1f8ff; */
    /* background-color: #BFE6D7; */
    background-color: #e2e2e2;
}

.parentnode
{
    width: 25%;
    float:left;
    padding-top: 25px;
    padding-bottom: 25px;
    background-color: #f1f8ff;
    font-size: 15px;
    border: 2px solid #008151;
}

.right {
    margin-left: 27%;
    padding: 1px 50px;
    background-color: #f1f8ff;
    border: 2px solid #008151;
}

.parentnode a
{
    color: #009a61;
    font-weight: bold;
}

h1 {
    border-bottom: 1px solid #bec8d6;
    padding-bottom: .3em;
}

h2 {
    margin-left: 5px;
    border-bottom: 1px solid #bec8d6;
    padding-bottom: .3em;
}

h3 {
    margin-left: 10px;
    border-bottom: 1px solid #bec8d6;
    padding-bottom: .3em;
}

h4 {
    margin-left: 15px;
    border-bottom: 1px solid #bec8d6;
    padding-bottom: .3em;
}

h5 {
    margin-left: 20px;
    border-bottom: 1px solid #bec8d6;
    padding-bottom: .3em;
}

a:link {
    text-decoration: none;
}

p {
    padding: 20px 15px;
    font-size: 14px;
    text-indent:25px;
    background: #cce8cf;
    line-height: 1.4;
}


body, html
{
    padding: 0;
    margin: 0;
    border: 0;
    font-family: 'Microsoft YaHei';
}

.parentnode
{
    border: 2px solid F6F8F9;
    position: relative;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.09);
    display: inline-block;
    vertical-align: top;
}

.parentnode_noe
{
    padding-left: 20px;
}

.parentnode_title
{
    width: 100%;
    padding: 2px;
}

.parentnode_title_fix
{
    height: 24px;
    width: 18px;
    float: left;
    background-repeat: no-repeat;
    background-position: center;
    background-position-x: center;
    background-position-y: center;
}

.parentnode_title_symbol
{
    background-image: url("https://github.com/yuleMeng/pyMd2Doc/blob/master/app/static/image/minus.png");

}

    .parentnode_title_symbol:hover

    {

        cursor: pointer;

    }

    .parentnode_title_symbol b

    {

        display: none;

    }

.parentnode_title_check

{

    background-image: url("../../Image/iconUncheckAll.gif");

}

    .parentnode_title_check:hover

    {

        cursor: pointer;

    }

    .parentnode_title_check b

    {

        display: none;

    }

.parentnode_title_picture

{

    width: 24px;

    height: 24px;

    background-image: url("../../Image/folderClosed.gif");

}

.parentnode_title_nochildnode_symbol

{

    width: 18px;

}

.parentnode_title_nochildnode_picture

{

    width: 24px;

    height: 24px;

    background-image: url("../../Image/leaf.gif");

}

.parentnode_tow

{

    padding-left: 20px;

}

.parentnode_three

{

    padding-left: 20px;

}
</style>
</head>
<title>markdown转文档</title>
</head>
<body>
    <div class="content">
        <div class="parentnode"></div>
        <div class="right">
'''

htmlTail = u'''
</body>
</html>
 '''


def formatHeading():
    heading['heading1'] = 0
    heading['heading2'] = -1
    heading['heading3'] = -1
    heading['heading4'] = -1
    heading['heading5'] = -1
    heading['heading6'] = -1


def updateHeading(current, headId):
    for i in range(1, 6):
        if len(current) == i:
            heading['heading%r' % i] = headId


def getMenu(filename):
    titles = []
    global heading
    headId = 1
    current = None
    preCurrent = '$'
    parentID = 0
    with open(filename, 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            title = {}
            if not re.match(pattern, i.strip(' \t\n')):
                continue
            i = i.strip(' \t\n')
            current = i.split(' ')[0]
            # 当前标题级别比前一个小，则当前标题的父类标题是上一个的headId
            # 注释：#越多级别越小
            # 不论大多少个级别，只要父类级别大就是它的父类
            if len(current) > len(preCurrent):
                parentID = headId - 1
                # 更新当前级别父类
                updateHeading(current, parentID)
            # 当前级别比父类级别大，则去heading中寻找记录过的父类级别
            # 注释：#越少级别越大
            elif len(current) < len(preCurrent):
                length = len(current)
                # 当在文中出现一级标题的时候还原所有父类级别到初始值
                if length == 1:
                    formatHeading()
                    # 给当父类结果类赋值
                    parentID = 0
                else:
                    getVal = heading['heading%r' % length]
                    # 如果有记录过该级别的父类项
                    if getVal != -1:
                        parentID = getVal
                    # 改级别项没有记录则依次向上找父类，指导找到一级标题
                    else:
                        for j in range(length, 1, -1):
                            tempVal = heading['heading%r' % j]
                            if tempVal != -1:
                                parentID = tempVal
                                break
            titleName = i[len(current):].strip(' \t\n')
            title['titleName'] = titleName
            title['titleID'] = headId
            title['parentID'] = parentID
            titles.append(title)
            # print(headId, current, parentID)
            preCurrent = current
            headId += 1
    # print(titles)
    return titles


def writeFile(datas):
    jsObj = json.dumps(datas)
    fileObject = open('output/jsonFile.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()


def addAnchorMark(titles, name):
    filename = os.path.join(os.getcwd(), "html", name + ".html")
    anchorHtml = u''
    with open(filename, 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            for title in titles:
                old = '>' + title['titleName'] + '<'
                new = " id='a_" + str(
                    title['titleID']) + "'>" + title['titleName'] + "<"
                old = old.replace("\r", "")
                i = i.replace(old, new)
            anchorHtml += i
    # print(anchorHtml)
    out_file = '%s.html' % (name)
    output_file = codecs.open(
        out_file, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(anchorHtml)
    output_file.close()
    return anchorHtml


def convertHtml(filename, json):
    in_file = '%s.md' % (filename)
    out_file = '%s.html' % (filename)
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    output_file = codecs.open(
        out_file, "w", encoding="utf-8", errors="xmlcharrefreplace")

    htmlJson = u" </div> </div><input style='display: none' id='jsonContent' value='" + json + "'></input>"
    output_file.write(htmlHead + html + htmlJson + htmlTail)
    output_file.close()


def create(fileName):
    filePath = os.getcwd() + '/' + fileName
    mdFile = filePath + '.md'
    menu = getMenu(mdFile)
    # markdown转html（生成html）
    convertHtml(filePath, json.dumps(menu))
    # 给html加锚标记
    addAnchorMark(menu, filePath)


# ########################## 读String写入临时文件 ###########################
def createTempMd(strs, filename):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(strs)


def createByString(content, newFile):
    filePath = os.getcwd() + '/' + newFile + ".md"
    createTempMd(content, filePath)
    create(newFile)
    deleFile(filePath)


def deleFile(filePath):
    # 如果文件存在
    if os.path.exists(filePath):
        # 删除文件
        os.remove(filePath)
    else:
        print('no such file:%s' % filePath)


if __name__ == "__main__":
    create("content")
