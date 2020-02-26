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

class failedtofillinvoicedata(Exception):
    """Error while filling the invoice data"""
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
        self.__last_invoices_code = ['','','']
        self.__vehicle_name = ''
        self.__vehicle_plate_number = ''
        self.__bank_account = {'bank_name':'', 'bank_unity_name':'', 'bank_unity_number':'',
                             'account_number':'', 'account_digit':''}
        self.__address = {'city':'', 'state':'', 'place_name':'', 'place_number':'',
                        'neighborhood':'', 'zip_code':''}
        self.__invoice_numbers = {'first':'', 'second':'', 'third':''}
        self.__invoice = []
        self.__invoice_total_price = None
        self.__month = datetime.now().month
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

# Get the three last invoice numbers
#----------------------------------------------------------------------------------------------------------------------
    @property
    def invoice_numbers(self):
        logging.debug('Getting the last three invoice numbers...')
        if(not self.__logged):
            self.__login()

        if (self.__invoice_numbers['first'] != ''):
            logging.debug('Returning the invoice numbers: %s %s %s!', self.__invoice_numbers['first'],
                self.__invoice_numbers['second'], self.__invoice_numbers['third'])
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
            self.__invoice_numbers['first'] = result[0]['numeroFatura']
            self.__invoice_numbers['second'] = result[1]['numeroFatura']
            self.__invoice_numbers['third'] = result[2]['numeroFatura']
        except:
            logging.error('Failed to get the last invoice numbers!')
            raise FailedToFillInvoiceNumbers
            
        logging.debug('Returning the invoice numbers: %s %s %s!', self.__invoice_numbers['first'],
            self.__invoice_numbers['second'], self.__invoice_numbers['third'])
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
        data = {'tipoUso':None, 'statusItemFaturamento':4, 'quantidade':100, 'indice':1, 'codigoFatura':None,
            'dataInicialUnix':None, 'dataFinalUnix':None, 'placaVeiculo':None}
        try:
            self.__web.executePost(self.INVOICE_URL, data, True, header)
        except:
            logging.error('Failed to connect to get invoice data!')
            raise FailedToConnect

        try:
            self.__fill_user_extract_properties(json.loads(self.__web.getCurrentPage()))
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
        self.__bank_account['bank_unity_name'] = properties['dadosFinanceiros']['contaCorrente']['nomeAgencia']
        self.__bank_account['bank_unity_number'] = properties['dadosFinanceiros']['contaCorrente']['identificadorAgencia']
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
        self.__vehicle_name = properties['itemFaturas'][0]['modeloVeiculo'] 
        self.__vehicle_plate_number = properties['itemFaturas'][0]['placaVeiculo']
        self.__invoice_total_price = properties['valorTotal']
        self.__invoices = []
        for invoice in properties['itemFaturas']:
            description = invoice['descricaoItemFatura'].encode('utf-8')
            place_name = invoice['nomePontoUso'].encode('utf-8') + "/" + invoice['nomePraca'].encode('utf-8')
            value = invoice['valorBrutoFatura']
            self.__invoice.append({'description':description, 'place_name':place_name, 'value':value})

        logging.debug('User %s extract properties filled!', self.cpf)

# Set log level
#----------------------------------------------------------------------------------------------------------------------
    def set_log_level(self, debug):
        if (debug):
            logging.basicConfig(level=1)
            logging.debug('Log debug level activated!')
        else:
            logging.basicConfig(level=logging.INFO)

#----------------------------------------------------------------------------------------------------------------------
