#!/usr/bin/python

import argparse
from xml.etree import ElementTree
from prettytable import PrettyTable
from semparar import SemParar

# Parse the input arguments
#----------------------------------------------------------------------------------------------------------------------
def parse_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--total", help="Show the total invoice value.", action="store_true")
    parser.add_argument("-e", "--extract", help="Show the invoice extract.", action="store_true")
    parser.add_argument("-m", "--month", help="Month to get the invoice", default=None)
    parser.add_argument("-d", "--debug", help="Execute in debug mode.", action="store_true", default=False)
    parser.add_argument("config", help="Xml file with configuration data.")
    args = parser.parse_args()
    return args

# Read xml data from file
#----------------------------------------------------------------------------------------------------------------------
def xml_read(parse_string, config_file):
    return ElementTree.parse(config_file).findall(parse_string)[0].text

# Print the total invoice value
#----------------------------------------------------------------------------------------------------------------------
def print_total_invoice_value(sem_parar):
    try:
        total = sem_parar.invoice_total_price
    except:
        print ("Error while getting the total invoice price!")
        raise

    print ("Total: %.2f" %total)

# Print the invoice extract
#----------------------------------------------------------------------------------------------------------------------
def print_invoice_extract(sem_parar):
    try:
        invoice = sem_parar.invoice
        total = sem_parar.invoice_total_price
        vehicle = sem_parar.vehicle_name
    except:
        print ("Error processing the invoice!")
        raise

    table = PrettyTable()
    print ('---------------------------------------------------SemParar---------------------------------------------------')
    table.field_names = ["Vehicle", "Place", "Description", "Value"]

    for item in invoice:
        row = []
        row.append(vehicle)
        row.append(item['place_name'])
        row.append(item['description'])
        row.append('%.2f'%item['value'])
        table.add_row(row)

    row = ['TOTAL', '---------------------------------', '---', '%0.2f'%total]
    table.add_row(row)
    print table

# The main application works here
#----------------------------------------------------------------------------------------------------------------------
def main():
    arguments = parse_input_args()
    config_file = arguments.config
    cpf = xml_read("cpf", config_file)
    password = xml_read("password", config_file)
    month = arguments.month
    sem_parar = SemParar(cpf, password, debug=arguments.debug)

    if month:
        try:
            sem_parar.change_invoice_month(int(month))
        except:
            print ("Invalid Month! Currently is just possible to get the last 3 months")
            raise

    if arguments.total:
        print_total_invoice_value(sem_parar)
    
    if arguments.extract:
        print_invoice_extract(sem_parar)

# Starts the app
#----------------------------------------------------------------------------------------------------------------------
main()
