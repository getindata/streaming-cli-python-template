## How to run this on VVP?

1. Install VVP (e.g. on minikube): https://docs.ververica.com/getting_started/installation.html
2. (optional) Publish docker image e.g. (Alternative approach: [here](#using-streaming-cli-to-initialize-and-build-project))
- `docker build docker <YOUR_DOCKER_REGISTRY>/ververica/pyflink:1.15.3-scala_2.12`
- `docker push <YOUR_DOCKER_REGISTRY>/ververica/pyflink:1.15.3-scala_2.12`
3. Add secrets for pulling docker images
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
        flinkImageTag: 1.15.3-scala_2.12
        entryClass: org.apache.flink.client.python.PythonDriver
        flinkVersion: '1.15'
        jarUri: 'file:///flink/lib/flink-python_2.12-1.15.2.jar'
        kind: JAR
        mainArgs: --python /app/src/flink_app.py
      kubernetes:
        pods:
          imagePullSecrets:
            - name: regcred
```
5. Job should finish successfully


### Using streaming-cli to initialize and build project

To initialize and build project you can also use dedicated tool - [streaming-cli](https://github.com/getindata/streaming-cli)

1. Use scli to create new project based on this template `scli project init --project_type python`
2. Modify code in `flink_app.py`
3. Use scli to build docker image `scli project build` - this step will create image with name declared in the first step
4. Set proper image tag `docker tag <PROJECT_NAME> <YOUR_DOCKER_REGISTRY>/ververica/<PROJECT_NAME>`
5. Push image `docker push <YOUR_DOCKER_REGISTRY>/ververica/<PROJECT_NAME>`