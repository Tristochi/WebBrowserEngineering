def split_url(url):
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https", "file"]

    if scheme == "file":
        url = url[1:]

    if "/" not in url:
        url = url + "/"
    host, url = url.split("/", 1)
    path = "/" + url

    print(f"Scheme: {scheme}")
    print(f"Host: {host}")
    print(f"Path: {path}")

split_url("http://example.org")
split_url("file:///test.txt/")