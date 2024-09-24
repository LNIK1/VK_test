"""
Ex.
python3 script.py 2024-09-10
"""


import os
import sys
import glob
import pandas
import datetime


if __name__ == "__main__":

    file_date = sys.argv[1]
    dataframe_list = []
    cur_date = datetime.datetime.strptime(file_date, '%Y-%m-%d')
    start_date = cur_date - datetime.timedelta(days=7)
    path_to_output = os.path.join('output/', f"{file_date}.csv")
    csv_files = glob.iglob('**/input/*[0-9].csv', recursive=True)

    dates_list = [(start_date + datetime.timedelta(days=n)).strftime('%Y-%m-%d') for n in range(7)]

    required_dates = [csv.split('\\')[1].split('.')[0] for csv in csv_files
                      if csv.split('\\')[1].split('.')[0] in dates_list]

    required_files = [os.path.join('input/', f"{csv}.csv") for csv in required_dates]

    for csv in required_files:
        dataframe_list.append(pandas.read_csv(csv, header=None))

    dataframe = pandas.concat(dataframe_list, ignore_index=True)
    dataframe = dataframe.groupby([0, 1]).size().to_frame('size').reset_index()
    dataframe = dataframe.rename(columns={0: 'email', 1: 'action'})
    dataframe = dataframe.pivot_table(
        index=['email'], columns=['action'], values='size', aggfunc='first', fill_value=0).reset_index()
    dataframe = dataframe.reindex(columns=['email', 'CREATE', 'READ', 'UPDATE', 'DELETE'])
    dataframe = dataframe.rename(columns={
        'CREATE': 'create_count', 'READ': 'read_count', 'UPDATE': 'update_count', 'DELETE': 'delete_count'})
    dataframe.to_csv(path_to_output, index=False)
