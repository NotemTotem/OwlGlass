from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,ValidationError, SelectMultipleField
from wtforms.validators import DataRequired

#Accountfinder form class
class AccountfinderForm(FlaskForm):
    target = StringField("Target",validators=[DataRequired()],render_kw={"placeholder": "Target's username or email"})
    target_type = SelectField("Target Type",choices=['username','email'])
    submit = SubmitField("Submit")

    def validate_target(form,field):
        if form.target_type.data == 'email':
            if not('@' in (field.data) and '.' in field.data.split('@')[1] and len(field.data.split('@')[0]) >0):
                raise ValidationError("Not a valid email.")

                 
class dnslookupForm(FlaskForm):
    target = StringField("Target", validators=[DataRequired()], render_kw={"placeholder": "Target website or subdomain"})
    record_type_choices = [
        ("A", "A (Host Address)"),
        ("NS", "NS (Name Server)"),
        ("MD", "MD (Mail Destination - Obsolete)"),
        ("MF", "MF (Mail Forwarder - Obsolete)"),
        ("CNAME", "CNAME (Canonical Name)"),
        ("SOA", "SOA (Start of Authority)"),
        ("MB", "MB (Mailbox Domain Name - Obsolete)"),
        ("MG", "MG (Mail Group Member - Obsolete)"),
        ("MR", "MR (Mail Rename Domain Name - Obsolete)"),
        ("NULL", "NULL (Null Record - Obsolete)"),
        ("WKS", "WKS (Well Known Services - Obsolete)"),
        ("PTR", "PTR (Domain Name Pointer)"),
        ("HINFO", "HINFO (Host Information)"),
        ("MINFO", "MINFO (Mailbox Information)"),
        ("MX", "MX (Mail Exchange)"),
        ("TXT", "TXT (Text)"),
        ("RP", "RP (Responsible Person)"),
        ("AFSDB", "AFSDB (AFS Database Location)"),
        ("X25", "X25 (X.25 PSDN Address)"),
        ("ISDN", "ISDN (ISDN Address)"),
        ("RT", "RT (Route Through)"),
        ("NSAP", "NSAP (Network Service Access Point Address - Obsolete)"),
        ("NSAP-PTR", "NSAP-PTR (NSAP Pointer - Obsolete)"),
        ("SIG", "SIG (Signature)"),
        ("KEY", "KEY (Key Record)"),
        ("PX", "PX (X.400 Mail Information - Obsolete)"),
        ("GPOS", "GPOS (Geographical Position - Obsolete)"),
        ("AAAA", "AAAA (IPv6 Host Address)"),
        ("LOC", "LOC (Location Information)"),
        ("NXT", "NXT (Next Domain - Obsolete)"),
        ("SRV", "SRV (Service Locator)"),
        ("NAPTR", "NAPTR (Naming Authority Pointer)"),
        ("KX", "KX (Key Exchanger)"),
        ("CERT", "CERT (Certificate Record)"),
        ("A6", "A6 (IPv6 Address - Obsolete)"),
        ("DNAME", "DNAME (Delegation Name)"),
        ("APL", "APL (Address Prefix List)"),
        ("DS", "DS (Delegation Signer)"),
        ("SSHFP", "SSHFP (SSH Public Key Fingerprint)"),
        ("IPSECKEY", "IPSECKEY (IPSEC Key)"),
        ("RRSIG", "RRSIG (DNSSEC Signature)"),
        ("NSEC", "NSEC (Next Secure Record)"),
        ("DNSKEY", "DNSKEY (DNSSEC Key)"),
        ("DHCID", "DHCID (DHCP Identifier)"),
        ("NSEC3", "NSEC3 (Next Secure Record v3)"),
        ("NSEC3PARAM", "NSEC3PARAM (NSEC3 Parameters)"),
        ("TLSA", "TLSA (TLS Authentication)"),
        ("HIP", "HIP (Host Identity Protocol)"),
        ("CDS", "CDS (Child Delegation Signer)"),
        ("CDNSKEY", "CDNSKEY (Child DNSKEY)"),
        ("CSYNC", "CSYNC (Child Synchronisation)"),
        ("SPF", "SPF (Sender Policy Framework)"),
        ("UNSPEC", "UNSPEC (Unspecified - RFC 1035)"),
        ("EUI48", "EUI48 (EUI-48 Address)"),
        ("EUI64", "EUI64 (EUI-64 Address)"),
        ("URI", "URI (Uniform Resource Identifier)"),
        ("CAA", "CAA (Certification Authority Authorization)"),
        ("TA", "TA (Trust Authority - Obsolete)"),
        ("DLV", "DLV (DNSSEC Lookaside Validation - Obsolete)")
    ]

    my_choices = SelectMultipleField("Select DNS record types", choices=record_type_choices)
    submit = SubmitField("Submit query")
class port_scanner_form(FlaskForm):
    target = StringField("Target Address", validators=[DataRequired()], render_kw={"placeholder": "Target URL or IP Adress"})
    ports = StringField("Ports", render_kw={"placeholder": "Target URL or IP Adress"})
    submit = SubmitField("Submit")
