import hashlib
import time
import xml.etree.ElementTree as ET
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Query, Request, Response

from .config import BASE_URL, WECHAT_TOKEN
from .llm import query
from .store import store

router = APIRouter()


def parse_xml(body: bytes) -> dict:
    root = ET.fromstring(body)
    return {child.tag: child.text for child in root}


def build_reply_xml(to_user: str, from_user: str, content: str) -> str:
    return (
        "<xml>"
        f"<ToUserName><![CDATA[{to_user}]]></ToUserName>"
        f"<FromUserName><![CDATA[{from_user}]]></FromUserName>"
        f"<CreateTime>{int(time.time())}</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content>"
        "</xml>"
    )


def process_query(result_id: str, scene: str, client):
    try:
        result = query(scene, client)
        store.set_result(result_id, result)
    except Exception as e:
        store.set_error(result_id, str(e))


@router.get("/wechat")
async def verify(
    signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
):
    check = hashlib.sha1(
        "".join(sorted([WECHAT_TOKEN, timestamp, nonce])).encode()
    ).hexdigest()
    if check == signature:
        return Response(content=echostr, media_type="text/plain")
    return Response(content="Invalid signature", status_code=403)


@router.post("/wechat")
async def handle_message(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    msg = parse_xml(body)

    msg_type = msg.get("MsgType", "")
    if msg_type != "text":
        return Response(
            content=build_reply_xml(
                msg["FromUserName"], msg["ToUserName"], "请发送文字消息哦~"
            ),
            media_type="application/xml",
        )

    msg_id = msg.get("MsgId", "")
    scene = msg.get("Content", "").strip()

    # Dedup: WeChat retries with same MsgId
    existing = store.get_by_msg_id(msg_id)
    if existing:
        result_id = existing
    else:
        result_id = uuid4().hex[:12]
        store.create(result_id, scene, msg_id)
        background_tasks.add_task(
            process_query, result_id, scene, request.app.state.client
        )

    link = f"{BASE_URL}/result/{result_id}"
    reply = f"正在为你查询，请点击查看结果：\n{link}"
    return Response(
        content=build_reply_xml(msg["FromUserName"], msg["ToUserName"], reply),
        media_type="application/xml",
    )
