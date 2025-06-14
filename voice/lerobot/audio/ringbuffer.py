from collections import deque
import numpy as np

class RingBuffer:
    """A simple ring buffer using a deque."""

    def __init__(self, capacity_seconds: int, samplerate: int, frame_size: int):
        self.capacity_frames = (capacity_seconds * samplerate) // frame_size
        self._buffer = deque(maxlen=self.capacity_frames)
        self._samplerate = samplerate
        self._frame_size = frame_size

    def extend(self, frame: np.ndarray):
        """Add a new frame to the buffer."""
        if frame.shape[0] != self._frame_size:
            raise ValueError(f"Invalid frame size: expected {self._frame_size}, got {frame.shape[0]}")
        self._buffer.append(frame)

    def get_all(self) -> np.ndarray:
        """Return all frames in the buffer as a single numpy array."""
        return np.concatenate(list(self._buffer))

    @property
    def is_full(self) -> bool:
        """Check if the buffer is full."""
        return len(self._buffer) == self.capacity_frames

    def __len__(self):
        return len(self._buffer)

# Example usage
async def main():
    import asyncio
    from lerobot.audio.capture import capture_audio, SAMPLERATE, FRAME_SIZE

    print("Testing RingBuffer with live audio. Press Ctrl+C to stop.")
    
    # 2-second buffer
    buffer = RingBuffer(capacity_seconds=2, samplerate=SAMPLERATE, frame_size=FRAME_SIZE)

    try:
        async for frame in capture_audio():
            buffer.extend(frame)
            print(f"Buffer size: {len(buffer)}/{buffer.capacity_frames} frames", end='\r')
            if buffer.is_full:
                print("\nBuffer is full. All frames concatenated have shape:", buffer.get_all().shape)
                break
    except asyncio.CancelledError:
        print("\nTest stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting.")
