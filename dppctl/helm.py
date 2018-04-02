from subprocess import getstatusoutput
from time import sleep
import dppctl.kubectl, dppctl.config
import re, uuid, requests


def get_helm_install_cmd(id, chart, values):
    set_values = ' '.join(['--set {}={}'.format(k, v) for k, v in values.items()])
    return 'helm install {chart} -n dppctl-pipelines-{id} --set id={id} {set_values}'.format(chart=chart,
                                                                                             id=id,
                                                                                             set_values=set_values)


def start_pipeline_pod(id, chart, values, cli_debug=False, max_retries=20, sleep_multiplier_seconds=.5):
    install_exitcode, install_output, pod_running = None, None, None
    for try_num in range(1, max_retries):
        if cli_debug and try_num > 1:
            print('starting pipeline pod ({}/{})...'.format(try_num, max_retries))
        if install_exitcode != 0:
            helm_install_cmd = get_helm_install_cmd(id, chart, values)
            if cli_debug:
                print('running helm install command: {}'.format(helm_install_cmd))
            install_exitcode, install_output = getstatusoutput(helm_install_cmd)
        if install_exitcode == 0:
            pod_running = dppctl.kubectl.is_pod_running(id, cli_debug)
            if pod_running:
                break
        elif cli_debug:
            print(install_output)
        sleep(try_num * sleep_multiplier_seconds)
    if install_exitcode != 0 or not pod_running:
        raise Exception('failed to start pod id {}: {}'.format(id, install_output))


def init():
    init_exitcode, init_output = getstatusoutput('helm init --history-max 1 --upgrade --wait')
    if init_exitcode == 0:
        return (True,
                'initialized helm',
                'init_output={}'.format(init_output))
    else:
        return (False,
                'helm init returned exit code {}'.format(init_exitcode),
                'init_output={}'.format(init_output))


def cli_init():
    print('initializing local helm provider configuration, please wait...')
    status, output, debug = init()
    if status:
        dppctl.config.configuration_set('helm', 'provider', 'helm', init=True, cli=True)
        dppctl.config.configuration_set('helm', 'init_log', '{}\n{}'.format(output, debug))
        dppctl.config.configuration_set('common', 'activeConfiguration', 'helm', init=True, cli=True)
        print('succcessfully created and connected to a cluster via local helm')
        exit(0)
    else:
        print('failed to create or connect to the cluster via local helm')
        print(output)
        print(debug)
        exit(1)


def cli_run_from_zip_url(active_configuration, workload, verbose, debug, pipeline_id):
    id = re.sub("-", "", str(uuid.uuid4()))
    if '.zip#' in workload:
        zip_url, zip_url_path = workload.split('.zip#')
        zip_url += '.zip'
    else:
        zip_url, zip_url_path = workload, ''
    run_params = pipeline_id
    if verbose:
        run_params = '--verbose {}'.format(run_params)
    if debug:
        print('id={}\nzip_url={}\nzip_url_path={}\nrun_params={}'.format(id, zip_url, zip_url_path, run_params))
    print('starting a pod')
    start_pipeline_pod(id,
                       'https://github.com/OriHoch/dppctl-pipelines/archive/v0.0.2.tar.gz',
                       {'workload': zip_url,
                        'workloadPath': zip_url_path,
                        'dppRunParams': run_params,
                        'postPipelinesSleepSeconds': 3600,
                        'enableInfo': '1'},
                       cli_debug=debug)
    dppctl.kubectl.cli_pod_log(id)
    dppctl.kubectl.delete_pod(id)
    exit(0)


def cli_run_from_cur_dir(active_configuration, workload, verbose, debug, pipeline_id):
    raise NotImplementedError('helm run from current directory is not implemented yet')
