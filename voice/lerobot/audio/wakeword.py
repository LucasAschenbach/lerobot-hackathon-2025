import openwakeword
from openwakeword.model import Model
import numpy as np
import os
import asyncio

# Path to the default wake-word model
# This can be customized or downloaded if not present.
MODEL_PATH = "hey_lerobot.onnx" # Placeholder for custom model

class WakeWordDetector:
    """A wrapper for the openwakeword library."""

    def __init__(self, model_path: str = MODEL_PATH, vad_threshold: float = 0.5):
        # Download models if they don't exist
        if not os.path.exists("openwakeword/resources/models"):
             openwakeword.utils.download_models()

        if not os.path.exists(model_path):
            print(f"Warning: Wake-word model not found at {model_path}. Using default 'hey_lerobot'.")
            # Fallback to a pre-defined model if the custom one isn't available
            self.oww = Model(
                wakeword_models=["hey_mycroft"],
                enable_speex_noise_suppression=False,
                vad_threshold=vad_threshold,
            )
        else:
            self.oww = Model(
                wakeword_models=[model_path],
                enable_speex_noise_suppression=False,
                vad_threshold=vad_threshold,
            )
            
    def check(self, frame: np.ndarray) -> bool:
        """
        Check a single audio frame for the wake-word.

        Args:
            frame: A numpy array of int16 audio data.

        Returns:
            True if the wake-word is detected, False otherwise.
        """
        results = self.oww.predict(frame.flatten())
        # Check the score for our specific model
        # The key in the results dict corresponds to the model name
        if "hey_mycroft" in results and results["hey_mycroft"] > 0.5: # 0.5 is the default threshold
            return True
        model_name = os.path.splitext(os.path.basename(MODEL_PATH))[0]
        if model_name in results and results[model_name] > 0.5: # 0.5 is the default threshold
            return True
        return False

# Example usage
async def main():
    from capture import capture_audio

    print("Listening for wake-word... Press Ctrl+C to stop.")
    
    # Example with VAD enabled
    detector = WakeWordDetector(vad_threshold=0.5)
    
    try:
        async for frame in capture_audio():
            if detector.check(frame):
                print("WAKE-WORD DETECTED!")
    except asyncio.CancelledError:
        print("\nWake-word detection stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting.")
