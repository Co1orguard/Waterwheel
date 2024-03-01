from procmon_parser import ProcmonLogsReader

def parse_procmon_output(file_path):
    with open(file_path, 'rb') as f:
        reader = ProcmonLogsReader(f)
        for row in reader:
            if row.operation == 'WriteFile':
                print(row)

parse_procmon_output("./output.PML")