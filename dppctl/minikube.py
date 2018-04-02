from subprocess import getstatusoutput
from time import sleep
from dppctl.config import configuration_set
import dppctl.helm


def init():
    status_exitcode, status_output = getstatusoutput('minikube status')
    if status_exitcode == 0:
        helm_status, helm_output, helm_debug = dppctl.helm.init()
        if helm_status:
            return (True,
                    'initialized minikube and helm',
                    'status_output={} helm_output={}\n{}'.format(status_output, helm_output, helm_debug))
        else:
            return (False,
                    'helm init failed',
                    'status_output={} helm_output={}\n{}'.format(status_output, helm_output, helm_debug))
    else:
        start_exitcode, start_output = getstatusoutput('minikube start')
        if start_exitcode == 0:
            return init()
        else:
            return (False,
                    'minikube status returned exit code {}, minikube start returned {}'.format(status_exitcode,
                                                                                               start_exitcode),
                    'status_output={} start_output={}'.format(status_output, start_output))


def cli_init():
    print('initializing minikube provider configuration, please wait...')
    for retry_num in range(1, 5):
        status, output, debug = init()
        if status:
            break
        print('.')
        sleep(2)
    if status:
        configuration_set('minikube', 'provider', 'minikube', init=True, cli=True)
        configuration_set('minikube', 'init_log', '{}\n{}'.format(output, debug))
        configuration_set('common', 'activeConfiguration', 'minikube', init=True, cli=True)
        print('succcessfully created and connected to the local minikube cluster')
        exit(0)
    else:
        print('failed to create or connect to the local minikube cluster')
        print(output)
        print(debug)
        exit(1)


def cli_run_from_zip_url(*args, **kwargs):
    return dppctl.helm.cli_run_from_zip_url(*args, **kwargs)


def cli_run_from_cur_dir(*args, **kwargs):
    return dppctl.helm.cli_run_from_cur_dir(*args, **kwargs)
