import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_cobertura(url):
    base_shields = "https://img.shields.io/badge/coverage"
    try:
        r = requests.get(url)
        logger.info(r)
        logger.info(r.json())
        ratio = None
        for e in r.json()['results']['elements']:
            if e['name'] == 'Lines':
                ratio = round(float(e['ratio']), 2)
                break
        if ratio < 20:
            color = 'red'
        elif ratio < 80:
            color = 'yellow'
        else:
            color = 'brightgreen'
    except:
        return {'location': '{}-none-lightgrey.svg'.format(base_shields)}
    return {'location': '{}-{}%-{}.svg'.format(base_shields, ratio, color)}


def lambda_handler(event, context):
    qp = event['queryParameters']
    jenkins_url = qp['jenkins_url']
    job_name = qp['job_name']
    logger.info("jenkins_url: {}, job_name: {}".format(jenkins_url, job_name))

    url = jenkins_url + '/job/' + job_name + '/lastSuccessfulBuild/cobertura/api/json/?depth=2'
    return get_cobertura(url)
