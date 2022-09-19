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

## API Documentations

### Create Text to Speech Task

- url: `/speak`
- method: `POST`
- parameters:

  | Name     | Type   | Required | Note                                               |
  | -------- | ------ | -------- | -------------------------------------------------- |
  | service  | string | Yes      | currently, only `azure` is supported               |
  | text     | string | Yes      | the text wanted to be read out                     |
  | speed    | string | No       | `fast`, `regular` and `slow`, default is `regular` |
  | voices   | string | No       | voice name would like to use                       |
  | callback | string | No       | url to receive notification when task is completed |

- response:

  ```json
  {
    "task_id": "xxxxxx",
    "msg": "xxxxxxx",
    "code": 0
  }
  ```

### Get Voices Name

- url: `/vocies`
- method: `GET`
- parameters:

  | Name    | Type   | Required | Note                               |
  | ------- | ------ | -------- | ---------------------------------- |
  | service | string | Yes      | currently, on `azure` is supported |
  | lang    | string | Yes      | locale of voices e.g en/ja/zh      |

- response:

  ```json
  {
    "voices": [
      {
        "name": "en-AU-NatashaNeural",
        "gender": "female"
      },
      {
        "name": "en-AU-WilliamNeural",
        "gender": "male"
      },
      {
        "name": "en-CA-ClaraNeural",
        "gender": "female"
      },
      {
        "name": "en-CA-LiamNeural",
        "gender": "male"
      }
    ]
  }
  ```

### Get Status of task

- url: `/status/{task_id}`
- method: `GET`
- response:

  ```json
  {
    "status": "pending",
    "code": 0,
    "msg": "string",
    "download_url": "string"
  }
  ```
