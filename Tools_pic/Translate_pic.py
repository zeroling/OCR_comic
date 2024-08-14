import json
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


def translate(text_list, target_language, ID, Key):
    access_key = ID  # https://console.volcengine.com/iam/keymanage/
    secret_key = Key

    service_info = ServiceInfo(
        'translate.volcengineapi.com',
        {'Content-Type': 'application/json'},
        Credentials(access_key, secret_key, 'translate', 'cn-north-1'),
        5,
        5
    )
    query = {
        'Action': 'TranslateText',
        'Version': '2020-06-01'
    }
    api_info = {
        'translate': ApiInfo('POST', '/', query, {}, {})
    }
    service = Service(service_info, api_info)
    # print(text_list)
    body = {
        'TargetLanguage': target_language,
        'TextList': text_list,
    }
    res = service.json('translate', {}, json.dumps(body))
    translations = [item['Translation'] for item in json.loads(res)['TranslationList']]
    return translations
