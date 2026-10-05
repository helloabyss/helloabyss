"""Credit Repair Organizations Act (15 U.S.C. § 1679 et seq.) compliance texts and rules.

DISCLOSURE is § 1679c(a) verbatim, as supplied from the U.S. Code. It must be given as a
separate document before any contract (§ 1679c(b)) and the signed acknowledgment kept
for 2 years (§ 1679c(c)).

The contract and cancellation-notice wording follows §§ 1679d(b) and 1679e(b). It was
written from the statute's requirements, not copied from it; have counsel confirm the
exact wording before launch (see VERIFY_BEFORE_LAUNCH).
"""

import hashlib
from datetime import datetime, time, timedelta

from cfads.pipeline import add_business_days

DISCLOSURE_TITLE = "Consumer Credit File Rights Under State and Federal Law"

DISCLOSURE = """Consumer Credit File Rights Under State and Federal Law

You have a right to dispute inaccurate information in your credit report by contacting the credit bureau directly. However, neither you nor any ‘credit repair’ company or credit repair organization has the right to have accurate, current, and verifiable information removed from your credit report. The credit bureau must remove accurate, negative information from your report only if it is over 7 years old. Bankruptcy information can be reported for 10 years.

You have a right to obtain a copy of your credit report from a credit bureau. You may be charged a reasonable fee. There is no fee, however, if you have been turned down for credit, employment, insurance, or a rental dwelling because of information in your credit report within the preceding 60 days. The credit bureau must provide someone to help you interpret the information in your credit file. You are entitled to receive a free copy of your credit report if you are unemployed and intend to apply for employment in the next 60 days, if you are a recipient of public welfare assistance, or if you have reason to believe that there is inaccurate information in your credit report due to fraud.

You have a right to sue a credit repair organization that violates the Credit Repair Organization Act. This law prohibits deceptive practices by credit repair organizations.

You have the right to cancel your contract with any credit repair organization for any reason within 3 business days from the date you signed it.

Credit bureaus are required to follow reasonable procedures to ensure that the information they report is accurate. However, mistakes may occur.

You may, on your own, notify a credit bureau in writing that you dispute the accuracy of information in your credit file. The credit bureau must then reinvestigate and modify or remove inaccurate or incomplete information. The credit bureau may not charge any fee for this service. Any pertinent information and copies of all documents you have concerning an error should be given to the credit bureau.

If the credit bureau’s reinvestigation does not resolve the dispute to your satisfaction, you may send a brief statement to the credit bureau, to be kept in your file, explaining why you think the record is inaccurate. The credit bureau must include a summary of your statement about disputed information with any report it issues about you.

The Federal Trade Commission regulates credit bureaus and credit repair organizations. For more information contact:

The Public Reference Branch
Federal Trade Commission
Washington, D.C. 20580"""

DISCLOSURE_SHA256 = hashlib.sha256(DISCLOSURE.encode()).hexdigest()
RETENTION_YEARS = 2

VERIFY_BEFORE_LAUNCH = [
    "Contract terms (§ 1679d(b)) and Notice of Cancellation wording (§ 1679e(b)) - confirm against statute",
    "Whether 'business day' for cancellation excludes Saturdays in your reading (this code excludes "
    "weekends and federal holidays, which gives the customer the longer window)",
    "State credit services organization registration/bond requirements for every state you sell in",
    "That charging at delivery satisfies § 1679b(b) for this product",
]


def cancellation_deadline(signed_at):
    """Midnight at the end of the 3rd business day after signing (§ 1679e(a))."""
    day = add_business_days(signed_at.date(), 3)
    return datetime.combine(day, time(23, 59, 59))


def contract_text(company, consumer_name, price_cents, signed_on=None):
    price = f"${price_cents / 100:,.2f}"
    deadline = cancellation_deadline(signed_on or datetime.now())
    return f"""SERVICE AGREEMENT

Between {company['name']}, {company['address']} ("we"), and {consumer_name} ("you").

1. SERVICES. We provide software that (a) reviews the credit report information and documents you
enter for inaccuracies under the Fair Credit Reporting Act and related laws, and (b) prepares dispute
letters, based only on facts and documents you supply, for you to review, sign and mail yourself. We
do not contact credit bureaus or creditors for you. We do not prepare disputes of information you
tell us is accurate.

2. TIME TO PERFORM. Your audit is shown as soon as you enter your information. Your letters are
delivered for download immediately after payment, which can be made only after your cancellation
period below has ended.

3. PAYMENT. Total price: {price}, one time. You are not charged anything until the services in
section 1 are fully performed and your letters are ready to deliver. There are no subscriptions or
recurring charges.

4. NO GUARANTEE. We cannot and do not promise that any item will be removed or that your credit score
will change. Accurate, current and verifiable information cannot lawfully be removed.

5. YOUR RESPONSIBILITY. The information and documents you provide must be true. Disputes must be
truthful; knowingly false disputes can harm you and others.

6. NOT LEGAL ADVICE. We are not a law firm. For legal claims, consult a licensed attorney.

7. RECORDS. We keep your signed acknowledgment of the Consumer Credit File Rights statement for
{RETENTION_YEARS} years as the law requires. You can delete your case and documents at any time.

YOU MAY CANCEL THIS CONTRACT WITHOUT PENALTY OR OBLIGATION AT ANY TIME BEFORE MIDNIGHT OF THE 3RD
BUSINESS DAY AFTER THE DATE ON WHICH YOU SIGNED THE CONTRACT. SEE THE ATTACHED NOTICE OF CANCELLATION
FORM FOR AN EXPLANATION OF THIS RIGHT.

Cancellation deadline for this agreement: {deadline:%B %d, %Y} at midnight."""


def cancellation_notice(company, signed_on):
    deadline = cancellation_deadline(signed_on)
    return f"""NOTICE OF CANCELLATION

You may cancel this contract, without any penalty or obligation, at any time before midnight of the
3rd business day which begins after the date the contract is signed by you.

To cancel this contract, use the Cancel button in your account, or mail or deliver a signed, dated
copy of this cancellation notice, or any other written notice, to {company['name']} at
{company['address']} before midnight on {deadline:%B %d, %Y}.

I hereby cancel this transaction.

Date: ____________________

Purchaser's signature: ______________________________"""
