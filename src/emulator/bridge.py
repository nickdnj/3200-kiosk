#!/usr/bin/env python3
"""WebSocket <-> telnet bridge for the OS/32 emulator terminal.

The browser can't speak telnet, and OS/32's MTM presents its terminals as a
telnet mux on :1026 (SIMH PAS device). This bridges a WebSocket (:7682) to it,
answering telnet option negotiation so control bytes never reach the screen.
Each browser connection gets its own MTM line.

websockets 10.x: handler signature is (websocket, path).
"""
import asyncio
import websockets

MTM_HOST, MTM_PORT = "127.0.0.1", 1026
WS_HOST,  WS_PORT  = "127.0.0.1", 7682
IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240


class Telnet:
    """Strip telnet IAC sequences from the stream and refuse all options."""
    def __init__(self):
        self.state = "data"; self.cmd = None

    def feed(self, data: bytes):
        out = bytearray(); resp = bytearray()
        for b in data:
            if self.state == "data":
                if b == IAC: self.state = "iac"
                else: out.append(b)
            elif self.state == "iac":
                if b == IAC: out.append(IAC); self.state = "data"
                elif b in (DO, DONT, WILL, WONT): self.cmd = b; self.state = "opt"
                elif b == SB: self.state = "sb"
                else: self.state = "data"
            elif self.state == "opt":
                if self.cmd == DO:   resp += bytes([IAC, WONT, b])
                elif self.cmd == WILL: resp += bytes([IAC, DONT, b])
                self.state = "data"
            elif self.state == "sb":
                if b == IAC: self.state = "sbiac"
            elif self.state == "sbiac":
                self.state = "data" if b == SE else "sb"
        return bytes(out), bytes(resp)


async def handler(ws, path):
    try:
        reader, writer = await asyncio.open_connection(MTM_HOST, MTM_PORT)
    except OSError:
        await ws.close(code=1011, reason="OS/32 not reachable")
        return
    tel = Telnet()

    async def tcp_to_ws():
        while True:
            data = await reader.read(4096)
            if not data: break
            out, resp = tel.feed(data)
            if resp:
                writer.write(resp); await writer.drain()
            if out:
                await ws.send(out.decode("latin-1"))

    async def ws_to_tcp():
        async for msg in ws:
            if isinstance(msg, str): msg = msg.encode("latin-1")
            writer.write(msg); await writer.drain()

    try:
        await asyncio.gather(tcp_to_ws(), ws_to_tcp())
    except (websockets.ConnectionClosed, ConnectionResetError):
        pass
    finally:
        writer.close()


async def main():
    async with websockets.serve(handler, WS_HOST, WS_PORT, ping_interval=None):
        print(f"bridge up: ws://{WS_HOST}:{WS_PORT}  ->  telnet {MTM_HOST}:{MTM_PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
