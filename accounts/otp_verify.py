import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def otpverify(mobile):
    account_sid = 'AC3ef75ff7814967643ea18e41eaacf2d3'
    auth_token = '43a05ac89a751fdec685b1fc183a55d3'
    client = Client(account_sid, auth_token)

    verification = client.verify \
                     .services('VAeb43b67f74da9bff1024c316c0d3f728') \
                     .verifications \
                     .create(to='+91'+mobile, channel='sms')

    print(verification.status)
    
def verify(mobile,otp):
    account_sid = 'AC3ef75ff7814967643ea18e41eaacf2d3'
    auth_token = '43a05ac89a751fdec685b1fc183a55d3'
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                           .services('VAeb43b67f74da9bff1024c316c0d3f728') \
                           .verification_checks \
                           .create(to='+91'+mobile, code=otp)

    print(verification_check.status)
    if verification_check.status=='approved':
        return True
    else:
        return False