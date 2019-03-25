from flask_wtf import FlaskForm
from wtforms import StringField , TextField , IntegerField , DateTimeField , SubmitField , FileField
from wtforms.validators import DataRequired , Length , NumberRange , InputRequired
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms.fields import RadioField , SelectField

class AddAsset(FlaskForm):
    Assettype = TextField('Asset type',
                          validators=[InputRequired(), Length(min=1, max=25)])
    Assetsequence = StringField('Asset sequence',
                         validators=[InputRequired() , NumberRange(min=0, max=1000)])
    Assetname = StringField('Asset name',
                         validators=[InputRequired() , NumberRange(min=0, max=1000)])

    Assetnumber = StringField('Asset number',
                          validators=[InputRequired(), Length(min=1, max=25)])
    DateofPurchase = DateField('Date of Purchase' , validators=[InputRequired()] , format='%y/%d/%m')
    AssestWarrentyUpto = DateField('Warrenty Upto', validators=[InputRequired()] , format='%y/%d/%m ')
    Submit = SubmitField('Submit')
    Modify = SubmitField('Modify')


class ProjectDetail(FlaskForm):
        ProjectNumber = IntegerField('Project Number',validators=[DataRequired()])
        ProjectName = StringField('Project Name',
                         validators=[DataRequired()])
        ProjectContact = IntegerField('Project Contact',validators=[DataRequired()])
        ProjectAddress = StringField('Project Address',
                         validators=[DataRequired()])
        ProjectStartDate = DateField('Project Start Date', validators=[DataRequired()] , format='%m/%d/%y')
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class AddProjectDocument(FlaskForm):
        DocumentType = StringField('Document Type' , validators=[DataRequired()])
        DocumentSequence = StringField('Document Sequence', validators=[DataRequired()])
        DocumentNumber = StringField('Document Number' , validators=[DataRequired()])
        DocumentName = StringField('Document Name' , validators=[DataRequired])
        IssueDate = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        Attachment = FileField('choose File' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class AddTechDocument(FlaskForm):
        DocumentType = TextField('Document Type' , validators=[DataRequired()])
        DocumentSequence = StringField('Document Sequence', validators=[DataRequired()])
        DocumentNumber = StringField('Document Number' , validators=[DataRequired()])
        DocumentName = TextField('Document Name' , validators=[DataRequired])
        IssueDate = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        Attachment = FileField('choose File' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class AssetSpecification(FlaskForm):
    AssetNumber = StringField('Asset Number' , validators=[DataRequired()])
    Model = StringField('Model')
    Brand = StringField('Brand')
    Specifications = StringField('Specification')
    Submit = SubmitField('Submit')
    Modify = SubmitField('Modify')

class AssetCorrespondance(FlaskForm):
    AssetNumber = StringField('Asset Number' , validators=[DataRequired()])
    UserGuide = StringField('User Guide')
    WarrentyCard = FileField('Upload Warrenty Card')
    BillNumber = StringField('Bill Number' , validators= [DataRequired()])
    #PaymentMode = SelectField('Payment Mode' , choices=[('Cash' , 'Cash') , ('DBCard' , 'Debit Card'), ('CrCard','Credit Card') , ('OnWallet' , 'Online Wallet')])
    
    Submit = SubmitField('Submit')
    Modify = SubmitField('Modify')

class Investment(FlaskForm):
        Date = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        CashRecived = StringField('Cash Received From' , validators= [DataRequired()])
        Paid = StringField('Paid AS' , validators= [DataRequired()])
        Remark = StringField('Remarks' , validators= [DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class Installment(FlaskForm):
        AssetNumber = StringField('Asset Number' , validators= [DataRequired()])
        DueDate = DateField('Due Date', validators=[DataRequired()] , format='%m/%d/%y')
        Payment = DateField('Payment Date', validators=[DataRequired()] , format='%m/%d/%y')
        EnterAmt = StringField('Enter Amount' , validators= [DataRequired()])
        RemBal = StringField('Remaning Balance' , validators= [DataRequired()])
        PaymentRecpt = FileField('Upload Warrenty Card')
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class InvestmentInfo(FlaskForm):
        DocumentType = StringField('Document Type' , validators= [DataRequired()])
        InvestmentNum = StringField('Investment Number' , validators= [DataRequired()])
        DocumentNumber = StringField('Document Number' , validators= [DataRequired()])
        DocumentName = StringField('Document Name' , validators= [DataRequired()])
        IssueDate = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        Attachment = FileField('Attach Document' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class LegalDocu(FlaskForm):
        DocumentType = TextField('Document Type' , validators=[DataRequired()])
        DocumentSequence = StringField('Document Sequence', validators=[DataRequired()])
        DocumentNumber = StringField('Document Number' , validators=[DataRequired()])
        DocumentName = TextField('Document Name' , validators=[DataRequired])
        IssueDate = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        Attachment = FileField('choose File' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class ReferanceDoc(FlaskForm):
        DocumentType = TextField('Document Type' , validators=[DataRequired()])
        DocumentSequence = StringField('Document Sequence', validators=[DataRequired()])
        DocumentNumber = StringField('Document Number' , validators=[DataRequired()])
        DocumentName = TextField('Document Name' , validators=[DataRequired])
        IssueDate = DateField('Issue Date', validators=[DataRequired()] , format='%m/%d/%y')
        Attachment = FileField('choose File' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')

class WarrentyDetail(FlaskForm):
        AssetNum = StringField('Asset Number', validators=[DataRequired()])
        WarrentyStart = DateField('Warrenty Start', validators=[DataRequired()] , format='%m/%d/%y')
        ServiceAddrs = StringField('Service Centre Address' , validators=[DataRequired()])
        ServiceCentre = StringField('Service Centre Contact' , validators=[DataRequired()])
        Submit = SubmitField('Submit')
        Modify = SubmitField('Modify')