# SemParar API 

![status](images/working.png) ![release](images/release.png)

A python library to consult your SemParar data such as invoice, invoice total price, registered bank account, etc.

To use this library, it is necessary to install the following packages:
 - Python 2
 - Python argparse
 - Python automatedweb - https://github.com/renanleonellocastro/automatedweb
 - Python datetime
 - Python xml.etree
 - Python prettytable

## Library Usage

To use this library you need to know your registered  **CPF** and **PASSWORD** in the SemParar's system.
You can debug the library using the "**debug=True**" option in the library constructor.

Using this library you can get the following information from your SemParar's toll system:
- Name
- Invoice Due Date
- E-mail
- Mobile Number
- Client Code
- Number of Registered Vehicles
- Blocked Account
- Vehicle Name
- Vehicle Plate Number
- Registered Bank Account
- Address
- Current Invoice Extract
- Current Invoice Total Price
- Last 3 Months Invoice Extract
- Last 3 Months Invoice Total Price

### Initialize the library

```python
from semparar import SemParar

sem_parar = SemParar(cpf="12312312312", password="123123", simulate=False, debug=False)
```

### Get the user name

```python
name = sem_parar.name
```

### Get the invoice due date

```python
due_date = sem_parar.due_date
```

### Get the user e-mail

```python
email = sem_parar.email
```

### Get the user mobile number

```python
mobile_number = sem_parar.mobile_number
```

### Get the client code

```python
client_code = sem_parar.client_code
```

### Get the number of registered vehicles

```python
number_of_vehicles = sem_parar.number_of_vehicles
```

### Get the status of the account (is it blocked?)

```python
blocked = sem_parar.blocked
```

### Get the vehicle name

```python
vehicle_name = sem_parar.vehicle_name
```

### Get the vehicle plate number

```python
vehicle_plate_number = sem_parar.vehicle_plate_number
```

### Get the bank account

```python
bank_account = sem_parar.bank_account
bank_name = bank_account['bank_name']
bank_unit_name = bank_account['bank_unit_name']
bank_unit_number = bank_account['bank_unit_number']
bank_account_number = bank_account['account_number']
bank_account_digit = bank_account['account_digit']
```

### Get the user address

```python
address = sem_parar.address
city = address['city']
state = address['state']
place_name = address['place_name']
place_number = address['place_number']
neighborhood = address['neighborhood']
zip_code = address['zip_code']
```

### Get the current invoice extract

```python
invoice = sem_parar.invoice
for item in invoice:
    description = item['description']
    place_name = item['place_name']
    value = item['value']
```

### Get the current invoice total price

```python
invoice_total_price = sem_parar.invoice_total_price
```

### Get the last 3 months invoice extract (suppose we are in march/2020)

```python
for month in [02, 01, 12]:
    sem_parar.change_invoice_month(month)
    invoice = sem_parar.invoice
    for item in invoice:
        description = item['description']
        place_name = item['place_name']
        value = item['value']
```

### Get the last 3 months invoice total price (suppose we are in march/2020)

```python
for month in [02, 01, 12]:
    sem_parar.change_invoice_month(month)
    invoice_total_price = sem_parar.invoice_total_price
```

## Sample Application (sample_app.py)

In this repository there is a "**sample_app**" directory that contains a simple example on how
to use the 'SemParar API' library.

### Usage
```
renan@computer:~/semparar_api/sample_app$ python2 sample_app.py -h
usage: semparar [-h] [-t] [-e] [-m MONTH] [-d] config

positional arguments:
  config                Xml file with configuration data.

optional arguments:
  -h, --help            show this help message and exit
  -t, --total           Show the total invoice value.
  -e, --extract         Show the invoice extract.
  -m MONTH, --month MONTH
                        Month to get the invoice
  -d, --debug           Execute in debug mode.
```
### Configuration File
  
It is necessary to fill your credentials on the **sample.xml** file to be able to connect to the
SemParar's tolls system.

Substitute the following tags on "**sample_app/sample.xml**" in your local directory:
```xml
 - <cpf>32167592303</cpf> -> <cpf>xxxxxxxxxxx</cpf> (xxxxxxxxxxx = your cpf number)
 - <password>exemplo123</password>-> <password>xxxx</password> (xxxx = your SemParar's password)
```
### Execution

To execute the sample above to get the **invoice extract**, write the following in your terminal:
```sh
python2 sample_app.py -e
```

To execute the sample above to get the **invoice total price**, write the following in your terminal:
```sh
python2 sample_app.py -t
```

## TODO List

- [x] Add option to change month in the sample_app
- [ ] Fill the README.md with samples using different months in sample_app
- [ ] Add the data in each invoice item
- [ ] Test and fix the app for accounts with more than one vehicle
- [ ] Add unit tests
- [ ] Complete the documentation with more samples
