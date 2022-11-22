import json


def get_password_generator_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def update_password_generator_settings(settings):
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
