import random
import string
import uuid
import yaml
import dotenv


def generate_random_text(length: int = 15) -> str:
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


with open("docker-compose.yml", 'r') as ymlfile:
    docker_config = yaml.load(ymlfile, Loader=yaml.BaseLoader)

docker_services = docker_config['services'].keys()

uid_dict = dict()
for service in docker_services:
    if service.startswith('connector'):
        new_name = service.replace('-', '_')
        new_name = new_name.upper()
        new_name += '_ID'
        uid_dict[new_name] = str(uuid.uuid4())
    elif service in ['opencti']:
        uid_dict['OPENCTI_ADMIN_TOKEN'] = str(uuid.uuid4())

dotenv_file = dotenv.find_dotenv()
if dotenv_file == '':
    with open('.env', 'w') as fp:
        pass
    dotenv_file = '.env'
dotenv.load_dotenv(dotenv_file)

for key, val in uid_dict.items():
    if dotenv.get_key(dotenv_file, key) is None:
        dotenv.set_key(dotenv_file, key, val, quote_mode='never')

custom = {
    'OPENCTI_ADMIN_EMAIL': 'admin@opencti.io',
    'OPENCTI_ADMIN_PASSWORD': generate_random_text(),
    'MINIO_ACCESS_KEY': generate_random_text(),
    'MINIO_SECRET_KEY': generate_random_text(),
    'RABBITMQ_DEFAULT_USER': generate_random_text(),
    'RABBITMQ_DEFAULT_PASS': generate_random_text()
}

for key, val in custom.items():
    if dotenv.get_key(dotenv_file, key) is None:
        dotenv.set_key(dotenv_file, key, val, quote_mode='never')
