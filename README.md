---
title: MediaFlow Proxy
emoji: 🎥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8888
pinned: false
license: mit
thumbnail: >-
  https://cdn.githubraw.com/mhdzumair/mediaflow-proxy/main/mediaflow_proxy/static/logo.png
---


# MediaFlow Proxy

<div style="text-align: center;">
  <img src="https://cdn.githubraw.com/mhdzumair/mediaflow-proxy/main/mediaflow_proxy/static/logo.png" alt="MediaFlow Proxy Logo" width="200" style="border-radius: 15px;">
</div>

MediaFlow Proxy is a powerful and flexible solution for proxifying various types of media streams. It supports HTTP(S) links, HLS (M3U8) streams, and MPEG-DASH streams, including DRM-protected content. This proxy can convert MPEG-DASH DRM-protected streams to decrypted HLS live streams in real-time, making it one of the fastest live decrypter servers available.

## Features

- Convert MPEG-DASH streams (DRM-protected and non-protected) to HLS
- Support for Clear Key DRM-protected MPD DASH streams
- Support for non-DRM protected DASH live and VOD streams
- Proxy HTTP/HTTPS links with custom headers
- Proxy and modify HLS (M3U8) streams in real-time with custom headers and key URL modifications for bypassing some sneaky restrictions.
- Retrieve public IP address of the MediaFlow Proxy server for use with Debrid services
- Support for HTTP/HTTPS/SOCKS5 proxy forwarding
- Protect against unauthorized access and network bandwidth abuses
- Support for play expired or self-signed SSL certificates server streams `(verify_ssl=false)` default is `false`
- Flexible request proxy usage control per request `(use_request_proxy=true/false)` default is `true`
- Obfuscating endpoint parameters by encrypting them to hide sensitive information from third-party.
- Optional IP-based access control restriction & expiration for encrypted URLs to prevent unauthorized access

## Configuration

Set the following environment variables:

- `API_PASSWORD`: Required. Protects against unauthorized access and API network abuses.
- `PROXY_URL`: Optional. HTTP/HTTPS/SOCKS5 proxy URL for forwarding network requests.
- `ENABLE_STREAMING_PROGRESS`: Optional. Enable streaming progress logging. Default is `false`.

## Installation

### Option 1: Self-Hosted Deployment

#### Using Docker from Docker Hub

1. Pull & Run the Docker image:
   ```
   docker run -p 8888:8888 -e API_PASSWORD=your_password mhdzumair/mediaflow-proxy
   ```

#### Using pip

> [!IMPORTANT]  
> Ensure that you have Python 3.10 or higher installed.

1. Install the package:
   ```
   pip install mediaflow-proxy
   ```

2. Set the `API_PASSWORD` and other environment variables in `.env`:
   ```
   echo "API_PASSWORD=your_password" > .env
   ```

3. Run the MediaFlow Proxy server:
   ```
   mediaflow-proxy
   ```
   You can access the server at `http://localhost:8888`.

4. To run the server with uvicorn options: (Optional)
   ```
   uvicorn mediaflow_proxy.main:app --host 0.0.0.0 --port 8888 --workers 4
   ```


#### Using git & poetry

> [!IMPORTANT]  
> Ensure that you have Python 3.10 or higher installed.


1. Clone the repository:
   ```
   git clone https://github.com/mhdzumair/mediaflow-proxy.git
   cd mediaflow-proxy
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set the `API_PASSWORD` environment variable in `.env`:
   ```
   echo "API_PASSWORD=your_password" > .env
   ```

4. Run the FastAPI server:
   ```
   poetry run uvicorn mediaflow_proxy.main:app --host 0.0.0.0 --port 8888 --workers 4
   ```


#### Build and Run Docker Image Locally

1. Build the Docker image:
   ```
   docker build -t mediaflow-proxy .
   ```

2. Run the Docker container:
   ```
   docker run -d -p 8888:8888 -e API_PASSWORD=your_password --restart unless-stopped --name mediaflow-proxy mediaflow-proxy
   ```

### Option 2: Premium Hosted Service (ElfHosted)
<div style="text-align: center;">
  <img src="https://store.elfhosted.com/wp-content/uploads/2024/08/mediaflow-proxy.jpg" alt="ElfHosted Logo" width="200" style="border-radius: 15px;">
</div>
For a hassle-free, high-performance deployment of MediaFlow Proxy, consider the premium hosted service through ElfHosted.

To purchase:
1. Visit [https://store.elfhosted.com/product/mediaflow-proxy](https://store.elfhosted.com/product/mediaflow-proxy)
2. Follow ElfHosted's setup instructions

Benefits:
- Instant setup and automatic updates
- High performance and 24/7 availability
- No server maintenance required

Ideal for users who want a reliable, plug-and-play solution without the technical overhead of self-hosting.

### Option 3: Hugging Face Space Deployment

1. Visit the HF Space: [mhdzumair/mediaflow-proxy](https://huggingface.co/spaces/mhdzumair/mediaflow-proxy)
2. Click on three dots on the right side of the page and select "Duplicate Space"
3. Set the `API_PASSWORD` secret value & Set Visibility to "Public"
4. Click on "Duplicate Space" to deploy the API

## Usage

### Endpoints

1. `/proxy/hls/manifest.m3u8`: Proxify HLS streams
2. `/proxy/stream`: Proxy generic http video streams
3. `/proxy/mpd/manifest.m3u8`: Process MPD manifests
4. `/proxy/mpd/playlist.m3u8`: Generate HLS playlists from MPD
5. `/proxy/mpd/segment.mp4`: Process and decrypt media segments
6. `/proxy/ip`: Get the public IP address of the MediaFlow Proxy server

Once the server is running, for more details on the available endpoints and their parameters, visit the Swagger UI at `http://localhost:8888/docs`.

### Examples

#### Proxy HTTPS Stream (without using configured proxy)

```bash
mpv "http://localhost:8888/proxy/stream?d=https://jsoncompare.org/LearningContainer/SampleFiles/Video/MP4/sample-mp4-file.mp4&api_password=your_password&use_request_proxy=false"
```

#### Proxy HTTPS self-signed certificate Stream

```bash
mpv "http://localhost:8888/proxy/stream?d=https://self-signed.badssl.com/&api_password=your_password&verify_ssl=false"
```


#### Proxy HLS Stream with Headers

```bash
mpv "http://localhost:8888/proxy/hls/manifest.m3u8?d=https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_fmp4/master.m3u8&h_referer=https://apple.com/&h_origin=https://apple.com&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36&api_password=your_password"
```

#### Live DASH Stream (Non-DRM Protected)

```bash
mpv -v "http://localhost:8888/proxy/mpd/manifest.m3u8?d=https://livesim.dashif.org/livesim/chunkdur_1/ato_7/testpic4_8s/Manifest.mpd&api_password=your_password"
```

#### VOD DASH Stream (DRM Protected)

```bash
mpv -v "http://localhost:8888/proxy/mpd/manifest.m3u8?d=https://media.axprod.net/TestVectors/v7-MultiDRM-SingleKey/Manifest_1080p_ClearKey.mpd&key_id=nrQFDeRLSAKTLifXUIPiZg&key=FmY0xnWCPCNaSpRG-tUuTQ&api_password=your_password"
```

Note: The `key` and `key_id` parameters are automatically processed if they're not in the correct format.

### URL Encoding

For players like VLC that require properly encoded URLs, use the `encode_mediaflow_proxy_url` function:

```python
from mediaflow_proxy.utils.http_utils import encode_mediaflow_proxy_url

encoded_url = encode_mediaflow_proxy_url(
    mediaflow_proxy_url="http://127.0.0.1:8888",
    endpoint="/proxy/mpd/manifest.m3u8",
    destination_url="https://media.axprod.net/TestVectors/v7-MultiDRM-SingleKey/Manifest_1080p_ClearKey.mpd",
    query_params={
        "key_id": "nrQFDeRLSAKTLifXUIPiZg",
        "key": "FmY0xnWCPCNaSpRG-tUuTQ",
        "api_password": "your_password"
    },
    request_headers={
        "referer": "https://media.axprod.net/",
        "origin": "https://media.axprod.net",
    }
)

print(encoded_url)

# http://127.0.0.1:8888/proxy/mpd/manifest.m3u8?key_id=nrQFDeRLSAKTLifXUIPiZg&key=FmY0xnWCPCNaSpRG-tUuTQ&api_password=your_password&d=https%3A%2F%2Fmedia.axprod.net%2FTestVectors%2Fv7-MultiDRM-SingleKey%2FManifest_1080p_ClearKey.mpd&h_referer=https%3A%2F%2Fmedia.axprod.net%2F&h_origin=https%3A%2F%2Fmedia.axprod.net
```

This will output a properly encoded URL that can be used with players like VLC.

```bash
vlc "http://127.0.0.1:8888/proxy/mpd/manifest.m3u8?key_id=nrQFDeRLSAKTLifXUIPiZg&key=FmY0xnWCPCNaSpRG-tUuTQ&api_password=dedsec&d=https%3A%2F%2Fmedia.axprod.net%2FTestVectors%2Fv7-MultiDRM-SingleKey%2FManifest_1080p_ClearKey.mpd"
```

### Generating Encrypted URLs

To generate an encrypted URL with optional IP restriction and expiration, Use the `/generate_encrypted_or_encoded_url` endpoint via swagger UI or programmatically as shown below:
```python
import requests

url = "http://localhost:8888/generate_encrypted_or_encoded_url"
data = {
    "mediaflow_proxy_url": "http://localhost:8888",
    "endpoint": "/proxy/mpd/manifest.m3u8",
    "destination_url": "https://media.axprod.net/TestVectors/v7-MultiDRM-SingleKey/Manifest_1080p_ClearKey.mpd",
    "query_params": {
        "key_id": "nrQFDeRLSAKTLifXUIPiZg",
        "key": "FmY0xnWCPCNaSpRG-tUuTQ"
    },
    "request_headers": {
        "referer": "https://media.axprod.net/",
        "origin": "https://media.axprod.net",
    },
    "expiration": 3600,  # URL will expire in 1 hour
    "ip": "123.123.123.123",  # Optional: Restrict access to this IP
    "api_password": "your_password"
}

response = requests.post(url, json=data)
encrypted_url = response.json()["encoded_url"]
print(encrypted_url)
```

You can then use the `encoded_url` in your player or application to access the media stream.


### Using MediaFlow Proxy with Debrid Services and Stremio Addons

MediaFlow Proxy can be particularly useful when working with Debrid services (like Real-Debrid, AllDebrid) and Stremio addons. The `/proxy/ip` endpoint allows you to retrieve the public IP address of the MediaFlow Proxy server, which is crucial for routing Debrid streams correctly.

When a Stremio addon needs to create a video URL for a Debrid service, it typically needs to provide the user's public IP address. However, when routing the Debrid stream through MediaFlow Proxy, you should use the IP address of the MediaFlow Proxy server instead.

Here's how to utilize MediaFlow Proxy in this scenario:

1. If MediaFlow Proxy is accessible over the internet:
   - Use the `/proxy/ip` endpoint to get the MediaFlow Proxy server's public IP.
   - Use this IP when creating Debrid service URLs in your Stremio addon.

2. If MediaFlow Proxy is set up locally:
   - Stremio addons can directly use the client's IP address.


## Future Development

- Add support for Widevine and PlayReady decryption

## Acknowledgements and Inspirations

MediaFlow Proxy was developed with inspiration from various projects and resources:

- [Stremio Server](https://github.com/Stremio/stremio-server) for HLS Proxify implementation, which inspired our HLS M3u8 Manifest parsing and redirection proxify support.
- [Comet Debrid proxy](https://github.com/g0ldyy/comet) for the idea of proxifying HTTPS video streams.
- [mp4decrypt](https://www.bento4.com/developers/dash/encryption_and_drm/), [mp4box](https://wiki.gpac.io/xmlformats/Common-Encryption/), and [devine](https://github.com/devine-dl/devine) for insights on parsing MPD and decrypting Clear Key DRM protected content.
- Test URLs were sourced from:
  - [OTTVerse MPEG-DASH MPD Examples](https://ottverse.com/free-mpeg-dash-mpd-manifest-example-test-urls/)
  - [OTTVerse HLS M3U8 Examples](https://ottverse.com/free-hls-m3u8-test-urls/)
  - [Bitmovin Stream Test](https://bitmovin.com/demos/stream-test)
  - [Bitmovin DRM Demo](https://bitmovin.com/demos/drm)
  - [DASH-IF Reference Player](http://reference.dashif.org/dash.js/nightly/samples/)
- [HLS Protocol RFC](https://www.rfc-editor.org/rfc/rfc8216) for understanding the HLS protocol specifications.
- Claude 3.5 Sonnet for code assistance and brainstorming.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)


## Disclaimer

This project is for educational purposes only. The developers of MediaFlow Proxy are not responsible for any misuse of this software. Please ensure that you have the necessary permissions to access and use the media streams you are proxying.