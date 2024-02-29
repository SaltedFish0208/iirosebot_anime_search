import requests

from loguru import logger
from io import BufferedReader, BytesIO
from API.api_message import at_user
from API.api_iirose import APIIirose  # 大部分接口都在这里
from globals.globals import GlobalVal  # 一些全局变量 now_room_id 是机器人当前所在的房间标识，websocket是ws链接，请勿更改其他参数防止出bug，也不要去监听ws，websockets库只允许一个接收流
from API.api_get_config import get_master_id  # 用于获取配置文件中主人的唯一标识
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enmu

API = APIIirose()  # 吧class定义到变量就不会要求输入self了（虽然我都带了装饰器没有要self的 直接用APIIirose也不是不可以 习惯了

searchapi = "http://saucenao.com/search.php?output_type=2&db=999&numres=10&dbs[]=5&dbs[]=21"
apikey = ""

@on_command('>搜图 ', True, command_type=[MessageType.room_chat, MessageType.private_chat])  # command_type 参数可让本指令在哪些地方生效，发送弹幕需验证手机号，每天20条。本参数需要输入列表，默认不输入的情况下只对房间消息做出反应，单个类型也需要是列表
async def searchanime(Message, text):  # 请保证同一个插件内不要有两个相同的指令函数名进行注册，否则只会保留最后一个注册的
    result = ''
    response = requests.get(f'{searchapi}&url={text}&api_key={apikey}').json()
    # pixiv
    if response["results"][0]["header"]["index_id"] == 5:
        result = f'[{response["results"][0]["header"]["thumbnail"]}#e]\n来源：pixiv\n标题：{response["results"][0]["data"]["title"]}\n作者：{response["results"][0]["data"]["member_name"]}\n相似度：{response["results"][0]["header"]["similarity"]}\n链接：{response["results"][0]["data"]["ext_urls"][0]}'
    # anidb
    if response["results"][0]["header"]["index_id"] == 21:
        result = f'[{response["results"][0]["header"]["thumbnail"]}#e]\n来源：番剧\n标题：{response["results"][0]["data"]["source"]}\n位置：{response["results"][0]["data"]["part"]}P  {response["results"][0]["data"]["est_time"]}\n相似度：{response["results"][0]["header"]["similarity"]}\n链接：{response["results"][0]["data"]["ext_urls"][0]}'
    await API.send_msg(Message, result)