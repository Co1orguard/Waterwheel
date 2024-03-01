import wmi

# Initialize the WMI interface
c = wmi.WMI()

# Specify the directory that contains the file to monitor
watched_dir = r"./Sensitive/target.txt"

# Specify the name of the file to monitor
watched_file = "target.txt"

# Create a query to watch for file change events
watcher = c.watch_for(
    notification_type="Operation",
    wmi_class="CIM_DirectoryContainsFile",
    delay_secs=1,
    Directory=watched_dir
)

# Loop forever, printing a message whenever the watched file is changed
while True:
    file_changed = watcher()
    if file_changed.FileName == watched_file:
        print(f"File {watched_file} in {watched_dir} was changed")