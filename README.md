# Agreement_Generation
Program to automatically generate the business agreement, based off of python module PyPDF2.

# Table of Contents

[`generate.py`](#`generate.py`)   
[Setup](#Setup)   
[Adding new agreements](#Adding-new-agreements)   
[`generate.py` Method Documentation](#`generate.py`-Method-Documentation)   

# `generate.py`
`generate.py` is a python script written in order to generate a business agreement. The script takes a template pdf form and values. The script then uses module PyPDF2 to fill in form fields and write to an output pdf file. The output pdf file contains all specified fields filled.

# Setup
You must run `pip install PyPDF2` in order to run the script navigate to the directory of the program and run `python generate.py`  
Ask Jeffrey for agreement file(s) necessary to run the program.

# Adding new agreements
In order to add more agreements, you must have a template pdf file with fillable form fields.
In order to get the program to fill out the file, place the template pdf file in the same directory as the generate.py file.  

Modify the `constructAgreement(manufacturer)` method with this template:
```python
elif manufacturer == "MANUFACTURER":
    generatePdf("Template.pdf", "out.pdf")
```
Where `MANUFACTURER` is the name of the manufacturer and `Template` is the name of the template pdf.

After this is taken care of, the program should be able to detect whatever manufacturer is desired and generate an agreement for them specifically.
Ensure that the checkbox fields are taken care of beforehand as the program currently does not contain funcionality to modify them.

# `generate.py` Method Documentation

## constructAgreement(manufacturer)
```python
def constructAgreement(manufacturer):
    if manufacturer == "MARVIN":
        generatePdf("2020 Agreement Marvin.pdf", "out.pdf")
    elif manufacturer == "AMERIMAX":
        generatePdf("2020 Agreement Amerimax with Patio Door.pdf", "out.pdf")
```
`constructAgreement(manufacturer)` is a method that takes a manufacturer and generates a pdf given a template pdf and a designated output pdf. Currently manufacturers Marvin and Amerimax are supported.

## updateFormProperlyWriter(writer: PdfFileWriter)
```python
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
```
`updateFormProperlyWriter(writer: PdfFileWriter)` is a method that takes a pdfFileWriter and modifies it so that the resulting pdf file properly displays edited fields in the browser.

## generatePdf(infile, outfile)
```python
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

    for x in range(pdf.getNumPages() - 1):
        pdf2.addPage(pdf.getPage(x)) 
        pdf2.updatePageFormFieldValues(pdf2.getPage(x), FORM_VALUES)
    
    flat_page = pdf2.getPage(0)
    for j in range(0, len(flat_page['/Annots'])):
        writer_annot = flat_page['/Annots'][j].getObject()
        for field in FLATTEN_VALUES: 
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/Ff"): NumberObject(1)
                })

    outputStream = open(outfile, "wb")
    pdf2.write(outputStream)
```
`generatePdf(infile, outfile)` is a method that takes an input pdf file and an output pdf file. Using these, a pdfFileReader and pdfFileReader object is created. After the pdf has been written to, designated fields for field flattening are flattened(unable to be edited by the user).

