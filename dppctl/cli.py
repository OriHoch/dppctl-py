import sys, json, click
import dppctl.minikube, dppctl.workload, dppctl.config, dppctl.helm


def configurations():
    return [{'id': 'minikube'},
            {'id': 'helm'}, ]


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option('--workload')
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.argument('pipeline_id')
def run(workload, verbose, debug, pipeline_id):
    try:
        active_configuration = dppctl.config.get_active_configuration()
        if active_configuration:
            provider_name = active_configuration['provider']
            workload_type = dppctl.workload.detect_type(workload)
            run_func = {'minikube-zip-url': dppctl.minikube.cli_run_from_zip_url,
                        'minikube-cur-dir': dppctl.minikube.cli_run_from_cur_dir,
                        'helm-zip-url': dppctl.helm.cli_run_from_zip_url,
                        'helm-cur-dir': dppctl.helm.cli_run_from_cur_dir}.get(
                '{}-{}'.format(provider_name, workload_type))
            if run_func:
                run_func(active_configuration, workload, verbose, debug, pipeline_id)
            else:
                raise NotImplementedError('support for running workload of type {} on provider {} was not implemented yet'.format(workload_type, provider_name))
        else:
            raise Exception('dppctl is not initialized')
    except Exception as e:
        if debug:
            raise
        else:
            print(e)
            exit(1)


@cli.command()
def providers():
    print('Available Providers:')
    for conf in configurations():
        print(' - {}'.format(conf['id']))


@cli.command()
@click.argument('provider_name')
def init(provider_name):
    try:
        init_func = {'minikube': dppctl.minikube.cli_init,
                     'helm': dppctl.helm.cli_init,}.get(provider_name)
        if init_func:
            init_func()
        else:
            raise NotImplementedError('support for "{}" provider was not implemented yet.\n'
                                      'Run "dppctl providers" to see the list of available providers'.format(provider_name))
    except Exception as e:
        print(e)
        exit(1)
