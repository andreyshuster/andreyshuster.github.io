+++
title = "Setting Up Telegram Alerts for Prometheus - A Journey"
date = "2026-01-10T21:59:22-06:00"
draft = false
#
# description is optional
#
# description = "An optional description for SEO. If not provided, an automatically created summary will be used."

tags = ["homelab","alertmanager","prometheus","devops"]
+++

Today I added something useful and long overdue to my homelab.
My Spectrum router does not cover the whole house (it is not in the middle, but in a side room which is my home office), so I purchased an additional WiFi pod from Spectrum to create a mesh network. Unfortunately, the outlet where the pod is plugged in is a bit loose, so sometimes it disconnects and then Netflix starts to misbehave.

I have a small k3s cluster at home, built as an experiment on top of two Raspberry Pis (RP5 and RP Zero W 2) and an old laptop, and I thought it would be a good idea to use the cluster to solve this problem.

## What We Wanted

I use Telegram a lot, so I decided I wanted to get a Telegram notification when our Spectrum pod (192.168.1.135) goes down.

## Plan

- Set up Alertmanager
- Add the pod as a target to blackbox-exporter
- Create the alert rule
- Configure the integration with Telegram
- Test it

## The Discovery Phase

Did Helm install Alertmanager with Prometheus?

```bash
$ kubectl get pods -n monitoring | grep alert
prometheus-alertmanager-0    1/1     Running   0      6d
```

Cool, it is running, but completely useless without proper configuration.

## Adding the Probe Target

We are already using blackbox-exporter to ICMP ping a bunch of hosts (routers, laptops, servers, DNS servers, etc.), so adding our Spectrum pod was easy: just drop it into the targets list.

```yaml
- 192.168.1.135    # Spectrum pod
```

## Creating the Alert Rule

Then we needed an actual alert rule. A simple one that fires when any of our monitored hosts fails the ICMP probe for more than 2 minutes:

```yaml
- alert: HostDown
  expr: probe_success{job="blackbox"} == 0
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Spectrum POD {{ $labels.instance }} is down"
    description: "ICMP probe to {{ $labels.instance }} has failed for more than 2 minutes."
```

Pretty straightforward: if `probe_success` is 0, something is wrong.

## The Telegram Integration (aka The Fun Part)

Here is where it got interesting. We wanted to send alerts to Telegram, but we had a problem: **how do you configure secrets without committing them to GitHub?**

The solution:

1. Add the actual config file to `.gitignore`.
2. Create a Kubernetes Secret with the real Telegram bot token and chat ID.
3. Configure Helm to use this Secret.

Seemed perfect. Except…

## The Plot Twist

After applying everything with `helm upgrade`, Alertmanager was still using the default receiver. What gives?

It turned out the `configFromSecret` parameter we set in the Helm values was not actually working. The Helm chart kept creating and using a ConfigMap with the default config, completely ignoring our fancy Secret.

Classic Kubernetes moment.

## The Fix

Sometimes you have to be pragmatic. Instead of fighting with Helm, we just:

1. Pulled the config from our Secret.
2. Manually updated the ConfigMap.
3. Restarted the Alertmanager pod.

```bash
kubectl get secret alertmanager-telegram-config -n monitoring -o jsonpath='{.data.alertmanager\.yml}' | base64 -d > /tmp/alertmanager-telegram.yml

kubectl create configmap prometheus-alertmanager --from-file=alertmanager.yml=/tmp/alertmanager-telegram.yml -n monitoring --dry-run=client -o yaml | kubectl apply -f -

kubectl delete pod prometheus-alertmanager-0 -n monitoring
```

Boom. Then we verified the config:

```bash
$ curl -s http://localhost:9093/api/v2/status | jq -r '.config.route.receiver'
telegram
```


## Testing Time

We sent a test alert via the Alertmanager API:

```bash
curl -X POST http://localhost:9093/api/v2/alerts -H "Content-Type: application/json" -d '[{
  "labels": {
    "alertname": "HostDown",
    "instance": "192.168.1.135",
    "severity": "critical",
    "job": "blackbox"
  },
  "annotations": {
    "summary": "Spectrum POD 192.168.1.135 is down",
    "description": "ICMP probe to 192.168.1.135 has failed for more than 2 minutes."
  }
}]'
```

And  Telegram notification received.

## Lessons Learned

1. **Helm charts do not always work the way you expect** – sometimes you have to work around them.
2. **ConfigMaps get overwritten by Helm** – this is now documented in the troubleshooting guide.
3. **Testing with the API is much faster** – do not wait 2 minutes for real alerts to fire.
4. **Never commit secrets to Git** – even when it seems convenient.

## What’s Next?

Now that we have the basic setup working, we could:

- Add more alert rules (high CPU, disk space, memory, etc.).
- Set up different notification channels for different severity levels.
- Add some silencing rules for maintenance windows.
- Fine-tune the group intervals and repeat intervals.

But for now, alerts are going to Telegram, and that is a win.

*P.S. Don't forget to run those troubleshooting commands after any `helm upgrade` because the ConfigMap will get reset.*
