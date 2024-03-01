from colorama import init
init()


import schedule
import re
import os
import signal
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from termcolor import colored
 
# Define the directory to watch
watch_directory = "."
 
# Define the trigger file
trigger_file = './Sensitive/target.txt'
 
# Define your source directory and backup directory
src_directory = "./Sensitive"
backup_directory = "./Backup"
 
def backup_files(src_dir, backup_dir):
    # Copy all files from src_dir to backup_dir
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        if os.path.isfile(file_path):
            shutil.copy2(file_path, backup_dir)
 
def restore_files(src_dir, backup_dir):
    # Restore all files from backup_dir to src_dir
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.path.isfile(file_path):
            shutil.copy2(file_path, src_dir)
            
            print(colored("Restoring: " + file_path, 'green'))
            
    # Restore the trigger file
    

class Handler(FileSystemEventHandler):
    def on_deleted(self, event):
        if re.match(".*target.txt",event.src_path):
            print(colored("\n\n\n==================================", 'red'))
            print(colored(f"Trigger file has been deleted: {event.src_path}", 'red'))
            print(colored("==================================", 'red'))
            restore_files(src_directory, backup_directory)
    
    def on_modified(self, event):
        # Check if the modified file is the trigger file
        #print("Trigger_File = ", trigger_file)
        #print("Edited_File = ", event.src_path)
        if re.match(".*target.txt",event.src_path):
            # Get the modification time of the trigger file and the backup file
            trigger_time = os.path.getmtime(trigger_file)
            backup_time = os.path.getmtime(os.path.join(backup_directory, 'target.txt'))
            # If the modification times are not the same, restore the files
            if trigger_time != backup_time:
                print(colored("\n\n\n==================================", 'red'))
                print(colored(f"Trigger file has been modified: {event.src_path}", 'red'))
                print(colored("==================================", 'red'))
                restore_files(src_directory, backup_directory)
                
            # Get the PID of the process that last modified the file
            # pid = int(os.popen(f"lsof -t {trigger_file}").read().strip())
            #print(f"Killing process: {pid}")
            # Kill the process
            #os.kill(pid, signal.SIGKILL)
            # Restore the files from backup

# Backup files before starting the observer
schedule.every(1).minutes.do(backup_files, src_directory, backup_directory)



event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, watch_directory, recursive=True)
backup_files(src_directory, backup_directory)
observer.start()
 
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
