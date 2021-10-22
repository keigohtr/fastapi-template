# Deploy to Kubernetes

## Application deployment
### Prerequisite
- [helm](https://helm.sh/docs/intro/install)

```shell script
$ cd app
```

### Dry run
```shell script
$ helm template --values values.dev.yaml --dry-run fastapi-template .
```

### Check diff
```shell script
$ helm template --values values.dev.yaml --dry-run fastapi-template . | kubectl diff -f -
```

### Deploy
```shell script
$ helm template --values values."${STAGE}".yaml \
  --set image.tag="${TAG}" \
  --dry-run fastapi-template . > "${YAML_FILENAME}"
$ kubectl apply -f "${YAML_FILENAME}" -n default
```
