import pyotp

def send_otp(request):

    secret_key=pyotp.random_base32()
    totp=pyotp.TOTP(secret_key,digits=4)
    otp=totp.now()
    request.session['otp']=otp
    return otp