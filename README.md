# httpx-system-certs

This package patches httpx.AsyncClient, httpx.AsyncHTTPTransport, httpx.Client, httpx.HTTPTransport, httpx.Proxy, httpx.create_ssl_context, httpx.delete, httpx.get, httpx.head, httpx.options, httpx.patch, httpx.post, httpx.put, httpx.request and httpx.stream to use system certificates authority store by default allowing the use of self signed certificates.

## Installation

```bash
pip install httpx-system-certs
```

https sites trusted by your device should now also be trusted by httpx by default.

_Note: The package uses a .pth file to make the patching of httpx methods available to the python interpreter. In some environments you might need to apply the patch manually using "import httpx_system_certs" before using httpx in your code._

## Functionnality

This package uses higher order functions to patch httpx methods by providing a default value to ssl.SSLContext type arguments. This is done by inspecting the type annotation of the method's arguments and using the truststore package to create a new SSLContext instance with the system certificates authority store.

## Aknowledgements

This package development was inspired by [Andrew Leech's pip-system-certs package](https://gitlab.com/alelec/pip-system-certs)
