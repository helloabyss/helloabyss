"""Metro 2 and e-OSCAR reference data.

The authoritative source is the CDIA Credit Reporting Resource Guide (CRRG), which is
licensed and not public. Every table here carries a verification status. The audit
engine's logic depends only on dispute CATEGORIES, never on raw e-OSCAR code numbers,
so an out-of-date code number can't change which disputes the system raises.
"""

# Metro 2 Base Segment Account Status codes (Field 17A).
ACCOUNT_STATUS = {
    "05": "Account transferred",
    "11": "Current account (0-29 days past due)",
    "13": "Paid or closed account / zero balance",
    "61": "Paid in full, was a voluntary surrender",
    "62": "Paid in full, was a collection account",
    "63": "Paid in full, was a repossession",
    "64": "Paid in full, was a charge-off",
    "65": "Paid in full, a foreclosure was started",
    "71": "30-59 days past due",
    "78": "60-89 days past due",
    "80": "90-119 days past due",
    "82": "120-149 days past due",
    "83": "150-179 days past due",
    "84": "180 days or more past due",
    "88": "Claim filed with government for insured portion of balance",
    "89": "Deed received in lieu of foreclosure on a defaulted mortgage",
    "93": "Account assigned to internal or external collections",
    "94": "Foreclosure completed",
    "95": "Voluntary surrender",
    "96": "Merchandise was repossessed",
    "97": "Unpaid balance reported as a loss (charge-off)",
    "DA": "Delete entire account (not for fraud)",
    "DF": "Delete entire account due to confirmed fraud",
}
ACCOUNT_STATUS_VERIFIED = "unverified"

DEROGATORY_STATUSES = {"61", "62", "63", "64", "65", "71", "78", "80", "82", "83", "84",
                       "88", "89", "93", "94", "95", "96", "97"}
PAID_STATUSES = {"13", "61", "62", "63", "64", "65"}

# Payment History Profile characters (Field 18), most recent month first.
PAYMENT_HISTORY = {
    "0": "0-29 days past due (current)",
    "1": "30-59 days past due",
    "2": "60-89 days past due",
    "3": "90-119 days past due",
    "4": "120-149 days past due",
    "5": "150-179 days past due",
    "6": "180+ days past due",
    "B": "No payment history before this time",
    "D": "No payment history reported this month",
    "E": "Zero balance and current",
    "G": "Collection",
    "H": "Foreclosure completed",
    "J": "Voluntary surrender",
    "K": "Repossession",
    "L": "Charge-off",
}
LATE_MARKS = set("123456GHJKL")

# Compliance Condition Codes (Field 20).
COMPLIANCE_CONDITION = {
    "XA": ("Account closed at consumer's request", "unverified"),
    "XB": ("Account information disputed by consumer under the FCRA (investigation in progress)", "secondary"),
    "XC": ("Completed investigation of FCRA dispute; consumer disagrees", "unverified"),
    "XD": ("Account closed at consumer's request and in dispute under the FCRA", "unverified"),
    "XE": ("Account closed at consumer's request; FCRA dispute investigated, consumer disagrees", "unverified"),
    "XF": ("Account in dispute under the Fair Credit Billing Act", "unverified"),
    "XG": ("FCBA dispute resolved; consumer disagrees", "unverified"),
    "XH": ("Account previously in dispute; investigation completed and reported by furnisher", "secondary"),
    "XJ": ("Account closed at consumer's request and in dispute under the FCBA", "unverified"),
    "XR": ("Removes the most recently reported compliance condition code", "unverified"),
}
DISPUTE_FLAGS = {"XB", "XC", "XD", "XE", "XF", "XG", "XJ"}

# ECOA codes (Field 37): who is responsible.
ECOA = {
    "1": "Individual", "2": "Joint contractual liability", "3": "Authorized user",
    "5": "Co-maker or guarantor", "7": "Maker", "T": "Association terminated",
    "W": "Business / commercial", "X": "Deceased", "Z": "Delete consumer",
}

# Key Base Segment fields the audit reads, by CRRG field number.
METRO2_FIELDS = {
    "10": "Date Opened",
    "17A": "Account Status",
    "18": "Payment History Profile",
    "19": "Special Comment",
    "20": "Compliance Condition Code",
    "21": "Current Balance",
    "22": "Amount Past Due",
    "23": "Original Charge-off Amount",
    "24": "Date of Account Information",
    "25": "FCRA Compliance / Date of First Delinquency",
    "26": "Date Closed",
    "27": "Date of Last Payment",
    "37": "ECOA Code",
}
METRO2_FIELDS_VERIFIED = "unverified"

# Dispute categories. The audit maps every finding to one of these. Example e-OSCAR
# codes are from secondary sources (consumer law blogs, agency policy pages) and must be
# confirmed against the current CDIA list before anyone relies on the numbers.
DISPUTE_CATEGORIES = {
    "IDENTITY": {
        "label": "Not mine / mixed file",
        "example_codes": {"001": "Not his/hers", "002": "Belongs to another individual with same/similar name"},
    },
    "FRAUD": {
        "label": "Fraud / identity theft",
        "example_codes": {"103": "Claims true identity fraud; account fraudulently opened",
                          "104": "Claims account take-over; fraudulent charges"},
    },
    "STATUS": {
        "label": "Account status",
        "example_codes": {"012": "Claims paid original creditor before collection or charge-off",
                          "024": "Claims account closed by consumer",
                          "031": "Contract cancelled or rescinded"},
    },
    "PAYMENT_HISTORY": {
        "label": "Payment history / late payments",
        "example_codes": {"008": "Late due to change of address; never received statement"},
    },
    "BALANCE": {
        "label": "Balance, past due amount or credit limit",
        "example_codes": {"010": "Settlement or partial payment accepted"},
    },
    "DATES": {
        "label": "Dates (opened, DOFD, last activity, closed)",
        "example_codes": {},
    },
    "OWNERSHIP": {
        "label": "Ownership / transferred / sold",
        "example_codes": {"006": "Not aware of collection"},
    },
    "BANKRUPTCY": {
        "label": "Included in bankruptcy",
        "example_codes": {"019": "Included in the bankruptcy of another person"},
    },
    "REAGING": {
        "label": "Re-aged DOFD / obsolete",
        "example_codes": {},
    },
    "INQUIRY": {
        "label": "Inquiry",
        "example_codes": {},
    },
    "PERSONAL_INFO": {
        "label": "Personal identifying information",
        "example_codes": {},
    },
}
DISPUTE_CODES_VERIFIED = "secondary - confirm against current CDIA e-OSCAR dispute code list"


def worst_late_mark(history):
    """Most severe payment-history character, or None if the history has no lates."""
    order = "123456GHJKL"
    marks = [c for c in (history or "").upper() if c in LATE_MARKS]
    return max(marks, key=order.index) if marks else None
