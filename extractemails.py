"""Example script using PEAS to extract emails."""

__author__ = 'Adam Rutherford'

import sys
import os
import time
import random
import subprocess
from pprint import pprint

import peas
import _creds


def main():

    peas.show_banner()

    client = peas.Peas()

    client.set_creds(_creds.CREDS)

    print("Extracting all emails with pyActiveSync")
    client.set_backend(peas.PY_ACTIVE_SYNC)

    emails = client.extract_emails()

    pprint(emails)
    print

    print("Extracting all emails with py-eas-client")
    client.set_backend(peas.PY_EAS_CLIENT)

    emails = client.extract_emails()

    pprint(emails)
    print


if __name__ == '__main__':
    main()
