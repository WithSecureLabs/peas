# PEAS
PEAS is a Python 2 library and command line application for running commands on an ActiveSync server e.g. Microsoft Exchange. It is based on [research](https://labs.mwrinfosecurity.com/blog/accessing-internal-fileshares-through-exchange-activesync) into Exchange ActiveSync protocol by Adam Rutherford and David Chismon of MWR.

## Prerequisites

* `python` is Python 2, otherwise use `python2`
* Python [Requests](http://docs.python-requests.org/) library

## Significant source files
Path | Functionality
--- | ---
`peas/__main__.py` | The command line application.
`peas/peas.py` | The PEAS client class that exclusively defines the interface to PEAS.
`peas/py_activesync_helper.py` | The helper functions that control the interface to pyActiveSync.
`peas/pyActiveSync/client` | The pyActiveSync EAS command builders and parsers.

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
      
      
## PEAS library

PEAS can be imported as a library.

### Example code

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

## Extending

To extend the functionality of PEAS, there is a four step process:

1. Create a builder and parser for the EAS command if it has not been implemented in `pyActiveSync/client`. Copying an existing source file for another command and then editing it has proved effective. The [Microsoft EAS documentation](https://msdn.microsoft.com/en-us/library/ee202197%28v=exchg.80%29.aspx) describes the structure of the XML that must be created and parsed from the response.

2. Create a helper function in `py_activesync_helper.py` that connects to the EAS server over HTTPS, builds and runs the command to achieve the desired functionality. Again, copying an existing function such as `get_unc_listing` can be effective.

3. Create a method in the `Peas` class that calls the helper function to achieve the desired functionality. This is where PEAS would decide which backend helper function to call if py-eas-client was also an option.

4. Add command line support for the feature to the PEAS application by editing `peas/__main__.py`. A new option should be added that when set, calls the method created in the previous step.

 
## Limitations 
 
PEAS has been tested on Kali 2.0 against Microsoft Exchange Server 2013 and 2016. The domain controller was Windows 2012 and the Exchange server was running on the same machine. Results with other configurations may vary.

py-eas-client support is limited to retrieving emails and causes a dependency on Twisted. It was included when the library was being evaluated but it makes sense to remove it from PEAS now, as all functionality can be provided by pyActiveSync.

The licence may be restrictive due to the inclusion of pyActiveSync, which uses the GPLv2.

The requirement to know the hostname of the target machine for file share access may impede enumeration.
