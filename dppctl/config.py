from yaml import load, dump
import os


def configuration_set(id, key, value, init=False, cli=False):
    dppctl_conf_path = os.environ.get('DPPCTL_CONF_PATH')
    if not dppctl_conf_path and os.environ.get('HOME'):
        dppctl_conf_path = os.path.join(os.environ['HOME'], '.dppctl')
    if dppctl_conf_path:
        if not os.path.exists(dppctl_conf_path):
            if init:
                if cli:
                    print('initializing dppctl configuration at {}'.format(dppctl_conf_path))
                os.mkdir(dppctl_conf_path)
            else:
                raise Exception('dppctl is not initialized')
        dppctl_conf_file = os.path.join(dppctl_conf_path, '{}.yaml'.format(id))
        if os.path.exists(dppctl_conf_file):
            with open(dppctl_conf_file) as f:
                conf = load(f.read())
            conf[key] = value
            with open(dppctl_conf_file, 'w') as f:
                f.write(dump(conf, default_flow_style=False))
        elif init:
            with open(dppctl_conf_file, 'w') as f:
                f.write(dump({key: value}, default_flow_style=False))
        else:
            raise Exception('dppctl provider is not configured')
    else:
        raise Exception('failed to find a dppctl configuration path')


def configuration_get(id):
    dppctl_conf_path = os.environ.get('DPPCTL_CONF_PATH')
    if not dppctl_conf_path and os.environ.get('HOME'):
        dppctl_conf_path = os.path.join(os.environ['HOME'], '.dppctl')
    if dppctl_conf_path and os.path.exists(dppctl_conf_path):
        dppctl_conf_file = os.path.join(dppctl_conf_path, '{}.yaml'.format(id))
        if os.path.exists(dppctl_conf_file):
            with open(dppctl_conf_file) as f:
                conf = load(f.read())
            return conf
    return {}


def get_active_configuration():
    active_configuration_id = configuration_get('common').get('activeConfiguration')
    if active_configuration_id:
        return configuration_get(active_configuration_id)
    else:
        return None
