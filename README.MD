# 使用于shell的翻译
---

* 暂时封装了对百度翻译的api调用
* 支持对管道输入与传参输入
  * 管道输入暂时仅支持 `stdin`

## 安装

1. 克隆获取下载 `translate.py` 到您的设备 `/usr/bin/translate.py`
2. 赋予执行权限 `sudo chmod  744 /usr/bin/translate.py`
3. 将 以下内容添加到您的 `~/.bashrc`中
    ```bash
    # 百度的appid 与 key请通过https://fanyi-api.baidu.com/manage/developer 获取
    export SHELL_TRANSLATE_APPID="你的 APPID"
    export SHELL_TRANSLATE_KEY="你的密钥"
    ```
4. 执行刷新 `source ~/.bashrc`

## 使用
* 通过管道输入 `echo "hello world" | translate.py`
* 通过传参输入 `translate.py "hello world"`
   ```bash
  $ echo "hello world" | translate.py
  hello world
  你好，世界
  ```
* 翻译整个帮助
  ```bash
  $ docker -h | translate.py
  
  Usage:  docker [OPTIONS] COMMAND
  用法：docker[OPTIONS]COMMAND
    A self-sufficient runtime for containers
    容器的自给自足运行时
    Options:
    选项：
  ...
  ```