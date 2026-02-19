# Home Assistant Integration - Météo France

This an override of an official [Home Assistant](https://www.home-assistant.io/) integration.\
The `meteo_france` integration allows you fetch data from [Météo France Open Api](https://portail-api.meteofrance.fr/web/).

There is currently support for the following device types within Home Assistant:

*To complete here* 

## Usage

### Initial setup

*To complete here*

### Notes

*To complete here*

## Projects Scripts

### Start

To start Home Assistant instance with the integration, run the following command :\
`uv run homeassistant -c .homeassistant --debug --open-ui`

### Build

To build the project run the following command :\
`uv run ./scripts/build.py`

### Release

To release a new version of the project (Bump project version, update manifest version and create a git tag), run the following command :\
`uv run ./scripts/release.py <version>` where `version` is the version number with semantic versioning.
