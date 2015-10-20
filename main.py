#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from asyncio import subprocess
import datetime


loop = asyncio.get_event_loop()

async def exhaust_stream_reader(stream_reader, name, input):
    while True:
        line = await stream_reader.readline()

        if not line and stream_reader.at_eof():
            break

        msg = line.decode('utf-8').rstrip()
        formatted_msg = '[{}] [{:<10}] [{}] - {}'.format(
            datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            name,
            input,
            msg,
        )

        print(formatted_msg, flush=True)


async def custom_subprocess(subprocess_command, name):
    proc = await asyncio.create_subprocess_exec(
        *subprocess_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    asyncio.wait([
        asyncio.ensure_future(exhaust_stream_reader(proc.stdout, name, 'out')),
        asyncio.ensure_future(exhaust_stream_reader(proc.stderr, name, 'err')),
    ])

    await proc.wait()


loop = asyncio.get_event_loop()
loop.set_debug(True)


try:
    loop.run_until_complete(asyncio.gather(
        custom_subprocess(['programs/dumb_loop'], 'dumbone'),
        custom_subprocess(['programs/dumb_loop'], 'dumbtwo'),
    ))
except KeyboardInterrupt:
    loop.close()

loop.close()
