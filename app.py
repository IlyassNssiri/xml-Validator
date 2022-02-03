from flask import Flask, render_template, request, redirect, flash, url_for
import xmlschema , lxml
from lxml import  etree



app = Flask(__name__)









#************************************** function traits internal DTD ***************************************************
def InternalDTD(varDTD):
    try:
        tree = etree.parse(varDTD)
        dtd = tree.docinfo.internalDTD
        root = tree.getroot()
        is_valid = dtd.assertValid(root)
        msg = True

    except lxml.etree.DocumentInvalid as valide:
        msg =  valide
    return(msg)
#***********************************************************************************************************************

#******************************************* Routes for the MENU********************************************************
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xmlschema')
def xsd():
    return render_template('xmlschema.html')

@app.route('/intdtd')
def intdtd():
    return render_template('intdtd.html')

@app.route('/extdtd')
def extdtd():
    return render_template('extdtd.html')
#***********************************************************************************************************************

#************************************************** DTD Part ***********************************************************
#*************************EXTERNAL DTD****************************
#**VALIDETE XML USING EXTERNAL DTD TEXTAREA***
@app.route('/DTD_TEXT', methods=['POST'])
def input_dtd():
    input_file1 = request.form['xml1']
    text_file1 = open("xxxDTD.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()
    input_file2 = request.form['dtd1']
    text_file2 = open("xxxDTD.xsd", "w")
    text_file2.write(input_file2)
    text_file2.close()
    try:
        xml_file = lxml.etree.parse("xxxDTD.xml")
        xml_validator = lxml.etree.DTD(file="xxxDTD.xsd")
        valide = xml_validator.assertValid(xml_file)
        mes = True
    except lxml.etree.DocumentInvalid as valide:
        mes=valide
    return render_template('extdtd.html', message4=mes)
#**VALIDATE XML USING EXTERNAL DTD FILES**
@app.route('/extdtd', methods=['POST'])
def exdtdfile():
    if request.method == 'POST':
        f1 = request.files['f1']
        f2 = request.files['f2']
        f1.save(f1.filename)
        f2.save(f2.filename)
    try:
        dtd = lxml.etree.DTD(f1.filename)
        tree = lxml.etree.parse(f2.filename)
        valide = dtd.assertValid(tree)
        mes = True
    except lxml.etree.DocumentInvalid as valide:
        mes=valide
    return render_template('extdtd.html', message6=mes)
#*************************INTERNAL DTD****************************
#**VALIDATE XML USING INTERNAL DTD (FILE)**
@app.route('/intdtd', methods=['POST'])
def upload_file2():
    uploaded_file1 = request.files['file3']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)

    valide = InternalDTD(uploaded_file1.filename)
    return render_template('intdtd.html', message1=valide)


#**VALIDATE XML USING INTERNAL DTD TEXTAREA**
@app.route('/xml_DTD_TEXT', methods=['POST'])
def upload_file5():
    input_file1 = request.form['Xml_Dtd']
    text_file1 = open("xxxXmlDtd.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()
    valide = InternalDTD("xxxXmlDtd.xml")
    return render_template('intdtd.html', message5=valide)
#***********************************************************************************************************************

#***************************************** VALIDATE XML USING XMLSCHEMA ************************************************
#********** USING FILES XMLSCHEMA*********
@app.route('/xmlschema', methods=['POST'])
def upload_file():
    uploaded_file1 = request.files['file1']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)

    uploaded_file2 = request.files['file2']
    if uploaded_file2.filename != '':
        uploaded_file2.save(uploaded_file2.filename)


    try:
        xml_file = lxml.etree.parse(uploaded_file1.filename)
        xml_validator = lxml.etree.XMLSchema(file=uploaded_file2.filename)

        is_valid = xml_validator.assertValid(xml_file)

    except Exception as valide:
        return render_template('xmlschema.html', message=valide)
    return render_template('xmlschema.html', message=True)

#********  USING TEXTAREA XMLSCHEMA********
@app.route('/XSD', methods=['POST'])
def input_xsd():
    input_file1 = request.form['xml']
    text_file1 = open("TextArea.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()

    input_file2 = request.form['xsd']
    text_file2 = open("TextArea.xsd", "w")
    text_file2.write(input_file2)
    text_file2.close()

    try:
        xml_file = lxml.etree.parse("TextArea.xml")
        xml_validator = lxml.etree.XMLSchema(file="TextArea.xsd")

        is_valid = xml_validator.assertValid(xml_file)
    except Exception as valide:
        return render_template('xmlschema.html', message3=valide)

    return render_template('xmlschema.html', message3=True)

if __name__ == '__main__':
    app.run(debug=True)