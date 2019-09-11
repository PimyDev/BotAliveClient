import aiohttp
import asyncio
import json
import sys
import traceback


class Monitoring:
    def __init__(self, server_url: str, bot_name: str, token: str, run_async=False):
        """
        Args:
            server_url (str): Url to which the request will go
            bot_name (str): The name of the bot that will be displayed in the notification
            token (str): Token for this ip
            run_async (bool): async or sync bot
        """

        self.server_url = server_url
        self.bot_name = bot_name
        self.token = token
        self.run_async = run_async
        self.session = aiohttp.ClientSession()
        self._event_loop = asyncio.get_event_loop()
        self.timeout = 30

    def api_call(self, action: str, data: dict):
        data['action'] = action
        data['token'] = self.token
        data['bot_name'] = self.bot_name

        if self._event_loop is None:
            self._event_loop = self._get_event_loop()

        future = asyncio.ensure_future(
            self._request(url=self.server_url, data=data),
            loop=self._event_loop,
        )

        if self.run_async:
            return future

        return self._event_loop.run_until_complete(future)

    async def _request(self, url, data):
        if self.session and not self.session.closed:
            async with self.session.post(url=url, data=data) as res:
                a = await res.text()
                print(a)
                return {
                    "data": await res.json(),
                    "headers": res.headers,
                    "status_code": res.status,
                }
        async with aiohttp.ClientSession(
                loop=self._event_loop, timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as session:
            async with session.post(url=url, data=data) as res:
                return {
                    "data": await res.json(),
                    "headers": res.headers,
                    "status_code": res.status,
                }


    def _get_event_loop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    def send_error(self, name, value, traceback):
        """ Send error to server

        Args:
            name (str): Error name
            value (str): Error value
            traceback (str): Error traceback
        Returns:
            response (dict)
        """
        data = {
            "error": json.dumps({
                "name": name,
                "value": value,
                "traceback": traceback
            })
        }
        response = self.api_call(action="error", data=data)
        return response

    def sync_error_handler(self, func):
        """ Handler for sync bots"""
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                error = str(e)
                error_traceback = traceback.format_exc()
                print(error)
                self.send_error(name=error, traceback=error_traceback, value="handler")

        return wrapper

    def async_error_handler(self, func):
        """ Handler for async bots"""
        async def wrapper(event):
            try:
                await func(event)
            except Exception as e:
                error = str(e)
                error_traceback = traceback.format_exc()
                print(error)
                await self.send_error(name=error, traceback=error_traceback, value="handler")

        return wrapper
