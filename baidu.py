# -*- coding: utf-8 -*-

from bypy import ByPy
import os, sys
import datetime, time

'''
1、安装 ByPy：pip install bypy
2、授权：bypy info
3、解决报错: pip install pyopenssl
'''

CONFIG = {
    "backupPath": "backup", # 百度网盘备份目录名（我的应用数据的bypy 目录下）
    "db_host": "127.0.0.1", # 数据库主机名
    "db_user": "root",      # 数据库用户名
    "db_passwd": "",        # 数据库密码
    'db_name': [            # 数据库名称列表
        "abc"
    ],
    "mysql_backup": True    # 是否备份
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
        dir_name = CONFIG['backupPath']
        totalFileSize = 0  # 文件大小变量
        start = datetime.datetime.now()  # 计时开始

        # 获取一个bypy对象，封装了所有百度云文件操作的方法
        bp = ByPy()
        # 百度网盘创建远程文件夹backup
        bp.mkdir(remotepath=dir_name)

        if isinstance(allFiles,str):
            allFiles = [allFiles]

        for file in allFiles:
            if not os.path.exists(file):
                continue
            fileName = os.path.basename(file)
            filePath = os.path.dirname(file)
            print("正在上传文件:" + file)

            if file != "":
                localpath = filePath if filePath else "."
                bp.upload(localpath=localpath + "/" + fileName, remotepath=str(dir_name), ondup='newcopy')
                print("文件发送完成：本地路径：" + localpath + "/" + fileName + " 远程文件夹：" + dir_name)
                totalFileSize += self.get_FileSize(localpath + "/" + fileName)
            else:
                bp.upload(localpath=fileName, remotepath=dir_name, ondup='newcopy')
                print("文件发送完成：" + fileName + " 远程文件夹：" + dir_name)
                totalFileSize += self.get_FileSize("." + filePath + "/" + fileName)
            print("------------------------------------")

        end = datetime.datetime.now()  # 计时结束

        print("上传文件总大小为" + str(totalFileSize) + "MB")
        print("花费时间(s)：" + str((end - start).seconds))
        print("\nupload ok")

class BackupToAWS:

    aws_key = 'xxx'
    aws_secret = 'xxx'
    backet_name = 'xxx'
    region_name = "us-west-1"

    def upload_to_s3(self, file_path):
        _, file_name = os.path.split(file_path)
        session = Session(
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret,
            region_name = self.region_name)

        s3 = session.resource("s3")
        client = session.client("s3")
        bucket = self.backet_name
        upload_data = open(file_path, "rb")
        upload_key = file_name
        file_obj = s3.Bucket(bucket).put_object(Key=upload_key, Body=upload_data)




class AllBackup:
    
    def mysqlBackup(self):
        backup_time = time.strftime('%Y%m%d-%H%M%S')
        for db_name in CONFIG['db_name']:
            backup_sql = "/tmp/" + db_name + backup_time + ".sql"
            dumpcmd = "mysqldump -u " + CONFIG['db_user'] + " -p" + CONFIG['db_passwd'] + " " + db_name + " > " + backup_sql
            os.system(dumpcmd)
            print("Dump of "+ backup_sql +" completed")
            backup_file = "/tmp/" + db_name + backup_time + ".tar.gz"
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(backup_sql, arcname=os.path.basename(backup_sql))
            tar.close()

            backup = BackupToBaidu()
            backup.uploadFiles(backup_file)

            backup_aws = BackupToAWS()
            backup_aws.upload_to_s3(backup_file)
            print("正在删除文件：" + backup_sql)
            os.system("rm -f " + backup_sql)
            print("正在删除文件：" + backup_file)            
            os.system("rm -f " + backup_file)            



if __name__ == "__main__":

    if len(sys.argv) > 1:
        allFiles = sys.argv[1:]
        backup = BackupToBaidu()
        backup.uploadFiles(allFiles)

    allBackup = AllBackup()

    if CONFIG['mysql_backup']:
        allBackup.mysqlBackup()
