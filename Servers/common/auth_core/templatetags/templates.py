from django import template

register = template.Library()

@register.simple_tag
def fingerprint():
# initialize sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    except Exception as e:
        print('The fingerprint sensor failed.')
        print('Exception message: ' + str(e))
        exit(1)

    ## Tries to read image and download it
    try:
        print('Waiting for finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        print('Downloading image (this may take a while)...')
        imageDestination = '/home/logan/School/cps410/FingerPrintVerification/Images/fingerprint.bmp'
        f.downloadImage(imageDestination)
        print('The image was saved to "' + imageDestination + '".')
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
