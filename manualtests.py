from rest_framework import status
import requests
import json


def uploadClients(clients, url, headers):
    for client in clients:
        response = requests.post(url, data=json.dumps(client), headers=headers)

        if response.status_code != status.HTTP_201_CREATED:
            return 'failed to upload clients, response code: {}'.format(response.status_code)

    return 'successfully created {} client(s)'.format(len(clients))


def testMailingCreation(mailing, url, headers):
    response = requests.post(url, data=json.dumps(mailing), headers=headers)

    if response.status_code != status.HTTP_201_CREATED:
        return 'FAILED, response code: {}'.format(response.status_code)

    return 'OK'
    

def testMailingUpdate(data, newdata, url, headers):
    mailing = requests.post(url, data=json.dumps(data), headers=headers).json()
    response = requests.patch(url + str(mailing['object']['id']), data=json.dumps(newdata), headers=headers)
    
    if response.status_code != status.HTTP_200_OK:
        return 'FAILED, response code: {}'.format(response.status_code)

    return 'OK'


if __name__ == "__main__":

    createClientURL = 'http://localhost:8000/clients/'
    createMailingURL = 'http://localhost:8000/mailinglists/'
    generalStatURL = 'http://localhost:8000/generalstat/'
    detailedStatURL = 'http://localhost:8000/deatiledstat/'

    headers = {
        'Content-Type': 'application/json'
    }

    with open("testdata.json", "r") as file:
        data = json.loads(file.read())

    print(
        uploadClients(
            data['clients'],
            url = createClientURL,
            headers = headers
        )
    )
    print(
        'late mailing creation by tag - ',
        testMailingCreation(
            data['mailings']['late by tag'],
            url = createMailingURL,
            headers = headers
        )
    )
    print(
        'late mailing creation by operator code - ',
        testMailingCreation(
            data['mailings']['late by operator code'],
            url = createMailingURL,
            headers = headers
        )
    )
    print(
        'scheduled mailing creation - ',
        testMailingCreation(
            data['mailings']['scheduled by opertaor code'],
            url = createMailingURL,
            headers = headers
        )
    )
    print(
        'scheduled mailing update - ',
        testMailingUpdate(
            data = data['mailings']['scheduled to be updated'],
            newdata = data['mailings']['mailing time and text update'],
            url = createMailingURL,
            headers = headers
        )
    )
    print(
        'expired mailing creation - ',
        testMailingCreation(
            data['mailings']['expired'],
            url = createMailingURL,
            headers = headers
        )
    )



    