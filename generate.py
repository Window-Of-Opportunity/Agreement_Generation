from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

FORM_VALUES = {
  "Name": "Name",
  "Phone": "Phone",
  "Email": "Email",
  "City": "City",
  "Zip": "Zip",
  "Date": "Date",
  "Price": "Price",
  "Total": "Total",
  "Day": "Day",
  "Start Date": "Start Date",
  "Completion Date": "Completion Date",
  "Billing Address": "Billing Address",
  "Job Site Address": "Job Site Address",
  "Month": "Month",
  "Year": "Year",
  "Digital Signature": "Digital Signature",
  "Permit": True,
  "Right To Cancel": True,
  "Progress Payment": "Progress Payment",
  "Down Payment": "Down Payment" 
}

def set_need_appearances_writer(writer: PdfFileWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

def updateCheckboxValues(page, fields):

    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in fields:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/V"): NameObject(fields[field]),
                    NameObject("/AS"): NameObject(fields[field])
                })

if __name__ == '__main__':
    infile = "2020 Agreement Marvin.pdf"
    outfile = "out.pdf"

    pdf = PdfFileReader(open(infile, "rb"), strict=False)
    if "/AcroForm" in pdf.trailer["/Root"]:
        pdf.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf2 = PdfFileWriter()
    set_need_appearances_writer(pdf2)
    if "/AcroForm" in pdf2._root_object:
        pdf2._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})


    pdf2.addPage(pdf.getPage(0))
    pdf2.updatePageFormFieldValues(pdf2.getPage(0), FORM_VALUES)

    outputStream = open(outfile, "wb")
    pdf2.write(outputStream)