from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject
import datetime

#Sample form values, in dictionary format
FORM_VALUES = {
  "Name": "Name",
  "Phone": "Phone",
  "Email": "Email",
  "City": "City",
  "Zip": "Zip",
  "Date": f"{datetime.date.today().month}/{datetime.date.today().day}/{datetime.date.today().year}",
  "Price": "Price",
  "Total": "Total",
  "Day": datetime.date.today().day,
  "Start Date": "MM/DD/YYYY",
  "Completion Date": "MM/DD/YYYY",
  "Billing Address": "Billing Address",
  "Job Site Address": "Job Site Address",
  "Month": datetime.date.today().month,
  "Year": datetime.date.today().year,
#   "Digital Signature": "Digital Signature",
  "Permit": True,
#   "Right To Cancel": True,
  "Progress Payment": "Progress Payment",
  "Down Payment": "$0",
  "Window-Door" : "W-D"
}

# Designated values for flattening
FLATTEN_VALUES = {
    "Window-Door" : "W-D"
}

# Modification of the pdfwriter in order to be up to current pdf spec, or else form will not update properly upon generation.
def updateFormProperlyWriter(writer: PdfFileWriter):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('updateFormProperlyWriter() catch : ', repr(e))
        return writer

# Method to update check boxes, WORK IN PROGRESS.
# def updateCheckboxValues(page, fields):
#     for j in range(0, len(page['/Annots'])):
#         writer_annot = page['/Annots'][j].getObject()
#         for field in fields:
#             if writer_annot.get('/T') == field:
#                 writer_annot.update({
#                     NameObject("/V"): NameObject(fields[field]),
#                     NameObject("/AS"): NameObject(fields[field])
#                 })

def generatePdf(infile, outfile):
    pdf = PdfFileReader(open(infile, "rb"), strict=False)
    if "/AcroForm" in pdf.trailer["/Root"]:
        pdf.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf2 = PdfFileWriter()
    updateFormProperlyWriter(pdf2)
    if "/AcroForm" in pdf2._root_object:
        pdf2._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})


    pdf2.addPage(pdf.getPage(0))
    # Update form values.
    pdf2.updatePageFormFieldValues(pdf2.getPage(0), FORM_VALUES)
    
    # Flatten form fields.
    flat_page = pdf2.getPage(0)
    for j in range(0, len(flat_page['/Annots'])):
        writer_annot = flat_page['/Annots'][j].getObject()
        for field in FLATTEN_VALUES: 
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/Ff"): NumberObject(1)   # make ReadOnly
                })

    outputStream = open(outfile, "wb")
    pdf2.write(outputStream)

# Program that reads and fills pdf form, generating an output pdf file with form filled.
# requires designated agreement file, read readme file for instructions to obtain file.
if __name__ == '__main__':

    infile = "2020 Agreement Marvin.pdf"

    generatePdf(infile, "out.pdf")