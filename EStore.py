

import openpyxl
from openpyxl.styles import Alignment
import os
import datetime

def create_or_load_workbook(filename):
    if os.path.exists(filename):
        return openpyxl.load_workbook(filename)
    else:
        workbook = openpyxl.Workbook()
        workbook.save(filename)
        return openpyxl.load_workbook(filename)

def format_header_and_subheader(worksheet, header_subheader_mapping):
    col_offset = 1
    for top_header, subheaders in header_subheader_mapping.items():
        col_num = col_offset
        worksheet.cell(row=1, column=col_num, value=top_header)
        worksheet.merge_cells(start_row=1, start_column=col_num, end_row=1, end_column=col_num + len(subheaders) - 1)
        worksheet.cell(row=1, column=col_num).alignment = Alignment(horizontal='center', vertical='center')

        for subheader in subheaders:
            worksheet.cell(row=2, column=col_num, value=subheader)
            col_num += 1

        col_offset += len(subheaders)

    # Insert an empty row as the 3rd row
    worksheet.insert_rows(3)

def append_live_data(worksheet, live_data):
    for row_data in live_data:
        worksheet.append(row_data)

def auto_adjust_column_widths(worksheet):
    for col_idx, column_cells in enumerate(worksheet.columns, start=1):
        max_length = max(len(str(cell.value)) for cell in column_cells)
        col_letter = openpyxl.utils.get_column_letter(col_idx)
        adjusted_width = max(max_length, len(col_letter)) + 2
        worksheet.column_dimensions[col_letter].width = adjusted_width

def save_workbook(workbook, filename):
    workbook.save(filename)

def main(header_subheader_mapping,live_data):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"output_{current_date}.xlsx"
    
    workbook = create_or_load_workbook(filename)
    worksheet = workbook.active

    

    format_header_and_subheader(worksheet, header_subheader_mapping)

    

    append_live_data(worksheet, live_data)

    auto_adjust_column_widths(worksheet)

    save_workbook(workbook, filename)

if __name__ == "__main__":
    header_subheader_mapping = {
        "Business Information": ["License #", "Name", "Address","City","Zip","Phone #","Entity","Issue Date","Reissue Date","Expire Date"],
        "License Status": ["Status"],
        "Classifications": ["Classifications Name","Certifications Name"],
        "Bonding Information": ["Contractor's Bond Title","Contractor's Bond Number ","Contractor's Bond Amount","Contractor's Bond Effective Date","Contractor's Bond  History Link","LLC EMPLOYEE/WORKER BOND Title","LLC EMPLOYEE/WORKER BOND Number","LLC EMPLOYEE/WORKER BOND Amount","LLC EMPLOYEE/WORKER BOND Effective Date","LLC EMPLOYEE/WORKER BOND History Link","Bond of Qualifying Individual Title","Bond of Qualifying Individual Effective Date","Bond of Qualifying Individual History Link"],
        "Workers' Compensation": ["Title","Policy Number","Effective Date","Expire Date","Workers' Compensation History Link","Insurance Company Code",],
        "Liability Insurance Information": ["Title","Policy Number","Amount","Effective Date","Expiration Date","Liability Insurance History","Insurance Company"],
        "Miscellaneous Information": ["Title"],
        "Other": ["Title"],
        "Personnel": ["Name","Title","Association Date",""],

    }
    live_data = [
        ['927409', 'SILVERSTRAND CONSTRUCTION', '10065 OLD GROVE RD STE 200', 'SAN DIEGO', '92131', '(858) 444-1967', '\nCorporation\n', '\n04/17/1990\n', '', '\n04/30/2024\n', '\nThis license is current and active.All information below should be reviewed.\n', 'B - GENERAL BUILDING\nA - GENERAL ENGINEERING\n', 'HAZ - HAZARDOUS SUBSTANCES REMOVAL\nASB - ASBESTOS\n', "This license filed a Contractor's Bond with  MERCHANTS BONDING COMPANY (MUTUAL).", 'Bond Number: 100058428', 'Bond Amount: $25,000', 'Effective Date: 04/13/2023', '/OnlineServices/CheckLicenseII/ContractorBondingHistory.aspx?LicNum=592080&BondType=CB', '', '', '', '', '', 'The qualifying individual WILLIAM CHARLES GABRIELSON  certified that he/she owns 10 percent or more of the voting stock/membership interest of this company; therefore, the Bond of Qualifying Individual is not required.', 'Effective Date: 04/17/1990', '', '', 'This license is exempt from having workers compensation insurance; they certified that they have no employees at this time.', '', 'Effective Date:', '03/03/2022', 'Expire Date:', 'None', '/OnlineServices/CheckLicenseII/WCHistory.aspx?LicNum=592080', None]]
    main(header_subheader_mapping,live_data)
