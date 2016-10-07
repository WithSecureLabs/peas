__author__ = 'Adam Rutherford'

from twisted.internet import reactor

import eas_client.activesync


def body_result(result, emails, num_emails):

    emails.append(result['Properties']['Body'])

    # Stop after receiving final email.
    if len(emails) == num_emails:
        reactor.stop()


def sync_result(result, fid, async, emails):

    assert hasattr(result, 'keys')

    num_emails = len(result.keys())

    for fetch_id in result.keys():

        async.add_operation(async.fetch, collectionId=fid, serverId=fetch_id,
            fetchType=4, mimeSupport=2).addBoth(body_result, emails, num_emails)


def fsync_result(result, async, emails):

    for (fid, finfo) in result.iteritems():
        if finfo['DisplayName'] == 'Inbox':
            async.add_operation(async.sync, fid).addBoth(sync_result, fid, async, emails)
            break


def prov_result(success, async, emails):

    if success:
        async.add_operation(async.folder_sync).addBoth(fsync_result, async, emails)
    else:
        reactor.stop()


def extract_emails(creds):

    emails = []

    async = eas_client.activesync.ActiveSync(creds['domain'], creds['user'], creds['password'],
            creds['server'], True, device_id=creds['device_id'], verbose=False)

    async.add_operation(async.provision).addBoth(prov_result, async, emails)

    reactor.run()

    return emails
