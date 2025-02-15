# 简单的基于botpy的qq官方ai聊天机器人

## 一、配置config中的配置文件

### 1. config.yml

```yml
botpy:
    appid: "qqbot appid"
    secret: "qqbot secret"
intents:
    public_messages: true
    public_guild_messages: true
```

### 2. deepseek.yml

```yaml
deepseek:
    api_key: "api_key" # 配置你的ai的apikey
    base_url: "base_url" # 配置api的基础路径
```

### 3. mysql.yml

```yml
database: # 配置数据库连接记录聊天记录
    host: localhost
    port: 3306
    database: botpy
    username: root
    password: 123456
```

## 二、导入数据库

``` sql
新建数据库导入qqbot.sql即可
```

## 三、启动机器人

### 1. windows 启动

```cmd
run.bat
```