# -*- coding: utf-8 -*-

from bypy import ByPy
import os, sys
import datetime

'''
1、安装 ByPy：pip install bypy
2、授权：bypy info
'''

config = {
    "backupPath": "backup"
}

class BackupToBaidu:
    # 根据当前路径和文件夹路径得到相对路径
    def relPath(self, filePath, topDir):
        relativepath = ""
        for i in range(len(filePath)):
            if i < len(topDir) and filePath[i] == topDir[i]:
                continue
            relativepath += filePath[i]
        return relativepath


    # 函数作用：给出文件夹，得到所有文件的绝对路径
    # 输入参数：当前文件夹的绝对路径
    # 返回值：一个包含所有文件绝对路径,以及文件所在文件夹的大小的列表
    def getFileList(self, file_dir):
        fileList = []
        top_dir = ""
        checkFlag = False

        for root, dirs, files in os.walk(file_dir):
            if checkFlag == False:
                top_dir = root
                checkFlag = True
            for file in files:
                fileDict = dict(Path=self.relPath(root, top_dir), fileName=file, createFlag=False)
                fileList.append(fileDict)  # 当前目录+文件名

        return fileList


    # 获取文件的大小,结果保留两位小数，单位为MB
    def get_FileSize(self, filePath):
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    def uploadFiles(self, allFiles):
        # 百度云存放文件的文件夹名
        dir_name = config['backupPath']
        totalFileSize = 0  # 文件大小变量
        start = datetime.datetime.now()  # 计时开始

        # 获取一个bypy对象，封装了所有百度云文件操作的方法
        bp = ByPy()
        # 百度网盘创建远程文件夹backup
        bp.mkdir(remotepath=dir_name)

        for file in allFiles:
            if not os.path.exists(file):
                continue
            fileName = os.path.basename(file)
            filePath = os.path.dirname(file)
            print("正在上传文件:" + file)

            if file != "":
                bp.mkdir(remotepath=dir_name + filePath)
                DIR_NAME = dir_name + filePath
                bp.upload(localpath="." + filePath + "/" + fileName, remotepath=str(DIR_NAME), ondup='newcopy')
                print("文件发送完成：本地路径：" + filePath + "/" + fileName + " 远程文件夹：" + DIR_NAME)
                totalFileSize += self.get_FileSize("." + filePath + "/" + fileName)
            else:
                bp.upload(localpath=fileName, remotepath=dir_name, ondup='newcopy')
                print("文件发送完成：" + fileName + " 远程文件夹：" + dir_name)
                totalFileSize += self.get_FileSize("." + filePath + "/" + fileName)
            print("------------------------------------")

        end = datetime.datetime.now()  # 计时结束

        print("上传文件总大小为" + str(totalFileSize) + "MB")
        print("花费时间(s)：" + str((end - start).seconds))
        print("\nupload ok")


if __name__ == "__main__":

    allFiles = sys.argv[1:]
    backup = BackupToBaidu()
    backup.uploadFiles(allFiles)