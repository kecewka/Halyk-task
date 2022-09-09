import csv
import time

start_time = time.time()

reader = csv.DictReader(open('BTRecords.csv'))
data = {}

def populate(reader):
    for row in reader:
        date = row.pop('Date')
        desc = row.pop('Description')
        wd = row.pop("Withdrawls")
        
        if date in data.keys():
            if desc in data[date]:
                data[date][desc].append(float(wd.replace(",","")))
            if desc not in data[date]:
                data[date][desc] = [float(wd.replace(",",""))]
        else:
            data[date] = {desc : [float(wd.replace(",",""))]}

    output_list = calculate_by_desc(data)
    write_output(output_list)

def calculate_by_desc(data):
    new_data = []
    low = 0
    big = 0
    avg = 0
    cnt = 0
    all_elems_sum = 0

    low_daily = 0
    big_daily = 0
    avg_daily = 0
    cnt_daily = 0
    all_elems_sum_daily = 0

    for date in data:
        for row in data[date]:

            if min(data[date][row]) < low:
                low = min(data[date][row])

            if min(data[date][row]) < low_daily:
                low_daily = min(data[date][row])

            if max(data[date][row]) > big:
                big = max(data[date][row])

            if max(data[date][row]) > big_daily:
                big_daily = max(data[date][row])

            cnt = len(data[date][row])
            all_elems_sum = sum(data[date][row])
            avg = all_elems_sum/cnt
            new_data.append({"Date" : date, "Description" : row, "min" : low, "max" : big, "avg" : avg})

            cnt_daily += len(data[date][row])
            all_elems_sum_daily += sum(data[date][row])
            avg_daily = all_elems_sum_daily/cnt_daily
            
            low = 0
            big = 0
            avg = 0
            cnt = 0
            all_elems_sum = 0

        new_data.append({"Date" : date, "Description" : "", "min" : low_daily, "max" : big_daily, "avg" : avg_daily})

        low_daily = 0
        big_daily = 0
        avg_daily = 0
        cnt_daily = 0
        all_elems_sum_daily = 0

    return(new_data)


def write_output(new_data):
    headers = ['Date', 'Description', 'min', 'max', 'avg']
    with open('pure_output_sorted.csv','w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(new_data)

populate(reader)
print(time.time() - start_time)
