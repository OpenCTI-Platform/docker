import uuid
import yaml
import dotenv

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
    dotenv.set_key(dotenv_file, key, val)

custom = {
    'OPENCTI_ADMIN_EMAIL': 'admin@opencti.io',
    'OPENCTI_ADMIN_PASSWORD': 'ChangeMe',
    'OPENCTI_ADMIN_TOKEN': 'ChangeMe',
    'MINIO_ACCESS_KEY': 'ChangeMeAccess',
    'MINIO_SECRET_KEY': 'ChangeMeKey',
    'RABBITMQ_DEFAULT_USER': 'guest',
    'RABBITMQ_DEFAULT_PASS': 'guest'
}

for key, val in custom.items():
    dotenv.set_key(dotenv_file, key, val)

