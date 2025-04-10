import time
import httpx
from httpx import get, Client
import sys
import pytest
import subprocess
import asyncio


@pytest.fixture(scope="session", name="simple_server")
def simple_server_fixture():
    process = subprocess.Popen(
        [
            sys.executable,
            "-u",
            "-m",
            "uvicorn",
            "tests.simple_server:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8443",
            "--ssl-keyfile",
            "key.pem",
            "--ssl-certfile",
            "cert.pem",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    pattern = "Application startup complete."
    found_pattern = False
    start = time.time()
    timeout = 5
    allowed_lines = 5
    while not found_pattern:
        if process.poll() is not None:
            raise RuntimeError(
                f"Uvicorn startup failed: Process exited early with code {process.returncode}"
            )
        elif (
            process.stdout is not None
            and (line := process.stdout.readline()) is not None
        ):
            allowed_lines -= 1
            if pattern in line:
                found_pattern = True
                break
            elif allowed_lines == 0:
                raise RuntimeError(
                    "Uvicorn startup failed: Startup pattern not found in the first 5 lines"
                )
        if time.time() - start > timeout:
            process.terminate()
            raise TimeoutError(
                "Uvicorn startup failed: Timed out waiting for startup pattern"
            )

    yield "https://localhost:8443"
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


class TestHttpxCreateSSLContext:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.get(
                simple_server, verify=httpx.create_ssl_context(verify=True)
            ).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.create_ssl_context() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.get(simple_server, verify=httpx.create_ssl_context()).is_success, (
            "httpx.create_ssl_context() patch failed"
        )


class TestHttpxDelete:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.delete(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.delete() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.delete(simple_server).is_success, "httpx.delete() patch failed"


class TestHttpxGet:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.get(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.get() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.get(simple_server).is_success, "httpx.get() patch failed"


class TestHttpxHead:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.head(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.get() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.head(simple_server).is_success, "httpx.head() patch failed"


class TestHttpxOptions:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.options(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.options() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.options(simple_server).is_success, "httpx.options() patch failed"


class TestHttpxPatch:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.patch(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.patch() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.patch(simple_server).is_success, "httpx.patch() patch failed"


class TestHttpxPost:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.post(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.post() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.post(simple_server).is_success, "httpx.post() patch failed"


class TestHttpxPut:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.put(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.put() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.put(simple_server).is_success, "httpx.put() patch failed"


class TestHttpxRequest:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.request("get", simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.request() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert httpx.request("get", simple_server).is_success, (
            "httpx.request() patch failed"
        )


class TestHttpxStream:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            with httpx.stream("get", simple_server, verify=True) as resp:
                resp.is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.stream() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        with httpx.stream("get", simple_server) as resp:
            assert resp.is_success, "httpx.stream() patch failed"


class TestHttpxAsyncClient:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            asyncio.run(httpx.AsyncClient(verify=True).get(simple_server))
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.AsyncClient() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        resp = asyncio.run(httpx.AsyncClient().get(simple_server))
        assert resp.is_success, "httpx.AsyncClient() patch failed"


class TestHttpxAsyncHTTPTransport:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            asyncio.run(
                httpx.AsyncClient(
                    transport=httpx.AsyncHTTPTransport(verify=True), verify=True
                ).get(simple_server)
            )
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.AsyncHTTPTransport() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        resp = asyncio.run(
            httpx.AsyncClient(transport=httpx.AsyncHTTPTransport()).get(simple_server)
        )
        assert resp.is_success, "httpx.AsyncHTTPTransport() patch failed"


class TestHttpxClient:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.Client(verify=True).get(simple_server)
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.Client() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        resp = httpx.Client().get(simple_server)
        assert resp.is_success, "httpx.Client() patch failed"


class TestHttpxHTTPTransport:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            httpx.Client(transport=httpx.HTTPTransport(verify=True), verify=True).get(
                simple_server
            )
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.HTTPTransport() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        resp = httpx.Client(transport=httpx.HTTPTransport()).get(simple_server)
        assert resp.is_success, "httpx.HTTPTransport() patch failed"


class TestHttpxProxy:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            ssl_context = httpx.Proxy(
                simple_server, ssl_context=httpx.create_ssl_context(verify=True)
            ).ssl_context
            if ssl_context is None:
                raise RuntimeError("SSL context is None")
            httpx.get(simple_server, verify=ssl_context).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "httpx.Proxy() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        ssl_context = httpx.Proxy(
            simple_server, ssl_context=httpx.create_ssl_context()
        ).ssl_context
        if ssl_context is None:
            raise RuntimeError("SSL context is None")
        assert httpx.get(simple_server, verify=ssl_context).is_success, (
            "httpx.Proxy() patch failed"
        )


class TestFromHttpxImportGet:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            get(simple_server, verify=True).is_success
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "get() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        assert get(simple_server).is_success, "get() patch failed"


class TestFromHttpxImportClient:
    def test_server(self, simple_server):
        with pytest.raises(httpx.ConnectError) as excinfo:
            Client(verify=True).get(simple_server)
        assert isinstance(excinfo.value, httpx.ConnectError), (
            "Client() worked without httpx_system_certs"
        )

    def test_patch(self, simple_server):
        resp = Client().get(simple_server)
        assert resp.is_success, "Client() patch failed"
