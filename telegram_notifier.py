import asyncio
import base64
import json
import mimetypes
import os

import aiohttp

from config import PROXY_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USE_PROXY


TELEGRAM_API_BASE = "https://api.telegram.org"
TELEGRAM_TEXT_LIMIT = 4000


def _api_url(method):
    return f"{TELEGRAM_API_BASE}/bot{TELEGRAM_BOT_TOKEN}/{method}"


def _is_configured():
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        print(f"错误: Telegram 配置缺失: {', '.join(missing)}")
        return False
    return True


async def _read_response(response):
    response_text = await response.text()
    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError:
        response_data = {}
    return response_text, response_data


async def _send_single_message(session, content, proxy, msg_type="text"):
    """向 Telegram 发送单条文本消息。"""
    if msg_type not in {"text", "markdown"}:
        print(f"不支持的消息类型: {msg_type}")
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": content,
        "link_preview_options": {"is_disabled": True},
    }
    if msg_type == "markdown":
        payload["parse_mode"] = "Markdown"

    try:
        async with session.post(
            _api_url("sendMessage"), json=payload, proxy=proxy
        ) as response:
            response_text, response_data = await _read_response(response)
            if response.status == 200 and response_data.get("ok"):
                print(f"Telegram 消息片段发送成功! (长度: {len(content)})")
                return True

            description = response_data.get("description", response_text)
            print(f"Telegram 消息片段发送失败: {response.status}, {description}")
            return False
    except Exception as exc:
        print(f"Telegram 消息片段发送出错: {exc}")
        return False


async def _send_image(
    session,
    image_path=None,
    image_base64=None,
    proxy=None,
    title="图片",
):
    """向 Telegram 发送单张图片。"""
    if image_base64:
        try:
            image_data = base64.b64decode(image_base64, validate=True)
        except (ValueError, TypeError) as exc:
            print(f"解码 base64 图片失败: {exc}")
            return False
        filename = "image.png"
    elif image_path:
        if not os.path.isfile(image_path):
            print(f"图片不存在: {image_path}")
            return False
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
        except OSError as exc:
            print(f"读取图片失败: {exc}")
            return False
        filename = os.path.basename(image_path)
    else:
        print("未提供图片数据")
        return False

    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    form = aiohttp.FormData()
    form.add_field("chat_id", TELEGRAM_CHAT_ID)
    form.add_field(
        "photo",
        image_data,
        filename=filename,
        content_type=content_type,
    )
    if title:
        form.add_field("caption", title[:1024])

    try:
        async with session.post(
            _api_url("sendPhoto"), data=form, proxy=proxy
        ) as response:
            response_text, response_data = await _read_response(response)
            if response.status == 200 and response_data.get("ok"):
                print("Telegram 图片发送成功!")
                return True

            description = response_data.get("description", response_text)
            print(f"Telegram 图片发送失败: {response.status}, {description}")
            return False
    except Exception as exc:
        print(f"Telegram 图片发送出错: {exc}")
        return False


def split_message(message, max_length=TELEGRAM_TEXT_LIMIT):
    """按行优先将长消息切分为多个 Telegram 消息片段。"""
    if len(message) <= max_length:
        return [message]

    segments = []
    current_segment = ""

    for line in message.split("\n"):
        separator_length = 1 if current_segment else 0
        if len(current_segment) + separator_length + len(line) <= max_length:
            current_segment = (
                f"{current_segment}\n{line}" if current_segment else line
            )
            continue

        if current_segment:
            segments.append(current_segment.strip())
            current_segment = ""

        while len(line) > max_length:
            segments.append(line[:max_length])
            line = line[max_length:]
        current_segment = line

    if current_segment:
        segments.append(current_segment.strip())

    total = len(segments)
    return [f"[{index}/{total}]\n{segment}" for index, segment in enumerate(segments, 1)]


async def send_message_async(message_content, msg_type="text"):
    """向 Telegram 发送文本消息，长消息会自动分段。"""
    if not _is_configured():
        return False

    segments = split_message(str(message_content))
    total_segments = len(segments)
    if total_segments > 1:
        print(f"消息将被分成 {total_segments} 段发送")

    proxy = PROXY_URL if USE_PROXY else None
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for index, segment in enumerate(segments, 1):
            if not await _send_single_message(session, segment, proxy, msg_type):
                print(f"第 {index}/{total_segments} 段消息发送失败")
                return False
            if index < total_segments:
                await asyncio.sleep(0.5)

    print(
        f"所有 {total_segments} 段消息发送完成"
        if total_segments > 1
        else "Telegram 消息发送成功!"
    )
    return True


async def send_image_async(image_path=None, image_base64=None, title="图片"):
    """向 Telegram 发送图片。"""
    if not _is_configured():
        return False

    proxy = PROXY_URL if USE_PROXY else None
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        return await _send_image(
            session,
            image_path=image_path,
            image_base64=image_base64,
            proxy=proxy,
            title=title,
        )
