import json


def get_config():
    with open('config.json', 'r', encoding='utf-8') as json_config:
        config = json.load(json_config)
        return config


def main():
    config = get_config()
    print(config)
    print(config['telegram']['bot_token'])


if __name__ == '__main__':
    main()
