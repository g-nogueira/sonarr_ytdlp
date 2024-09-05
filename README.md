# sonarr_ytdlp (fork of sonarr_youtubedl)

This fork aims to solve some of the problems I faced while using the repo.

**Why?** Because the original repo has quite a few open PRs that are already stale. Some of the PR's were already ready to merge but were never merged.  
**What issues do I have?** I will be opening the issues on the original repo and solving them here, trying to open PRs there when possible.

**Fixed Issues**
- Error "This episode is for premium members only" from Crunchyroll [#6](https://github.com/g-nogueira/sonarr_ytdlp/issues/6)
- Error "Unable to extract initial state" on yt-dlp [#4](https://github.com/g-nogueira/sonarr_ytdlp/issues/4)
- Message "title did not match pattern" on most of the episodes from Crunchyroll [#2](https://github.com/g-nogueira/sonarr_ytdlp/issues/2)
---

![Docker Build](https://img.shields.io/docker/cloud/automated/whatdaybob/sonarr_youtubedl?style=flat-square)
![Docker Pulls](https://img.shields.io/docker/pulls/whatdaybob/sonarr_youtubedl?style=flat-square)
![Docker Stars](https://img.shields.io/docker/stars/whatdaybob/sonarr_youtubedl?style=flat-square)
[![Docker Hub](https://img.shields.io/badge/Open%20On-DockerHub-blue)](https://hub.docker.com/r/whatdaybob/sonarr_youtubedl)

[whatdaybob/sonarr_youtubedl](https://github.com/whatdaybob/Custom_Docker_Images/tree/master/sonarr_youtubedl) is a [Sonarr](https://sonarr.tv/) companion script to allow the automatic downloading of web series normally not available for Sonarr to search for. Using [YT-DLP](https://github.com/yt-dlp/yt-dlp) (a youtube-dl fork with added features) it allows you to download your webseries from the list of [supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Features

* Downloading **Web Series** using online sources normally unavailable to Sonarr
* Ability to specify the downloaded video format globally or per series
* Downloads new episodes automatically once available
* Imports directly to Sonarr and it can then update your plex as and example
* Allows setting time offsets to handle prerelease series
* Can pass cookies.txt to handle site logins

## How do I use it

Firstly you need a series that is available online in the supported sites that YouTube-DL can grab from.
Secondly you need to add this to Sonarr and monitor the episodes that you want.
Thirdly edit your config.yml accordingly so that this knows where your Sonarr is, which series you are after and where to grab it from.
Lastly be aware that this requires the TVDB to match exactly what the episodes titles are in the scan, generally this is ok but as its an openly editable site sometime there can be differences.

## Supported Architectures

The architectures supported by this image are:

| Architecture | Tag |
| :----: | --- |
| x86-64 | latest |
| x86-64 | dev |

## Version Tags

| Tag | Description |
| :----: | --- |
| latest | Current release code |
| dev | Pre-release code for testing issues |

## Great how do I get started

Obviously its a docker image so you need docker, if you don't know what that is you need to look into that first.

### docker

```bash
docker create \
  --name=sonarr_youtubedl \
  -v /path/to/data:/config \
  -v /path/to/sonarrmedia:/sonarr_root \
  -v /path/to/logs:/logs \
  --restart unless-stopped \
  whatdaybob/sonarr_youtubedl
```

### docker-compose

```yaml
---
version: '3.4'
services:
  sonarr_youtubedl:
    image: whatdaybob/sonarr_youtubedl
    container_name: sonarr_youtubedl
    volumes:
      - /path/to/data:/config
      - /path/to/sonarrmedia:/sonarr_root
      - /path/to/logs:/logs
```

### Docker volumes

| Parameter | Function |
| :----: | --- |
| `-v /config` | sonarr_youtubedl configs |
| `-v /sonarr_root` | Root library location from Sonarr container |
| `-v /logs` | log location |

**Clarification on sonarr_root**

A couple of people are not sure what is meant by the sonarr root. As this downloads directly to where you media is stored I mean the root folder where sonarr will place the files. So in sonarr you have your files moving to `/mnt/sda1/media/tv/Smarter Every Day/` as an example, in sonarr you will see that it saves this series to `/tv/Smarter Every Day/` meaning the sonarr root is `/mnt/sda1/media/` as this is the root folder sonarr is working from.

## Configuration file

On first run the docker will create a template file in the config folder. Example [config.yml.template](./app/config.yml.template)

Copy the `config.yml.template` to a new file called `config.yml` and edit accordingly.

If I helped in anyway and you would like to help me, consider donating a lovely beverage with the below.

<!-- markdownlint-disable MD033 -->
<a href="https://www.buymeacoffee.com/whatdaybob" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/lato-black.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>
<!-- markdownlint-enable MD033 -->
