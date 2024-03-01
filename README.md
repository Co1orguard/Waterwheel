


## Waterwheel

- A quick demo of using watchdog to monitor a trigger file




### Usage
- `pip install -r requirements.txt`
- `python waterwheel.py`


- you can then edit ./Sensitive/target.txt to see waterwheel altert the file has been changed



### Description

In the event of a trigger, waterwheel will copy over files in `./Backup` to `./Sensitive`.

You'll find some remnants of attempted functionalities I worked on adding to waterwheel in the `./Graveyard` directory. (Don't laugh too hard) 
