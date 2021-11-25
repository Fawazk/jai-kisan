import os
from twilio.rest import Client
from django.conf import settings


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def otpverify(mobile):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    verification = client.verify \
                     .services(settings.TWILIO_VERIFICATION_SID) \
                     .verifications \
                     .create(to='+91'+mobile, channel='sms')

    print(verification.status)
    
def verify(mobile,otp):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                           .services(settings.TWILIO_VERIFICATION_SID) \
                           .verification_checks \
                           .create(to='+91'+mobile, code=otp)

    print(verification_check.status)
    if verification_check.status=='approved':
        return True
    else:
        return False