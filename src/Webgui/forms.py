from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,ValidationError, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
        """
        A multiple-select field that displays a list of checkboxes.
        """
        widget = widgets.ListWidget(prefix_label=False)
        option_widget = widgets.CheckboxInput()

#Accountfinder form class
class AccountfinderForm(FlaskForm):
    target = StringField("Target",validators=[DataRequired()],render_kw={"placeholder": "Target's username or email"})
    cap = StringField("Cap",render_kw={"placeholder": "max number of websites target will be checked against"})
    #submit = SubmitField("Submit")


class dnslookupForm(FlaskForm):

    target = StringField("Target", validators=[DataRequired()], render_kw={"placeholder": "Target website or subdomain"})
    record_type_choices = [
        ("ALL", "ALL"),
        ("ZONE", "ZONE TRANSFER"),
        ("A", "A (Host Address)"),
        ("NS", "NS (Name Server)"),
        ("MD", "MD (Mail Destination )"),
        ("MF", "MF (Mail Forwarder )"),
        ("CNAME", "CNAME (Canonical Name)"),
        ("SOA", "SOA (Start of Authority)"),
        ("MB", "MB (Mailbox Domain Name )"),
        ("MG", "MG (Mail Group Member )"),
        ("MR", "MR (Mail Rename Domain Name )"),
        ("NULL", "NULL (Null Record )"),
        ("WKS", "WKS (Well Known Services )"),
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
        ("NSAP", "NSAP (Network Service Access Point Address )"),
        ("NSAP-PTR", "NSAP-PTR (NSAP Pointer )"),
        ("SIG", "SIG (Signature)"),
        ("KEY", "KEY (Key Record)"),
        ("PX", "PX (X.400 Mail Information )"),
        ("GPOS", "GPOS (Geographical Position )"),
        ("AAAA", "AAAA (IPv6 Host Address)"),
        ("LOC", "LOC (Location Information)"),
        ("NXT", "NXT (Next Domain )"),
        ("SRV", "SRV (Service Locator)"),
        ("NAPTR", "NAPTR (Naming Authority Pointer)"),
        ("KX", "KX (Key Exchanger)"),
        ("CERT", "CERT (Certificate Record)"),
        ("A6", "A6 (IPv6 Address )"),
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
        ("TA", "TA (Trust Authority )"),
        ("DLV", "DLV (DNSSEC Lookaside Validation )")
    ]

    my_choices = MultiCheckboxField("Select DNS record types", choices=record_type_choices, coerce=str)
    submit = SubmitField("Submit query")



class port_scanner_form(FlaskForm):
    target = StringField("Target Address", validators=[DataRequired()], render_kw={"placeholder": "Target URL or IP Adress"})
    ports = StringField("Ports (max 65,535)", validators=[DataRequired()], render_kw={"placeholder": "Target Ports to Scan"})
    submit = SubmitField("Submit")


class fuzzer_form(FlaskForm):
    target = StringField("Target URL", validators=[DataRequired()], render_kw={"placeholder": "Target URL or IP Adress"})
    port = StringField("Port", render_kw={"placeholder": "Port of web server"})
    depth = StringField("Recursion Depth", validators=[DataRequired()], render_kw={"placeholder": "Depth of recursion"})

    def validate_port(form, port):
        if int(port.data) not in range(0, 65536):
            raise ValidationError('Port must be in range 0-65535')
