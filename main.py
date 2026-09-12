import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def main():
    services = [
        [sys.executable, str(ROOT_DIR / "backend" / "api_server.py")],
        [sys.executable, str(ROOT_DIR / "backend" / "streaming_server" / "send_audio.py")],
    ]

    processes = []
    try:
        for command in services:
            processes.append(subprocess.Popen(command, cwd=ROOT_DIR))

        print("FaceChat services started.")
        print("Open http://127.0.0.1:5000 in your browser.")
        print("Press Ctrl+C to stop all local services.")

        for process in processes:
            return_code = process.wait()
            if return_code != 0:
                raise RuntimeError(
                    f"A FaceChat service exited unexpectedly with code {return_code}."
                )
    except KeyboardInterrupt:
        print("\nStopping FaceChat services...")
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    main()
