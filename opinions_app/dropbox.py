"""Async Dropbox file upload and sharing functionality."""
import asyncio
import json
import os

import aiohttp
from werkzeug.datastructures import FileStorage

DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN', '')
AUTH_HEADER = f'Bearer {DROPBOX_TOKEN}'
UPLOAD_LINK = os.getenv('UPLOAD_LINK', '')
SHARING_LINK = os.getenv('SHARING_LINK', '')


async def async_upload_files_to_dropbox(
    images: list[FileStorage] | None
) -> list[str] | None:
    """Upload multiple images to Dropbox concurrently and return sharing URLs."""
    if images is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for image in images:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, image)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return list(urls)
    return None


async def upload_file_and_get_url(
    session: aiohttp.ClientSession, image: FileStorage
) -> str:
    """Upload a single image to Dropbox and return its sharing URL."""
    dropbox_args = json.dumps({
        'autorename': True,
        'mode': 'add',
        'path': f'/{image.filename}',
    })
    async with session.post(
        UPLOAD_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': dropbox_args
        },
        data=image.read()
    ) as response:
        data = await response.json()
        path = data['path_lower']
    async with session.post(
        SHARING_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/json',
        },
        json={'path': path}
    ) as response:
        data = await response.json()
        if 'url' not in data:
            data = data['error']['shared_link_already_exists']['metadata']
        url = data['url']
        url = url.replace('&dl=0', '&raw=1')
    return url
