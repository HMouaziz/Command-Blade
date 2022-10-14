import os
import csv


def mk_dict_from(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        command_database = dict((rows[0], rows[1]) for rows in reader)
    return command_database


def mk_list_from(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        command_list = list((rows[0]) for rows in reader)
    return command_list


def run_ipconfig(parameter="", value=""):
    print(f"ipconfig {parameter} {value}")
    os.system(f"ipconfig {parameter} {value}")


