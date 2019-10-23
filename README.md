# 小工具集合

1.百度网盘上传(baidu.py)

```
python baidu.py file1 file2...
```

或上传备份

```
python baidu.py
```

已添加

MySQL备份上传

定时备份上传：

```
chmod +x baidu.py
# crontab -e
0 2 * * * /usr/bin/python /path/to/baidu.py
```

2. Nginx日志切割脚本示例文件： nginxLogRotate.sh

```
# vi /etc/crontab或 crontab -e
0 0 * * * root /usr/local/nginx/logs/nginxLogRotate.sh
```