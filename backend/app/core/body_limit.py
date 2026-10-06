import asyncio

from starlette.types import ASGIApp, Message, Receive, Scope, Send

MAX_BODY_BYTES = 32 * 1024
BODY_READ_TIMEOUT_SECONDS = 10
_CREATE_PATH = b"/api/v1/urls"


class BodySizeLimitMiddleware:
    """Bound create requests, including chunked bodies without Content-Length."""

    def __init__(self, app: ASGIApp, max_bytes: int = MAX_BODY_BYTES):
        self.app = app
        self.max_bytes = max_bytes

    async def _reject(self, send: Send, status: int, detail: str) -> None:
        body = ('{"detail":"' + detail + '"}').encode()
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode()),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] != "http"
            or scope["method"] != "POST"
            or scope["path"].encode() != _CREATE_PATH
        ):
            await self.app(scope, receive, send)
            return

        lengths = [value for name, value in scope["headers"] if name.lower() == b"content-length"]
        if len(lengths) > 1:
            await self._reject(send, 400, "Invalid Content-Length")
            return
        if lengths:
            try:
                content_length = int(lengths[0])
                if content_length < 0:
                    raise ValueError
            except ValueError:
                await self._reject(send, 400, "Invalid Content-Length")
                return
            if content_length > self.max_bytes:
                await self._reject(send, 413, "Request body too large")
                return

        # Buffer only this small, bounded create payload before passing it on.
        # This avoids reading an unbounded request.body() for chunked requests.
        messages: list[Message] = []
        total = 0
        try:
            async with asyncio.timeout(BODY_READ_TIMEOUT_SECONDS):
                while True:
                    message = await receive()
                    if message["type"] == "http.disconnect":
                        return
                    messages.append(message)
                    total += len(message.get("body", b""))
                    if total > self.max_bytes:
                        await self._reject(send, 413, "Request body too large")
                        return
                    if not message.get("more_body", False):
                        break
        except TimeoutError:
            await self._reject(send, 408, "Request body timed out")
            return

        next_message = 0

        async def replay_receive() -> Message:
            nonlocal next_message
            if next_message < len(messages):
                message = messages[next_message]
                next_message += 1
                return message
            return await receive()

        await self.app(scope, replay_receive, send)
