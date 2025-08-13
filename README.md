## 정보조회 이미지 빌드 배포

```

docker build -t ghcr.io/chambittrace/k8s_collector:latest .
docker push ghcr.io/chambittrace/k8s_collector:latest

kubectl rollout restart deployment k8s-collector -n collecter
kubectl logs -l app=k8s-collector -n collecter -f

```

## 파드 생성 테스트

```

kubectl run test-nginx --image=nginx --restart=Never -n collecter


kubectl delete pod test-nginx -n collecter

```