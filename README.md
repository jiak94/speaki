# speaki

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![codecov](https://codecov.io/gh/jiak94/speaki/branch/master/graph/badge.svg?token=HST9G3RNRN)](https://codecov.io/gh/jiak94/speaki)

a api service integrated with multiple text to speech service

## Supported TTS Services

- [ ] Amazon Polly
- [ ] Google GCP
- [x] Microsoft Azure
- [ ] Aliyun

## Supported Storage Services

- [ ] Amazon S3
- [ ] Microsoft Azure

## Getting Started

### Configuration

There are two options of configure speaki

#### Option 1

Go to `templates` and modified the `.env` file. Then move the file to the root directory of the project.

#### Option 2

Open `docker-compose.yml` and set all configuration via environment variables

### Start the Service

execute `docker compose up` in the root directory of this project.
