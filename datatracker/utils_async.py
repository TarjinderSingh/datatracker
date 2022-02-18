import asyncio
import functools

from hailtop.utils import bounded_gather
from hailtop.aiotools.router_fs import RouterAsyncFS

import nest_asyncio
nest_asyncio.apply()


async def async_check_files_exist(file_paths):
    async with RouterAsyncFS('file') as fs:
        results = await bounded_gather(
            *[functools.partial(fs.exists, file_path)
              for file_path in file_paths],
            parallelism=150)
        return {file_path: exists for file_path, exists in zip(file_paths, results)}


def check_files_exist(file_paths):
    return asyncio.run(async_check_files_exist(file_paths))
