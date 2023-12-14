from channels.generic.websocket import AsyncWebsocketConsumer


class BabyCare(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # 广播接收到的二进制数据给所有已连接的 WebSocket
            await self.send(bytes_data=bytes_data)
