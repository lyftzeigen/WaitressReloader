import time
import subprocess

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

command = ['waitress-serve', '--port=8000', 'start:app']


class PythonFileModifiedHandler(PatternMatchingEventHandler):
    patterns = ["*.py"]
    reload_needed = False

    def on_modified(self, event):
        self.reload_needed = True

    def on_created(self, event):
        self.reload_needed = True

    def on_deleted(self, event):
        self.reload_needed = True

if __name__ == "__main__":
    print('Start waitress-serve reloader...')

    process = subprocess.Popen(command, cwd='.')

    handler = PythonFileModifiedHandler()

    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            if handler.reload_needed:
                print('Reloading waitress...')
                process.kill()
                process = subprocess.Popen(command, cwd='.')
                handler.reload_needed = False
                time.sleep(1)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('Interrupting...')
        observer.stop()
        process.kill()

    observer.join()
