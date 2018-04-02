from subprocess import getstatusoutput
import json
import subprocess


def is_pod_running(id, cli_debug=False):
    cmd = 'kubectl get pod pipeline-{} -o json'.format(id)
    if cli_debug:
        print('running kubectl command: {}'.format(cmd))
    get_pod_exitcode, get_pod_output = getstatusoutput('kubectl get pod pipeline-{} -o json'.format(id))
    if get_pod_exitcode == 0:
        pod_phase = json.loads(get_pod_output).get('status', {}).get('phase')
        if cli_debug:
            print('pod_phase={}'.format(pod_phase))
        if pod_phase == 'Running':
            return True
    elif cli_debug:
        print(get_pod_output)
    return False


def cli_pod_log(id):
    subprocess.run('kubectl logs pipeline-{id} -c sync -f & SYNC_LOG_PID=$!; sleep 2; \
                    kubectl logs pipeline-{id} -c pipeline -f & PIPELINE_LOG_PID=$!; sleep 1; \
                    while ! kubectl logs pipeline-{id} -c pipeline --tail 10 | grep "done with exit code " >/dev/null; \
                    do sleep 1; done; \
                    kill $SYNC_LOG_PID >/dev/null 2>&1; kill $PIPELINE_LOG_PID >/dev/null 2>&1; sleep 1; \
                    kill -9 $SYNC_LOG_PID >/dev/null 2>&1; kill -9 $PIPELINE_LOG_PID >/dev/null 2>&1; \
                    '.format(id=id),
                    shell=True,)


def delete_pod(id):
    assert subprocess.run('kubectl delete --force --ignore-not-found --include-uninitialized --now \
                                          pod pipeline-{}'.format(id), shell=True).returncode == 0
