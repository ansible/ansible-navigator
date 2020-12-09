""" xterm.js in a box
"""
import asyncio
import curses
import fcntl
import logging
import os
import pty
import re
import signal
import struct
import sys
import termios
import webbrowser

from collections import deque
from http import HTTPStatus
from string import Template
from typing import Callable
from typing import List
from typing import Tuple
from typing import Union

import websockets

from websockets.http import Headers

logger = logging.getLogger("websockets")
logger.setLevel(logging.INFO)

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 8080

# pylint: disable=line-too-long
HTML_PAGE = Template(
    """
<!doctype html>
<html>
<head>
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm/css/xterm.css" />
    <script src="https://cdn.jsdelivr.net/npm/xterm/lib/xterm.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xterm-addon-web-links/lib/xterm-addon-web-links.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xterm-addon-search/lib/xterm-addon-search.js"></script>
    $add_src
    <title>$title</title>
</head>
<style>
    html,
    body {
        height: 100%;
        margin: 0px;
        background-color: #222222;
        overflow: hidden;
    }
    .full-height {
        width: 100%;
        height: 100%;
    }
    .xterm-viewport { overflow: hidden !important; }
</style>
<body>
    <div id="terminal" class="full-height"></div>
    <script>
    $script
    </script>
</body>
</html>
"""
)
DRVIER_ADD_SRC = """
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit/lib/xterm-addon-fit.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-attach/lib/xterm-addon-attach.js"></script>
"""
DRIVER_SCRIPT = Template(
    r"""
var socket = new WebSocket('ws://$ip:$port/ws');
socket.addEventListener('open', function (event) {
    fitToscreen();
});
socket.addEventListener('close', function (event) {
//  window.close();
    term.write("Disconnected. You may close this window.")
});
const term = new Terminal(),
      attachAddon = new AttachAddon.AttachAddon(socket, true, true);
	  fitAddon = new FitAddon.FitAddon();
      searchAddon = new SearchAddon.SearchAddon();
      webLinksAddon = new WebLinksAddon.WebLinksAddon();
term.loadAddon(attachAddon);
term.loadAddon(fitAddon);
term.loadAddon(searchAddon);
term.loadAddon(webLinksAddon);
term.open(document.getElementById('terminal'), true);
term.scrollback = 0;
function fitToscreen() {
    fitAddon.fit();
    socket.send(`\\\e[8;${term.rows};${term.cols}t`);
}
window.onresize = fitToscreen;
"""
)
WATCHER_ADD_SRC = ""
WATCHER_SCRIPT = Template(
    r"""
var socket = new WebSocket('ws://$ip:$port/ws');
socket.addEventListener('close', function (event) {
//  window.close();
    term.write("Disconnected. You may close this window.")
});
const term = new Terminal(),
      searchAddon = new SearchAddon.SearchAddon();
      webLinksAddon = new WebLinksAddon.WebLinksAddon();
term.loadAddon(searchAddon);
term.loadAddon(webLinksAddon);
term.resize($cols, $rows);
var socket = new WebSocket('ws://$ip:$port/ws');
var regex = new RegExp('\e\\[8;(\\d+);(\\d+)')
socket.addEventListener('message', function (event) {
    var found = event.data.match(regex);
    if (found) {
        term.resize(found[2], found[1]);
    } else {
        term.write(event.data)
    }
})
term.open(document.getElementById('terminal'), true);
term.scrollback = 0;
"""
)
# pylint: enable=line-too-long


class WebXtermJs:
    # pylint: disable=too-many-instance-attributes
    """Wrapup xtermjs for executable or curses app"""

    def __init__(self):
        self._command = None
        self._connected_clients = []
        self._current_winsize = None
        self._curses_app = None
        self._func = None
        self._logger = logging.getLogger(__name__)
        self._loop = None
        self._replay_queue = deque()
        self._ws_queue: asyncio.Queue = asyncio.Queue()

    def _set_winsize(self, fhand: int, row: int, col: int, xpix: int = 0, ypix: int = 0) -> None:
        # pylint: disable=too-many-arguments
        """set the size of the pty"""
        self._logger("setting pty size to width: %s , height: %s", col, row)
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(fhand, termios.TIOCSWINSZ, winsize)

    async def static(
        self, _path: str, request_headers: Headers
    ) -> Union[Tuple[HTTPStatus, List[Tuple[str, str]], bytes], None]:
        """Serves html if not websocket"""

        if "Upgrade" in request_headers:
            return None

        response_headers = [
            ("Server", "server"),
            ("Connection", "close"),
            ("Content-Type", "text/html"),
        ]
        if not self._connected_clients:
            page = HTML_PAGE.safe_substitute(
                add_src=DRVIER_ADD_SRC,
                script=DRIVER_SCRIPT.safe_substitute(ip=LISTEN_IP, port=LISTEN_PORT),
                title="Driving",
            )
            self._logger("served html to driver")
        else:
            page = HTML_PAGE.safe_substitute(
                add_src=WATCHER_ADD_SRC,
                script=WATCHER_SCRIPT.safe_substitute(
                    ip=LISTEN_IP,
                    port=LISTEN_PORT,
                    rows=self._current_winsize["rows"],
                    cols=self._current_winsize["cols"],
                ),
                title="Watching",
            )
            self._logger("served html to watcher")
        return HTTPStatus.OK, response_headers, page.encode()

    async def _queue_drainer(self):
        """drain the queue and send all messages
        to all clients
        """
        while True:
            message = await self._ws_queue.get()
            if message[0] == "stdout":
                for client in self._connected_clients:
                    if client.open:
                        await client.send(message[1].decode())
            elif message[0] == "quit":
                break

    async def _websocket_reader(self, pty_fd: int) -> None:
        """read the client[0] websocket, forward
        to stdin, unless a resize, forward that to all clients
        """
        try:
            async for message in self._connected_clients[0]:
                if match := re.match(r"^\\e\[8;(?P<rows>\d+);(?P<cols>\d+)t$", message):
                    self._set_winsize(
                        pty_fd,
                        int(match.groupdict()["rows"]),
                        int(match.groupdict()["cols"]),
                    )
                    self._current_winsize = match.groupdict()
                    for watcher in self._connected_clients[1:]:
                        if watcher.open:
                            await watcher.send(message)
                else:
                    os.write(pty_fd, message.encode())
        except websockets.exceptions.ConnectionClosedError:
            return

    def _stdout_reader(self, pty_fd: int) -> None:
        """read from stdout, add to queue
        add everything to the replay queue
        so newly connected clients get caughtup quickly
        """
        try:
            max_read_bytes = 1024 * 20
            pty_output = os.read(pty_fd, max_read_bytes)
            self._ws_queue.put_nowait(("stdout", pty_output))
            self._replay_queue.append(pty_output)
        except OSError:
            self._ws_queue.put_nowait(("quit", None))

    async def _init_child_proc(self) -> None:
        """for the first connected client
        fork, swap and hand off the pty to the new fork
        run the curses_app, command, func, etc
        these can exits because they lived in the fork

        add 3 funcs to the loop
        1) ws reader, gets keystrokes from client[0]
        2) queue drainer, drain stdout from queue, fwd to all clients
        3) reader, let's us now when stdout can be read
        """
        (child_pid, pty_fd) = pty.fork()
        if child_pid == 0 and self._curses_app:
            curses.wrapper(self._curses_app)
            sys.exit(0)
        elif child_pid == 0 and self._command:
            env = os.environ.copy()
            os.execvpe(self._command[0], self._command[1], env)
            sys.exit(0)
        elif child_pid == 0 and self._func:
            self._func()
            sys.exit(0)
        tasks = [
            asyncio.ensure_future(self._websocket_reader(pty_fd)),
            asyncio.ensure_future(self._queue_drainer()),
        ]
        self._loop.add_reader(pty_fd, self._stdout_reader, pty_fd)
        _done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        self._loop.remove_reader(pty_fd)

    async def _handler(self, websocket: websockets.WebSocketCommonProtocol, _path: str) -> None:
        """inbound connection, the first will kick off the
        proc, other will get caught and hangout
        """
        self._connected_clients.append(websocket)
        if len(self._connected_clients) == 1:
            await self._init_child_proc()
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            for entry in self._replay_queue:
                await websocket.send(entry.decode())
            while websocket.open:
                if not self._connected_clients[0].open:
                    await websocket.close()
                    break
                await asyncio.sleep(0.01)

    async def _serve(self, stop: asyncio.Future) -> None:
        """use the serve context handler to handle the stop
        use signal.SIGTERM to end this loop, when client[0]
        disconnects, they will throw it
        """

        async with websockets.serve(
            self._handler, LISTEN_IP, LISTEN_PORT, process_request=self.static
        ):
            print(f"Running server at http://{LISTEN_IP}:{LISTEN_PORT}/")
            webbrowser.open(f"http://{LISTEN_IP}:{LISTEN_PORT}/")
            await stop

    def run(
        self,
        command: Tuple[str, List[str]] = None,
        curses_app: Callable = None,
        func: Callable = None,
    ) -> None:
        """run an executable, curses_app or function"""
        if not any([command, curses_app, func]):
            sys.exit("either a command, curses_app, or func is required")
        self._command = command
        self._curses_app = curses_app
        self._func = func
        self._loop = asyncio.get_event_loop()
        stop = self._loop.create_future()
        self._loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
        self._loop.run_until_complete(self._serve(stop))


def sample_draw(scr):
    """quick curses app for testing"""
    scr.border(0)
    scr.addstr(5, 5, "Hello from Curses!", curses.A_BOLD)
    scr.addstr(6, 5, "Press q to close this screen", curses.A_NORMAL)
    while True:
        char = scr.getch()
        if char == ord("q"):
            break


def sample_func():
    """quick func for testing"""
    print("Welcome to the sample func")
    while True:
        txt = input("Type something to test this out or 'quit()': ")
        if txt == "quit()":
            break
        print("You typed: ", txt)


# left here for testing
if __name__ == "__main__":
    WebXtermJs().run(command=("zsh", ["zsh"]))
    WebXtermJs().run(curses_app=sample_draw)
    WebXtermJs().run(func=sample_func)
