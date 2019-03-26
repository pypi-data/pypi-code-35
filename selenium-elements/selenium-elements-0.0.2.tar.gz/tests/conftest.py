import json
import time
from pathlib import Path

import pytest
from docker import APIClient

INDEX_HTML_PATH = Path.cwd() / "tests" / "index.html"
SELENIUM_STANDALONE_IMAGE = "selenium/standalone-chrome-debug:3.141.59-iron"


@pytest.fixture(scope="session", autouse=True)
def selenium_container():
    client = APIClient()
    image = client.pull(SELENIUM_STANDALONE_IMAGE, stream=True, decode=True)
    client.create_network("network1", driver="bridge")
    networking_config = client.create_networking_config(
        {"network1": client.create_endpoint_config(aliases=["web"])}
    )
    for line in image:
        print(json.dumps(line, indent=4))
    selenium_container = client.create_container(
        SELENIUM_STANDALONE_IMAGE,
        detach=True,
        volumes=["/dev/shm"],
        ports=[4444, 4444, 5900, 5900],
        networking_config=networking_config,
        host_config=client.create_host_config(
            binds={"/dev/shm": {"bind": "/dev/shm", "mode": "rw"}},
            port_bindings={4444: 4444, 5900: 5900},
        ),
    )
    web_container = client.create_container(
        SELENIUM_STANDALONE_IMAGE,
        detach=True,
        working_dir="/www",
        entrypoint="python -m SimpleHTTPServer 8000",
        volumes=[str(INDEX_HTML_PATH)],
        ports=[8000, 8000],
        networking_config=networking_config,
        host_config=client.create_host_config(
            binds={str(INDEX_HTML_PATH): {"bind": "/www/index.html", "mode": "ro"}},
            port_bindings={8000: 8000},
        ),
    )
    client.start(selenium_container)
    client.start(web_container)
    time.sleep(3)
    yield
    client.remove_container(web_container, v=True, force=True)
    client.remove_container(selenium_container, v=True, force=True)
    client.remove_network("network1")
