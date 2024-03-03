#ANSI X12 to XML

import xml.etree.ElementTree as ET
import xml.dom.minidom
import hashlib

#===============================================================================================
# Array that contains the ansi x12 sections in xml format
xml_elements = []

isa_elements = ["AuthorizationInformationQuality","AuthorizationInformation","SecurityInformationQuality","SecurityInformation",
                "InterchangeSenderIDQualifier","InterchangeSenderID","AuthorizationReceiverIDQualifier","InterchangeReceiverID",
                "InterchangeDate","InterchangeTime","InterchangeStandardID","InterchangeVersionID","InterchangeControlID","AcknowledgementID",
                "TestIndicator","SubElementSeparator"]
gs_elements = ["FunctionalIdentifierCode", "ApplicationSenderCode", "ApplicationReceiverCode", "DataInterchangeDate",
               "DataInterchangeTime", "DataInterchangeControlNumber", "ResponsibilityAgency", "Version"]
st_elements = ["TransactionSetIDCode", "TransactionSetControlNumber"]
beg_elements = ["TransactionSetPurposeCode", "PurchaseOrderTypeCode", "PurchaseOrderNumber", "ReleaseNumber", "Date", "ContractNumber", "AcknowledgementType", "InvoiceTypeCode"]
ref_elements = ["ReferenceIdentificationQualifier", "ReferenceIdentfication", "Description", "ReferenceIdentificationQualifier"]
itd_elements = ["TermsTypeCode", "TermsBasisDateCode", "TermsDiscountPercent", "TermsDiscountDueDate",
                "TermsDiscountDaysDue", "TermsNetDueDate", "TermsNetDays", "TermsDiscountAmount",
                "TermsDeferredDueDate", "DeferredAmountDue", "PercentOfInvoicePayable", "Description"]
dtm_elements = ["DateTimeQualifier", "Time"]
pkg_elements = ["ItemDescriptionTypeCode", "PackagingCharacteristicCode", "AgencyQualifierCode", 
                "PackagingDescriptionCode", "Description", "UnitLoadOptionCode"]
td5_elements = ["RoutingSequenceCode", "IdentificationCodeQualifier", "IdentificationCode", 
                "TransportationMethod", "Routing"]
cur_elements = ["EntityIdentifierCode", "CurrencyCode", "ExchangeRate"]
fob_elements = ["ShipmentMethodofPaymentCode","LocationQualifier","Description","TransportationTermsQualifierCode","TransportationTermsCode","LocationQualifier","Description","RiskofLossQualifier","Description",]
n9_elements = ["ReferenceIdentificationQualifier","ReferenceIdentification","FreeFormDescription","Date",]
msg_elements = ["FreeFormMessageText","PrinterCarriageControlCode","Number",]
per_elements = ["ContactFunctionCode","Name","CommunicationNumberQualifier","CommunicationNumber","CommunicationNumberQualifier","CommunicationNumber","CommunicationNumberQualifier","CommunicationNumber","ContactInquiryReference",]
pid_elements = ["ItemDescriptionType","ProductorProcessCharacteristicCode","AgencyQualifierCode","ProductDescriptionCode","Description","SurfaceLayerPositionCode","SourceSubQualifier","YesNoConditionOrResponseCode","LanguageCode",]
sac_elements = ["AllowanceorChargeIndicator","ServicePromotionAllowance","AgencyQualifierCode","AgencyServicePromotionAllowance","Amount","AllowanceChargePercentQualifier","Percent","Rate","UnitBasisForMeasurement","Quantity","Quantity","AllowanceorChargeMethodofHandlingCode","ReferenceIdentification","OptionNumber","Description","LanguageCode",]
txi_elements = ["TaxTypeCode","MonetaryAmount","Percent","TaxJurisdictionCodeQualifier","TaxJurisdictionCode","TaxExemptCode","RelationshipCode","DollarBasisforPercent","TaxIdentificationNumber","AssignedIdentification",]
sln_elements = ["AssignedIdentification","AssignedIdentification","RelationshipCode","Quantity","UnitorBasisforMeasurementCode","UnitPrice","BasisofUnitPrice","RelationshipGuide","ProductorServiceIDQualifier","ProductorServiceID","ProductorServiceIDQualifierManufacturersName","ProductorServiceIDManufacturersName","ProductorServiceIDQualifierManufacturersPartNumber","ProductorServiceIDManufacturersPartNumber","ProductorServiceIDQualifierRebuildDrawingNumber","ProductorServiceIDRebuildDrawingNumber",]
n1_elements = ["EntityIdentifierCode","Name","IDCodeQualifier","IDCode","EntityRelationshipCode","EntityIdentifierCode",]
n2_elements = ["Name","Name",]
n3_elements = ["AddressInformation","AddressInformation",]
n4_elements = ["CityName","StateOrProvidenceCode","PostalCode","CountryCode","LocationQualifier","LocationIdentifier",]
po5_elements = ["AssignedIdentification","QuantityOrdered","UnitorBasisforMeasurementCode","UnitPrice","BasisofUnitPrice","ProductorServiceIDQualifier","ProductorServiceID","ProductorServiceIDQualifier","ProductorServiceID","ProductorServiceIDQualifier","ProductorServiceID","ProductorServiceIDQualifier","ProductorServiceID",]
ctt_elements = ["NumberofLineItems","HashTotal","Weight","UnitofMeasurementCode","Volume","UnitofMeasurementCode","Description",]
sdq_elements = ["UnitorBasisforMeasurementCode","IdentificationCodeQualifier","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","IdentificationCode","Quantity","LocationIdentifier",]
amt_elements = ["AmountQualifierCode","MonetaryAmount","CreditDebitFlagCode"]

def map_isa(line_elements):
    if len(line_elements) == 0:
        return

    isa_xml = ET.Element("InterchangeControlHeader", InterchangeControlID = line_elements[13] , InterchangeDate =  f"{line_elements[9][:2]}-{line_elements[9][2:4]}-{line_elements[9][4:]}")
    xml_elements.append(isa_xml)

    for i in range(1, len(line_elements)):

        if i == 10 and line_elements[i] != "":
            time_str = line_elements[i]
            time = f"{time_str[:2]}:{time_str[2:]}"
            isa_sub = ET.SubElement(isa_xml, isa_elements[i-1])
            isa_sub.text = time
            

        elif i != 13 and i != 9 and line_elements[i] != "":
            isa_sub = ET.SubElement(isa_xml, isa_elements[i-1])
            isa_sub.text = line_elements[i]

def map_gs(line_elements):
    gs_xml = ET.SubElement(xml_elements[0], "FunctionalGroupHeader", DataInterchangeControlNumber = line_elements[6])

    if len(xml_elements) > 1:
        xml_elements[1] = gs_xml
    else:
        xml_elements.append(gs_xml)

    for i in range(1, len(line_elements)):

        if i == 4 and line_elements[i] != "":
            date_str = line_elements[i]
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            isa_sub = ET.SubElement(gs_xml, gs_elements[i-1])
            isa_sub.text = date

        elif i == 5 and line_elements[i] != "":
            time_str = line_elements[i]
            time = f"{time_str[:2]}:{time_str[2:]}"
            isa_sub = ET.SubElement(gs_xml, gs_elements[i-1])
            isa_sub.text = time

        elif i != 6 and line_elements[i] != "":
            gs_sub = ET.SubElement(gs_xml, gs_elements[i-1])
            gs_sub.text = line_elements[i]

def map_st(line_elements):
    st_data = ET.SubElement(xml_elements[1], "TransactionSetHeader",TransactionSetControlNumber = line_elements[2])

    if len(xml_elements) > 2:
        xml_elements[2] = st_data
    else:
        xml_elements.append(st_data)

    for i in range(1, len(line_elements)):
        if i != 2 and line_elements[i] != "":
            st_sub = ET.SubElement(st_data, st_elements[i-1])
            st_sub.text = line_elements[i]

def map_beg(line_elements):
    beg_data = ET.SubElement(xml_elements[2], "BeginningSegment", PurchaseOrderNumber = line_elements[3])

    for i in range(1, len(line_elements)):
        if i == 5 and line_elements[i] != "":
            date_str = line_elements[i]
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            isa_sub = ET.SubElement(beg_data, beg_elements[i-1])
            isa_sub.text = date
        
        elif i != 3 and line_elements[i] != "":
            beg_sub = ET.SubElement(beg_data, beg_elements[i-1])
            beg_sub.text = line_elements[i]

def map_ref(line_elements):
    ref_data = ET.SubElement(xml_elements[2], "ReferenceInformation")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            ref_sub = ET.SubElement(ref_data, ref_elements[i-1])
            ref_sub.text = line_elements[i]

def map_itd(line_elements):
    itd_data = ET.SubElement(xml_elements[2], "TermsOfSale")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            itd_sub = ET.SubElement(itd_data, itd_elements[i-1])
            itd_sub.text = line_elements[i]

def map_dtm(line_elements):
    dtm_data = ET.SubElement(xml_elements[2], "DateTimeReference")

    for i in range(1, len(line_elements)):

        if i == 2 and line_elements[i] != "":
            date_str = line_elements[i]
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            isa_sub = ET.SubElement(dtm_data, dtm_elements[i-1])
            isa_sub.text = date

        elif line_elements[i] != "":
            dtm_sub = ET.SubElement(dtm_data, dtm_elements[i-1])
            dtm_sub.text = line_elements[i]

def map_pkg(line_elements):
    pkg_data = ET.SubElement(xml_elements[2], "Packaging")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            pkg_sub = ET.SubElement(pkg_elements, pkg_elements[i-1])
            pkg_sub.text = line_elements[i]

def map_td5(line_elements):
    td5_data = ET.SubElement(xml_elements[2], "CarrierDetails")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            td5_sub = ET.SubElement(td5_data, td5_elements[i-1])
            td5_sub.text = line_elements[i]

def map_cur(line_elements):
    cur_data = ET.SubElement(xml_elements[2], "Currency")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            cur_sub = ET.SubElement(cur_data, cur_elements[i-1])
            cur_sub.text = line_elements[i]

def map_fob(line_elements):
    fob_data = ET.SubElement(xml_elements[2], "FOBRelatedInstructions", ShipmentMethodofPaymentCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if  line_elements[i] != "":
            fob_sub = ET.SubElement(fob_data, fob_elements[i-1])
            fob_sub.text = line_elements[i]

def map_n9(line_elements):
    n9_data = ET.SubElement(xml_elements[2], "ReferenceIdentification", ReferenceIdentificationQualifier = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            n9_sub = ET.SubElement(n9_data, n9_elements[i-1])
            n9_sub.text = line_elements[i]

def map_msg(line_elements):
    msg_data = ET.SubElement(xml_elements[2], "MessageText", FreeFormMessageText = line_elements[1])

    for i in range(2, len(line_elements)):
        if  line_elements[i] != "":
            msg_sub = ET.SubElement(msg_data, msg_elements[i-1])
            msg_sub.text = line_elements[i]

def map_per(line_elements):
    per_data = ET.SubElement(xml_elements[2], "AdministrativeCommunicationsContact", ContactFunctionCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            per_sub = ET.SubElement(per_data, per_elements[i-1])
            per_sub.text = line_elements[i]

def map_pid(line_elements):
    pid_data = ET.SubElement(xml_elements[2], "ProductorItemDescription", ItemDescriptionTypeCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if  line_elements[i] != "":
            pid_sub = ET.SubElement(pid_data, pid_elements[i-1])
            pid_sub.text = line_elements[i]

def map_sac(line_elements):
    sac_data = ET.SubElement(xml_elements[2], "Service,Promotion,AllowanceorChargeInformation", AllowanceorChargeIndicatorCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            sac_sub = ET.SubElement(sac_data, sac_elements[i-1])
            sac_sub.text = line_elements[i]

def map_txi(line_elements):
    txi_data = ET.SubElement(xml_elements[2], "TaxInformation", TaxTypeCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if  line_elements[i] != "":
            txi_sub = ET.SubElement(txi_data, txi_elements[i-1])
            txi_sub.text = line_elements[i]

def map_sln(line_elements):
    sln_data = ET.SubElement(xml_elements[2], "SublineItemDetail", AssignedIdentification = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            sln_sub = ET.SubElement(sln_data, sln_elements[i-1])
            sln_sub.text = line_elements[i]

def map_n1(line_elements):
    n1_data = ET.SubElement(xml_elements[2], "PartyIdentificaction", EntityIdentifierCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            n1_sub = ET.SubElement(n1_data, n1_elements[i-1])
            n1_sub.text = line_elements[i]

def map_n2(line_elements):
    n2_data = ET.SubElement(xml_elements[2], "AdditionalNameInformation")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            n2_sub = ET.SubElement(n2_data, n2_elements[i-1])
            n2_sub.text = line_elements[i]

def map_n3(line_elements):
    n3_data = ET.SubElement(xml_elements[2], "AddressInformation")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            n3_sub = ET.SubElement(n3_data, n3_elements[i-1])
            n3_sub.text = line_elements[i]

def map_n4(line_elements):
    n4_data = ET.SubElement(xml_elements[2], "GeographicLocation")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            n4_sub = ET.SubElement(n4_data, n4_elements[i-1])
            n4_sub.text = line_elements[i]

def map_po1(line_elements):
    

    if len(xml_elements) <= 3:
        xml_elements.append(ET.SubElement(xml_elements[2], "Items"))

    po5_data = ET.SubElement(xml_elements[3], "BaselineItemData")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            po5_sub = ET.SubElement(po5_data, po5_elements[i-1])
            po5_sub.text = line_elements[i]
            

def map_ctt(line_elements):
    ctt_data = ET.SubElement(xml_elements[2], "TransactionTotals")

    for i in range(1, len(line_elements)):
        if line_elements[i] != "":
            ctt_sub = ET.SubElement(ctt_data, ctt_elements[i-1])
            ctt_sub.text = line_elements[i]

def map_sdq(line_elements):
    sdq_data = ET.SubElement(xml_elements[2], "DestinationQuantity", UnitorBasisforMeasurementCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            sdq_sub = ET.SubElement(sdq_data, sdq_elements[i-1])
            sdq_sub.text = line_elements[i]

def map_amt(line_elements):
    amt_data = ET.SubElement(xml_elements[2], "MonetaryAmountInformation", AmountQualifierCode = line_elements[1])

    for i in range(2, len(line_elements)):
        if line_elements[i] != "":
            amt_sub = ET.SubElement(amt_data, amt_elements[i-1])
            amt_sub.text = line_elements[i]


def clean_st(line_elements):
    del xml_elements[3]
    del xml_elements[2]

def clean_gs(line_elements):
    del xml_elements[1]

map_functions = [[ ],
                 [{"key": "N9", "func": map_n9}, {"key": "N1", "func": map_n1}], #1
                 [], #2
                 [{"key": "ISA", "func": map_isa}, {"key": "SE", "func": clean_st}], #3
                 [{"key": "SDQ", "func": map_sdq}],
                 [{"key": "N4", "func":map_n4}], #5
                 [{"key": "CTT", "func": map_ctt}],
                 [{"key": "AMT", "func": map_amt}],
                 [{"key": "CUR", "func": map_cur}, {"key": "PER", "func": map_per}, {"key": "N3", "func": map_n3}, {"key": "PO1", "func": map_po1}], #8
                 [{"key": "GS", "func": map_gs}],
                 [{"key": "BEG", "func": map_beg}], #10
                 [], #11
                 [ {"key": "N2", "func": map_n2}], #12
                 [ {"key": "GE", "func": clean_gs}], #13
                 [{"key": "DTM", "func": map_dtm}, {"key": "PID", "func": map_pid}], #14
                 [{"key": "ST", "func": map_st}],
                 [],
                 [],
                 [],
                 [{"key": "REF", "func": map_ref}]]

def hash_segment(segment):
    hash_object = hashlib.sha256()
    hash_object.update(segment.encode("utf-8"))

    hashed_value = int(hash_object.hexdigest(), 16)

    if hashed_value < 0:
        hashed_value = -hashed_value

    index = hashed_value % 20

    return index

def map_ansi_x12_to_xml(line_elements):
    index = hash_segment(line_elements[0])


    for e in map_functions[index]:
        if e["key"] == line_elements[0]:
            return e["func"](line_elements)


if __name__ == '__main__':
    #===============================================================================================
    # Open the file and separate each line
    f = open("test.edi", "r")
    lines = f.read().split("~")
    
    #===============================================================================================
    # Map each line depending of the segment (elements[0])
    for line in lines:
        elements = line.split("^")
        map_ansi_x12_to_xml(elements)

    #===============================================================================================
    # These lines give a pretty format to the XML Tree
    # print("XML TREE")
    temp = xml.dom.minidom.parseString(ET.tostring(xml_elements[0], encoding="utf-8", method="xml"))
    new_xml = temp.toprettyxml()
    print(new_xml)

    #===============================================================================================
    # Write the XML File
    tree = ET.ElementTree(xml_elements[0])

    with open("output.xml", "w") as f:
        f.write(new_xml)
