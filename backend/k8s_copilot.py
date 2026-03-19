from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

def get_problem_pods(namespace):

    pods = v1.list_namespaced_pod(namespace)

    issues = []

    for pod in pods.items:

        pod_name = pod.metadata.name

        if pod.status.container_statuses:

            for container in pod.status.container_statuses:

                if container.state.waiting:

                    reason = container.state.waiting.reason
                    message = container.state.waiting.message

                    logs = ""

                    try:
                        logs = v1.read_namespaced_pod_log(
                            name=pod_name,
                            namespace=namespace,
                            tail_lines=30
                        )
                    except:
                        logs = "Unable to fetch logs"

                    issues.append({
                        "pod": pod_name,
                        "reason": reason,
                        "message": message,
                        "logs": logs
                    })

    return issues