import asyncio
import sounddevice as sd
import numpy as np

# Constants
CHANNELS = 1
SAMPLERATE = 16000
FRAME_DURATION_MS = 20
FRAME_SIZE = (SAMPLERATE * FRAME_DURATION_MS) // 1000
DTYPE = "int16"


async def capture_audio():
    """An async generator that yields audio frames from the microphone."""
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status)
        loop.call_soon_threadsafe(queue.put_nowait, indata.copy())

    try:
        with sd.InputStream(
            samplerate=SAMPLERATE,
            channels=CHANNELS,
            dtype=DTYPE,
            blocksize=FRAME_SIZE,
            callback=callback,
        ):
            while True:
                yield await queue.get()
    except Exception as e:
        print(f"Error in audio capture: {e}")

async def main():
    """A simple demo to test audio capture."""
    print("Starting audio capture. Press Ctrl+C to stop.")
    try:
        async for frame in capture_audio():
            print(f"Captured frame of shape {frame.shape} and dtype {frame.dtype}")
            # You can add further processing here
            await asyncio.sleep(0.5) # Simulate work
    except asyncio.CancelledError:
        print("\nAudio capture stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting.")
