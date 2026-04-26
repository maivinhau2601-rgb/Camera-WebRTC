import aiohttp
import asyncio
from aiortc import RTCPeerConnection,RTCSessionDescription,RTCConfiguration,RTCIceServer
from aiortc.contrib.media import MediaPlayer

RTSP_URL = "rtsp://username:password@local_camera_ip:554/stream1"
SERVER_IP = "x.x.x.x"
WHIP_URL = f"http://{SERVER_IP}:8889/camera1/whip"

async def push_stream():
    rtcconfig = RTCConfiguration(
        iceServers=[RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
    )
    rtcconection = RTCPeerConnection()
    mediaplayer = MediaPlayer(RTSP_URL)

    if mediaplayer.video:
        rtcconection.addTrack(mediaplayer.video)
    else:
        print("Cannot get the camera video")

    offer = await rtcconection.createOffer()
    await rtcconection.setLocalDescription(offer)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            WHIP_URL,
            data=rtcconection.localDescription.sdp,
            headers={"Content-Type": "application/sdp"}
        ) as resp:
            answer_sdp = await resp.text()
            if resp.status != 201:
                print("Error found when initializing WHIP")
                print(answer_sdp)
                return
            await rtcconection.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp,type="answer"))

    # Keep the stream running
    try:
        await asyncio.sleep(3600)
    except KeyboardInterrupt:
        print("Stream interrupted by user.")
    finally:
        print("Closing WebRTC connection.")
        await rtcconection.close()

async def main():
    while True:
        try:
            await push_stream()
        except Exception as e:
            print(f"Error: {e} — reconnecting in 5s...")
            print(WHIP_URL)
            await asyncio.sleep(5)

asyncio.run(main())
