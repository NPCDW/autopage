import json


def get_config():
    with open('data/config.json', 'r', encoding='utf-8') as config_file:
        json_config = json.load(config_file)
        return json_config


config = get_config()


def main():
    json_config = get_config()
    print(json_config)
    print(json_config['telegram']['bot_token'])


if __name__ == '__main__':
    main()
