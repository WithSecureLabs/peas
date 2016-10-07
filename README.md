# PEAS
PEAS is a Python 2 library and command line application for running commands on an ActiveSync server e.g. Microsoft Exchange.

## Prerequisites

* `python` is Python 2, otherwise use `python2`
* Python [Requests](http://docs.python-requests.org/) library

## Optional installation
`python setup.py install`

# PEAS application
PEAS can be run without installation from the parent `peas` directory (containing this readme). PEAS can also be run with the command `peas` after installation.

## Running PEAS

`python -m peas [options] <server>`


## Example usage
### Check server
`python -m peas 10.207.7.100`

### Check credentials
`python -m peas --check -u luke2 -p ChangeMe123 10.207.7.100`

### Get emails
`python -m peas --emails -u luke2 -p ChangeMe123 10.207.7.100`

### Save emails to directory
`python -m peas --emails -O emails -u luke2 -p ChangeMe123 10.207.7.100`

### List file shares
`python -m peas --list-unc='\\fictitious-dc' -u luke2 -p ChangeMe123 10.207.7.100`

`python -m peas --list-unc='\\fictitious-dc\guestshare' -u luke2 -p ChangeMe123 10.207.7.100`

**Note:** Using an IP address or FQDN instead of a hostname in the UNC path may fail.

### View file on file share
`python -m peas --dl-unc='\\fictitious-dc\guestshare\fileonguestshare.txt' -u luke2 -p ChangeMe123 10.207.7.100`

### Save file from file share
`python -m peas --dl-unc='\\fictitious-dc\guestshare\fileonguestshare.txt' -o file.txt -u luke2 -p ChangeMe123 10.207.7.100`

### Command line arguments

Run `python -m peas --help` for the latest options.

    Options:
      -h, --help            show this help message and exit
      -u USER               username
      -p PASSWORD           password
      --smb-user=USER       username to use for SMB operations
      --smb-pass=PASSWORD   password to use for SMB operations
      --verify-ssl          verify SSL certificates (important)
      -o FILENAME           output to file
      -O PATH               output directory (for specific commands only, not
                            combined with -o)
      -F repr,hex,b64,stdout,stderr,file
                            output formatting and encoding options
      --check               check if account can be accessed with given password
      --emails              retrieve emails
      --list-unc=UNC_PATH   list the files at a given UNC path
      --dl-unc=UNC_PATH     download the file at a given UNC path
      
      
# PEAS library

PEAS can be imported as a library.

## Example code

    import peas

    # Create an instance of the PEAS client.
    client = peas.Peas()
    
    # Display the documentation for the PEAS client.
    help(client)

    # Disable certificate verification so self-signed certificates don't cause errors.
    client.disable_certificate_verification()

    # Set the credentials and server to connect to.
    client.set_creds({
        'server': '10.207.7.100',
        'user': 'luke2',
        'password': 'ChangeMe123',
    })

    # Check the credentials are accepted.
    print("Auth result:", client.check_auth())

    # Retrieve a file share directory listing.
    listing = client.get_unc_listing(r'\\fictitious-dc\guestshare')
    print(listing)

    # Retrieve emails.
    emails = client.extract_emails()
    print(emails)
