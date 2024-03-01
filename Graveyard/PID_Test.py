import re
import os
import psutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watch_directory = "./Sensitive/"
file_path = "./Sensitive/target.txt"

class FileEditHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is the trigger file
        #print("Trigger_File = ", trigger_file)
        #print("Edited_File = ", event.src_path)
        if re.match(".*target.txt",event.src_path):
            
            # If the modification times are not the same, restore the files
            
            print(f"Trigger file has been modified: {event.src_path}")
            pid = find_process_using_file(event.src_path)
            print("PID: ", pid)

def find_process_using_file(file_path):
    
    for proc in psutil.process_iter(['pid', 'open_files']):
        try:
            if proc.info['open_files']:
                for item in proc.info['open_files']:
                    #print("PID: ", proc.pid, " Name: ", proc.name(), " File: ", item.path)
                    if re.match(".*target.txt",item.path):
                        return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


event_handler = FileEditHandler()
observer = Observer()
observer.schedule(event_handler, watch_directory, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
