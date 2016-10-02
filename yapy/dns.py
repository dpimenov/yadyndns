import requests


class DNS:
    host = 'pddimp.yandex.ru'

    def __init__(self, pdd_token):
        self.headers = {'PddToken': pdd_token}

    def list(self, domain):
        url = 'https://{host}/api2/admin/dns/list?domain={domain}'
        response = requests.get(url.format(host=self.host, domain=domain), headers=self.headers).json()
        records = response['records']

        return records

    def edit_record(self, record_id, domain, content):
        url = 'https://{host}/api2/admin/dns/edit'
        data = {'record_id': record_id, 'domain': domain, 'content': content}
        response = requests.post(url.format(host=self.host), data=data, headers=self.headers).json()

        return response['record']
