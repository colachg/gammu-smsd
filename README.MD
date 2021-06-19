## Preface

ENGLISH | [中文](README.CN.MD)

I have three SIM cards, but my phone can only carry two. So I have to left one somewhere. At the sametime, 
I need receive sms sent to it. I need a solution for this situation, that is the project created. 

## Requirements

* Container runtime (Ubuntu or Centos, Ubuntu is preferred)
* LTE or 3G USB dongle (Used as a phone to send or receive sms, check [here](https://wammu.eu/phones/) to find support devices) 

## Feature

* Forward sms to your mobile app (such as Telegram)
* Reply important sms inside mobile app

## Quick Start

1. Get necessary token inside the `docker-compose.yaml` and change them to yours.
2. Then set a reverse proxy to your container runtime host:
   ```
      https://example.com:8443 {
         tls {
         dns cloudflare {env.CF_API_KEY}
         }
         reverse_proxy /bot_token 192.168.199.2:5000
      }
   ```
3. Make your USB device name permanent (here `/dev/ec20` is default) according to [it](https://wiki.debian.org/udev#persistent-name), 
   otherwise you should change USB path in `docker-compose.yaml` 
4. `docker-compose up -d` to start containers
5. Enjoy it and have fun.

## Reference

- https://post.smzdm.com/p/a4wme8zx/
- https://docs.gammu.org/faq/general.html#device-name-always-changes-on-linux-how-to-solve-that
- https://wiki.debian.org/udev#persistent-name
- https://docs.gammu.org/project/index.html
- https://docs.aiogram.dev/en/latest/

