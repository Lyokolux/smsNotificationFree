import sys
import click
import json

from urllib.request import urlopen
from urllib.parse import quote

RESPONSES_CODE = {
    200 : "SMS sent",
    400 : "One parameter is missing (identifier, password or message).",
    402 : "Too many SMS sent.",
    403 : "Service not activated or false login/key.",
    500 : "Server Error. Please try again later."
}

#---------------------------------------
#  CREATION & CONFIGURATION DU MESSAGE
#---------------------------------------
@click.command()
@click.option("-m", "--message", 
                prompt="SMS content: ", 
                help="the message to be sent")
@click.option("-c", "--config", 
                type=click.Path(exists=True),
                prompt="Path of the config file",
                help="parse JSON file to get id and password keys")
@click.option("-v", "--verbose",
                is_flag=True,
                help="Print the HTTP response code of the request")
def sms(message, config, verbose):
    (user, password) = getKeys(config)
    url = f"https://smsapi.free-mobile.fr/sendmsg?&user={user}&pass={password}&msg={quote(message)}"
    response = urlopen(url)
    if verbose:
        status = response.getcode()
        print(f"{status} : {RESPONSES_CODE[status]}")

def getKeys(config):
    with open(config) as f:
        credential = json.loads(f.read())
    return (credential["user"], credential["password"])

if __name__ == "__main__":
    sms()
