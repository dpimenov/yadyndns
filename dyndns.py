import time
import logging
import requests
import yapy
import settings

from daemonize import Daemonize


log_level = getattr(logging, settings.LOGLEVEL)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(log_level)
logger.propagate = False
fh = logging.FileHandler(settings.LOG_FILE, "w")
fh.setLevel(log_level)
logger.addHandler(fh)

keep_fds = [fh.stream.fileno()]


def main():
    dns = yapy.DNS(settings.PDD_TOKEN)
    _dns_record = dns_record(dns, settings.DYN_DOMAIN, settings.DYN_SUBDOMAIN)

    while True:
        try:
            my_current_ip = my_ip()
            logger.info('Server ip: {0}, DNS ip: {1}'.format(my_current_ip, _dns_record['content']))
            if my_current_ip not in _dns_record.values():
                logger.info('Update DNS ip: {0}'.format(my_current_ip))
                _dns_record = dns.edit_record(_dns_record['record_id'], settings.DYN_DOMAIN, my_current_ip)
            time.sleep(settings.CHECK_INTERVAL)
        except KeyboardInterrupt:
            break


def my_ip():
    return requests.get('https://api.ipify.org/').text


def dns_record(dns, domain, subdomain):
    records = dns.list(domain)

    try:
        record = next(filter(lambda r: r['type'] == 'A' and subdomain in r['subdomain'], records))
    except StopIteration:
        return None
    else:
        return record


if __name__ == '__main__':
    daemon = Daemonize(app='dyndns', pid=settings.PID_FILE, action=main, keep_fds=keep_fds)
    daemon.start()
