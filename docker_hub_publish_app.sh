#!/bin/bash
docker build -f Dockerfile.app -t keywords-stats-app:latest .
docker tag keywords-stats-app:latest mvkan/keywords-stats-app:latest
docker push mvkan/keywords-stats-app:latest