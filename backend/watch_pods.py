from kubernetes import client, config, watch

config.load_kube_config()

v1 = client.CoreV1Api()

def watch_pods(namespace):

    w = watch.Watch()

    for event in w.stream(v1.list_namespaced_pod, namespace=namespace):

        pod = event["object"]
        event_type = event["type"]

        pod_name = pod.metadata.name
        status = pod.status.phase

        print(f"Event: {event_type} Pod: {pod_name} Status: {status}")

        if pod.status.container_statuses:
            for c in pod.status.container_statuses:

                if c.state.waiting:
                    reason = c.state.waiting.reason

                    if reason in ["CrashLoopBackOff", "ImagePullBackOff"]:

                        print("⚠️ Incident detected:", pod_name)

                        return {
                            "pod": pod_name,
                            "reason": reason
                        }