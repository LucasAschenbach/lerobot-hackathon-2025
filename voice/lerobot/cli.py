import asyncio
import logging
import click
from audio.capture import capture_audio
from audio.wakeword import WakeWordDetector

@click.group()
def cli():
    """A CLI for LeRobot."""
    pass

@cli.command()
@click.option('--debug', is_flag=True, help="Enable debug logging.")
def listen(debug):
    """Listens for the wake-word and prints 'WAKE!' upon detection."""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s:%(name)s:%(message)s')
    
    print("Starting wake-word detection. Press Ctrl+C to stop.")

    async def _listen():
        detector = WakeWordDetector()
        try:
            async for frame in capture_audio():
                print("Frame received")
                if detector.check(frame):
                    print("WAKE!")
        except asyncio.CancelledError:
            print("\nDetection stopped.")

    try:
        asyncio.run(_listen())
    except KeyboardInterrupt:
        print("Exiting.")

if __name__ == '__main__':
    cli() 