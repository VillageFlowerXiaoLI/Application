# 应用文件层次说明文档
## Application
* /__init__.py        应用初始化
* /requirements.txt   依赖库列表
* /config.py          配置名称，变量列表
* /instance/config.py 私密配置项
* /app_debug.py       测试运行应用
* /app.py             实际运行应用
* /moudles.py         模型，包括算法或请求处理
* /views.py           试图，即展示出来的页面
* /templates/         html文件(jinja2)
* /static/            向用户展示的静态文件(css,img,ext)

# 数据库格式说明文档
## 用户资料
* id integer identity(1,1),
* username text not null,
* password text not null,
* nickname text not null,
* sex text,
* birthday text,
* email text,
* phone_number text not null,
* head_img text,
## 文章信息
* id
* 作者
* 类型
* 标题
* 内容
* 图片链接
* 点赞信息，评论信息(可以起一个新表)
