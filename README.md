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

3. fake_useragent_0.1.11.json

对https://fake-useragent.herokuapp.com/browsers/0.1.11 文件一个备份

4. 数据库直转Protobuf 文件

```
cd sql2db
go mod tidy
go run main.go > xxx.proto
```

   

# 常见问题

1.  Max retries exceeded with url: /houtianze/bypy/master/update/update.json

```
pip install pyopenssl
```

