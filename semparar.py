#!/usr/bin/python

import json
import logging
from datetime import datetime
from automatedweb import AutomatedWeb

class FailedToConnect(Exception):
    """Failed to connect to SEM-PARAR system"""
    pass

class CpfOrPasswordIncorrect(Exception):
    """Invalid CPF or Password in SEM-PARAR system"""
    pass

class FailedToFillInvoiceNumbers(Exception):
    """Error while filling the invoice numbers"""
    pass

class FailedToFillInvoiceData(Exception):
    """Error while filling the invoice data"""
    pass

class InvalidMonth(Exception):
    """Error trying to set an invalid month"""
    pass

class SemParar:

# Constants api URLs
#----------------------------------------------------------------------------------------------------------------------
    LOGIN_URL="https://minhaconta.semparar.com.br/minhaconta/api/login"
    INVOICE_SUMMARY_URL="https://minhaconta.semparar.com.br/minhaconta/api/faturaResumido"
    INVOICE_URL="https://minhaconta.semparar.com.br/minhaconta/api/movimentacaoCliente"

# Initialize the class with its properties
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, cpf, password, simulate=False, debug=False):
        self.__simulate = simulate
        self.__cpf = cpf
        self.__password = password
        self.__web = AutomatedWeb(debug=debug)
        self.__logged = False
        self.__name = ''
        self.__due_date = ''
        self.__email = ''
        self.__mobile_number = ''
        self.__client_code = ''
        self.__number_of_vehicles = ''
        self.__blocked = False
        self.__vehicle_name = ''
        self.__vehicle_plate_number = ''
        self.__bank_account = {'bank_name':'', 'bank_unit_name':'', 'bank_unit_number':'',
                             'account_number':'', 'account_digit':''}
        self.__address = {'city':'', 'state':'', 'place_name':'', 'place_number':'',
                        'neighborhood':'', 'zip_code':''}
        month1 = self.month_number_from_any_number(datetime.now().month - 3) 
        month2 = self.month_number_from_any_number(datetime.now().month - 2) 
        month3 = self.month_number_from_any_number(datetime.now().month - 1) 
        month4 = datetime.now().month
        self.__invoice_numbers = {'%d'%month1: '', '%d'%month2: '', '%d'%month3: '', '%d'%month4:''}
        self.__invoice = []
        self.__invoice_total_price = None
        self.__month = None
        self.set_log_level(debug)

# Get class member "cpf"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def cpf(self):
        logging.debug('Returning the user cpf: %s!', self.__cpf)
        return self.__cpf

# Get class member "name"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        logging.debug('Getting the user name...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user name: %s!', self.__name)
        return self.__name

# Get class member "due_date"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def due_date(self):
        logging.debug('Getting the user due date...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user due date: %s!', self.__due_date)
        return self.__due_date

# Get class member "email"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def email(self):
        logging.debug('Getting the user email...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user email: %s!', self.__email)
        return self.__email

# Get class member "mobile_number"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def mobile_number(self):
        logging.debug('Getting the user mobile number...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user mobile number: %s!', self.__mobile_number)
        return self.__mobile_number

# Get class member "client_code"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def client_code(self):
        logging.debug('Getting the user client code...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user client code: %s!', self.__client_code)
        return self.__client_code

# Get class member "number_of_vehicles"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def number_of_vehicles(self):
        logging.debug('Getting the user number of vehicles...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user number of vehicles: %s!', self.__number_of_vehicles)
        return self.__number_of_vehicles

# Get class member "blocked"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def blocked(self):
        logging.debug('Getting the user blocked...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user blocked: %s!', self.__blocked)
        return self.__blocked

# Get class member "vehicle_name"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def vehicle_name(self):
        logging.debug('Getting the vehicle name...')
        if(not self.__logged):
            self.__login()
        if(len(self.__invoice) == 0):
            self.__get_invoice(self.__month)

        logging.debug('Returning the vehicle name: %s!', self.__vehicle_name)
        return self.__vehicle_name

# Get class member "vehicle_plate_number"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def vehicle_plate_number(self):
        logging.debug('Getting the vehicle plate number...')
        if(not self.__logged):
            self.__login()
        if(len(self.__invoice) == 0):
            self.__get_invoice(self.__month)

        logging.debug('Returning the vehicle plate number: %s!', self.__vehicle_plate_number)
        return self.__vehicle_plate_number

# Get class member "bank_account"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def bank_account(self):
        logging.debug('Getting the user bank account...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user bank account: %s!', self.__bank_account)
        return self.__bank_account

# Get class member "address"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def address(self):
        logging.debug('Getting the user address...')
        if(not self.__logged):
            self.__login()

        logging.debug('Returning the user address: %s!', self.__address)
        return self.__address

# Get class member "invoice"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def invoice(self):
        logging.debug('Getting the user invoice...')
        if(not self.__logged):
            self.__login()
        if(len(self.__invoice) == 0):
            self.__get_invoice(self.__month)

        logging.debug('Returning the user invoice!')
        return self.__invoice

# Get class member "invoice_total_price"
#----------------------------------------------------------------------------------------------------------------------
    @property
    def invoice_total_price(self):
        logging.debug('Getting the user invoice total price...')
        if(not self.__logged):
            self.__login()
        if(len(self.__invoice) == 0):
            self.__get_invoice(self.__month)

        logging.debug('Returning the user invoice total price!')
        return self.__invoice_total_price

# Get the three last invoice numbers
#----------------------------------------------------------------------------------------------------------------------
    @property
    def invoice_numbers(self):
        logging.debug('Getting the last four invoice numbers...')
        month1 = self.month_number_from_any_number(datetime.now().month - 3) 
        month2 = self.month_number_from_any_number(datetime.now().month - 2) 
        month3 = self.month_number_from_any_number(datetime.now().month - 1) 
        month4 = datetime.now().month
        if(not self.__logged):
            self.__login()

        if (self.__invoice_numbers['%d'%month1] != ''):
            logging.debug('Returning the invoice numbers: %s %s %s %s!', self.__invoice_numbers['%d'%month1],
                self.__invoice_numbers['%d'%month2], self.__invoice_numbers['%d'%month3], 
                self.__invoice_numbers['%d'%month4])
            return self.__invoice_numbers

        header = {'content-type': 'application/json;charset=UTF-8'}
        data = {}
        try:
            self.__web.executePost(self.INVOICE_SUMMARY_URL, data, True, header)
        except:
            logging.error('Failed to connect to get the last invoice numbers!')
            raise FailedToConnect

        try:
            result = json.loads(self.__web.getCurrentPage())
            self.__invoice_numbers['%d'%month1] = result[0]['numeroFatura']
            self.__invoice_numbers['%d'%month2] = result[1]['numeroFatura']
            self.__invoice_numbers['%d'%month3] = result[2]['numeroFatura']
            if (len(result) == 4):
                self.__invoice_numbers['%d'%month4] = result[3]['numeroFatura']
            else:
                self.__invoice_numbers['%d'%month4] = None

        except:
            logging.error('Failed to get the last invoice numbers!')
            raise FailedToFillInvoiceNumbers
            
        logging.debug('Returning the invoice numbers: %s %s %s!', self.__invoice_numbers['%d'%month1],
            self.__invoice_numbers['%d'%month2], self.__invoice_numbers['%d'%month3])
        return self.__invoice_numbers

# Log in the user with its credentials and fill the user's properties
#----------------------------------------------------------------------------------------------------------------------
    def __login(self):
        logging.debug('Logging in the user %s...', self.cpf)
        header = {'content-type': 'application/json;charset=UTF-8'}
        data = {'login': self.cpf, 'senha': self.__password, 'nome': '', 'tipoCliente': 1}
        try:
            self.__web.executePost(self.LOGIN_URL, data, True, header)
        except:
            logging.error('User %s failed to log in!', self.cpf)
            raise FailedToConnect

        try:
            self.__fill_user_properties(json.loads(self.__web.getCurrentPage()))
        except:
            logging.error('User %s: cpf or password invalid!', self.cpf)
            raise CpfOrPasswordIncorrect 
        
        self.__logged = True
        logging.debug('User %s logged in sucessfully!', self.cpf)

# Get user's invoice data and fill the user's extract properties
#----------------------------------------------------------------------------------------------------------------------
    def __get_invoice(self, month):
        logging.debug('Get user %s invoice data from month %s...', self.cpf, month)
        header = {'content-type': 'application/json;charset=UTF-8'}
        data = {'tipoUso':None, 'statusItemFaturamento':None, 'quantidade':10, 'indice':1, 'codigoFatura':None,
            'dataInicialUnix':None, 'dataFinalUnix':None, 'placaVeiculo':None}
        properties = []
        try:
            if (month == None or (month == datetime.now().month and \
                 self.invoice_numbers['%d'%datetime.now().month] == None)):
                data['statusItemFaturamento'] = 4
            else:
                data['codigoFatura'] = self.invoice_numbers['%d'%month]
                data['statusItemFaturamento'] = None
            
            while True:
                self.__web.executePost(self.INVOICE_URL, data, True, header)
                if (len((json.loads(self.__web.getCurrentPage()))['itemFaturas']) == 0):
                    break
                else:
                    properties.append(json.loads(self.__web.getCurrentPage()))
                    data['indice']+=1
        except:
            logging.error('Failed to connect to get invoice data!')
            raise FailedToConnect

        try:
            self.__fill_user_extract_properties(properties)
        except:
            logging.error('Failed to get invoice data!')
            raise FailedToFillInvoiceData 
        
        logging.debug('User %s got invoice data from month %s sucessfully!', self.cpf, month)

# Log in the user with its credentials and fill the user's properties
#----------------------------------------------------------------------------------------------------------------------
    def __fill_user_properties(self, properties):
        logging.debug('Filling user %s properties...', self.cpf)
        self.__name = properties['usuario'] 
        self.__due_date = properties['dadosFinanceiros']['diaVencimentoConta']
        self.__bank_account['bank_name'] = properties['dadosFinanceiros']['contaCorrente']['banco']['nome']
        self.__bank_account['bank_unit_name'] = properties['dadosFinanceiros']['contaCorrente']['nomeAgencia']
        self.__bank_account['bank_unit_number'] = properties['dadosFinanceiros']['contaCorrente']['identificadorAgencia']
        self.__bank_account['account_number'] = properties['dadosFinanceiros']['contaCorrente']['numeroConta']
        self.__bank_account['account_digit'] = properties['dadosFinanceiros']['contaCorrente']['digito']
        self.__address = {'city':'', 'state':'', 'place_name':'', 'place_number':'',
                        'neighborhood':'', 'zip_code':''}
        self.__address['city'] = properties['dadosFinanceiros']['endereco']['cidade']
        self.__address['state'] = properties['dadosFinanceiros']['endereco']['estado']
        self.__address['place_name'] = properties['dadosFinanceiros']['endereco']['logradouro']
        self.__address['place_number'] = properties['dadosFinanceiros']['endereco']['numero']
        self.__address['neighborhood'] = properties['dadosFinanceiros']['endereco']['bairro']
        self.__address['zip_code'] = properties['dadosFinanceiros']['endereco']['cep']
        self.__email = properties['email']
        self.__mobile_number = properties['celular']
        self.__client_code = properties['codigoCliente']
        self.__number_of_vehicles = properties['quantidadeVeiculos']
        self.__blocked = properties['bloqueado']
        logging.debug('User %s properties filled!', self.cpf)

# Fill user extract properties
#----------------------------------------------------------------------------------------------------------------------
    def __fill_user_extract_properties(self, properties):
        logging.debug('Filling user %s extract properties...', self.cpf)
        if len(properties) != 0:
            self.__vehicle_name = properties[0]['itemFaturas'][0]['modeloVeiculo']
            self.__vehicle_plate_number = properties[0]['itemFaturas'][0]['placaVeiculo']
            self.__invoice_total_price = 0.0
            self.__invoice = []
            for prop in properties:
                for invoice in prop['itemFaturas']:
                    description = invoice['descricaoItemFatura'].encode('utf-8')
                    place_name = invoice['nomePontoUso'].encode('utf-8') + "/" + invoice['nomePraca'].encode('utf-8')
                    value = invoice['valorBrutoFatura']
                    self.__invoice.append({'description':description, 'place_name':place_name, 'value':value})
                    self.__invoice_total_price += value
        else:
            self.__invoice_total_price = 0.0

        logging.debug('User %s extract properties filled!', self.cpf)

# Change the month of the invoice
#----------------------------------------------------------------------------------------------------------------------
    def change_invoice_month(self, month):
        logging.debug('Changing the month to %d...', month)
        if(not self.__logged):
            self.__login()

        try:
            if month == None or month == datetime.now().month or self.invoice_numbers['%d'%month]:
                self.__month = month
                self.__invoice = []
                self.__invoice_total_price = None
        except:
            logging.error('Failed to change month to %d', month)
            raise InvalidMonth

        logging.debug('The current invoice month is: %d', self.__month)

# Return month number from any number
#----------------------------------------------------------------------------------------------------------------------
    def month_number_from_any_number(self, number):
        logging.debug('Getting the month from number %d...', number)
        month = number%12
        month = 12 if month == 0 else month
        logging.debug('Returning the month: %d', month)
        return month

# Set log level
#----------------------------------------------------------------------------------------------------------------------
    def set_log_level(self, debug):
        if (debug):
            logging.basicConfig(level=1)
            logging.debug('Log debug level activated!')
        else:
            logging.basicConfig(level=logging.INFO)

#----------------------------------------------------------------------------------------------------------------------
