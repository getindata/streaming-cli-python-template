## How to run this on VVP?

1. Install VVP (e.g. on minikube): https://docs.ververica.com/getting_started/installation.html
2. mvn clean package
3. (optional) Publish docker image e.g.
- `docker build docker <YOUR_DOCKER_REGISTRY>/ververica/pyflink:1.15.3-scala_2.12`
- `docker push <YOUR_DOCKER_REGISTRY>/ververica/pyflink:1.15.3-scala_2.12`
4. Add secrets for pulling docker images
- `kubectl create secret docker-registry regcred --docker-server=<YOUR_DOCKER_REGISTRY> --docker-username=[gitlab-username] --docker-password=[token] --docker-email=[email] -n vvp-jobs`
4. Create a deployment
- upload shaded jar in the UI (note: you might have to edit YAML manually for the first time to make it work)
- go to the YAML tab and add:
```yaml
spec:
  template:
    spec:
      artifact:
        flinkImageRegistry: <YOUR_DOCKER_REGISTRY>
        flinkImageRepository: ververica/pyflink
        flinkImageTag: 1.11.2-scala_2.12
      kubernetes:
        pods:
          imagePullSecrets:
            - name: regcred
```
5. Job should finish successfully

In general: we package program with the jar and execute it on VVP.
Alternative approach: use persistent volume.
