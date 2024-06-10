import csv
import xml.etree.ElementTree as ET
import sys
import os
import string
import random
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
import configparser

def current_time_date():
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    return current_time


def current_date():
    current_datetime = datetime.now()
    date_only = current_datetime.date()
    formatted_date = date_only.strftime('%Y-%m-%d')
    return formatted_date


def generate_payment_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(32))

def generate_sepa(csv_file, debitor_name, debitor_iban, debitor_bic):

    controlSum = 0
    numOfTx = 0
    

    with open(csv_file,  'r', newline='') as f:
        # reader = csv.DictReader(f)

        # Create the root element for the SEPA XML
        xml =  '<?xml version="1.0" encoding="utf-8"?>\n'
        sepa = ET.Element('Document')
        sepa.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        sepa.set('xmlns', "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03")
        
        CstmrCdtTrfInitn = ET.SubElement(sepa,'CstmrCdtTrfInitn')
        GrpHdr = ET.SubElement(CstmrCdtTrfInitn,'GrpHdr')

        # Generates random payment id 
        MsgId = ET.SubElement(GrpHdr,'MsgId')
        MsgId.text = "Vendor Payment"
        # Use current time and date as creditor time
        CreDtTm = ET.SubElement(GrpHdr,'CreDtTm')
        CreDtTm.text = current_time_date()
        NbOfTxs = ET.SubElement(GrpHdr,'NbOfTxs')
        CtrlSum = ET.SubElement(GrpHdr,'CtrlSum')
        InitgPty = ET.SubElement(GrpHdr,'InitgPty')

        Id = ET.SubElement(InitgPty,"Id")
        OrgId = ET.SubElement( Id , "OrgId")
        Othr = ET.SubElement(OrgId, "Othr")
        Id = ET.SubElement(Othr, "Id")
        Id.text = "IE33SCT844793"

        # Nm = ET.SubElement(InitgPty,'Nm')
        # Nm.text = debitor_name.upper()

        r = csv.reader(f)
        headers = next(r)  # Read the header row

        data = []
        for row in r:
        # Create a dictionary for each row using zip() and headers
            record = dict(zip(headers, row))
            data.append(record)
        print(data)
        index = 0

        PmtInf = ET.SubElement(CstmrCdtTrfInitn,'PmtInf')
        PmtInfId = ET.SubElement(PmtInf,'PmtInfId')
       

        PmtInfId.text = "Block 1"
        PmtMtd = ET.SubElement(PmtInf, "PmtMtd")
        PmtMtd.text= "TRF"
        NbOfTxs2 = ET.SubElement(PmtInf, "NbOfTxs")
        CtrlSum2 = ET.SubElement(PmtInf,"CtrlSum")

        PmtTpInf = ET.SubElement(PmtInf,"PmtTpInf" )
        SvcLvl = ET.SubElement(PmtTpInf, "SvcLvl")
        Cd = ET.SubElement(SvcLvl, "Cd")  
        Cd.text = "SEPA"     

        ReqdExctnDt = ET.SubElement(PmtInf, "ReqdExctnDt")
        today = current_date()
        ReqdExctnDt.text = today

   
            
        Dbtr = ET.SubElement(PmtInf,'Dbtr')
        Nm = ET.SubElement(Dbtr,'Nm')
        Nm.text = debitor_name
        PstlAdr = ET.SubElement(Dbtr, "PstlAdr")
        Ctry = ET.SubElement(PstlAdr, "Ctry")
        Ctry.text = "IE" # need to add client information
        AdrLine =  ET.SubElement(PstlAdr, "AdrLine")
        AdrLine.text = 'Unit C1, Three Rock Road' # need to add client information
        AdrLine =  ET.SubElement(PstlAdr, "AdrLine")
        AdrLine.text = "Sandyford Business Park,Dublin,D18N9P6,Ireland" # need to add client information


            
        DbtrAcct = ET.SubElement(PmtInf,'DbtrAcct')
        Id = ET.SubElement(DbtrAcct,'Id')
        IBAN = ET.SubElement(Id,'IBAN')
        IBAN.text = debitor_iban
        Ccy = ET.SubElement(DbtrAcct, "Ccy")
        Ccy.text = "EUR"
            
        DbtrAgt = ET.SubElement(PmtInf,'DbtrAgt')
        FinInstnId = ET.SubElement(DbtrAgt,'FinInstnId')
        BIC = ET.SubElement(FinInstnId,'BIC')
        BIC.text = debitor_bic

        ChrgBr = ET.SubElement(PmtInf, "ChrgBr")
        ChrgBr.text = "SLEV"
        
        for vendor_info in data:
            numOfTx += 1 


            # Creditor information started
            CdtTrfTxInf = ET.SubElement(PmtInf,'CdtTrfTxInf')

            PmtId = ET.SubElement(CdtTrfTxInf, "PmtId")
            EndToEndId = ET.SubElement(PmtId, "EndToEndId")
            EndToEndId.text = vendor_info.get("Remittance_Info")

            Amt = ET.SubElement(CdtTrfTxInf,'Amt')

            InstdAmt = ET.SubElement(Amt,'InstdAmt', Ccy='EUR')
           
            payment = float(vendor_info.get('Payment_Amount'))
            payment = Decimal(payment).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
            print("payment", payment)
            InstdAmt.text =str(payment)
           
            controlSum += payment


            CdtrAgt = ET.SubElement(CdtTrfTxInf,'CdtrAgt')
            


            Cdtr = ET.SubElement(CdtTrfTxInf,'Cdtr')

           

            
            
            
            FinInstnId = ET.SubElement(CdtrAgt,'FinInstnId')
            BIC = ET.SubElement(FinInstnId,'BIC')



            BIC.text = vendor_info.get("Creditor_BIC")


            Nm = ET.SubElement(Cdtr,'Nm')
            Nm.text = vendor_info.get("Supplier_Name")
            PstlAdr = ET.SubElement(Cdtr,'PstlAdr')
            AdrLine = ET.SubElement(PstlAdr,'AdrLine')
            AdrLine.text = vendor_info.get("Address1")
            AdrLine = ET.SubElement(PstlAdr,'AdrLine')
            AdrLine.text = vendor_info.get("Address2")

            CdtrAcct = ET.SubElement(CdtTrfTxInf,'CdtrAcct')
            Id = ET.SubElement(CdtrAcct,'Id')
            IBAN = ET.SubElement(Id,'IBAN')
            IBAN.text = vendor_info.get("Creditor_IBAN")
            
            
            

        # RmtInf = ET.SubElement(PmtInf,'RmtInf')
        # Ustrd = ET.SubElement(RmtInf,'Ustrd')
        # Ustrd.text = "Vendor_Payment"

        # Store number of transactions
        NbOfTxs2.text  =  str(numOfTx)
        CtrlSum2.text =  str(controlSum)
       
        NbOfTxs.text = str(numOfTx)

        # Control sum (total transfer amount)
        
        CtrlSum.text = str(controlSum)
            
        # Create the SEPA XML string
        sepa_xml = ET.tostring(sepa, encoding='unicode')

    # Save the SEPA XML to a file in the same directory as the CSV file
    filename, file_extension = os.path.splitext(csv_file)
    sepa_xml_file = filename + '.xml'
    with open(sepa_xml_file, 'w') as f:
        f.write(sepa_xml)



csv_file = "VendorPayment.csv"  
debitor_name = "Action Alarms Ltd"
debitor_iban = "IE79AIBK93339229596275"  # Note: Likely not a valid IBAN format
debitor_bic = "AIBKIE2D"

generate_sepa(csv_file, debitor_name, debitor_iban, debitor_bic)
