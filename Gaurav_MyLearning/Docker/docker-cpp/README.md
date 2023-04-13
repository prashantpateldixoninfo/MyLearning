https://medium.com/@mfcollins3/shipping-c-programs-in-docker-1d79568f6f52

$docker build -f dockerfiles/cpp/Dockerfile . -t cpp-build-base:0.1.0
$docker build -f dockerfiles/exe/Dockerfile . -t hello-world:1.0.0
$docker run --rm -it hello-world:1.0.0

