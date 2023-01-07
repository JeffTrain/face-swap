docker build -t jefftian/face-swap:"$1" .
docker images
docker run --network host -e CI=true -d -p 127.0.0.1:5000:5000 --name face-swap jefftian/face-swap:"$1"
docker ps | grep -q face-swap
docker ps -aqf "name=face-swap$"
docker push jefftian/face-swap:"$1"
docker logs $(docker ps -aqf name=face-swap$)
curl localhost:5000 || docker logs $(docker ps -aqf name=face-swap$)
docker kill face-swap || echo "face-swap killed"
docker rm face-swap || echo "face-swap removed"
