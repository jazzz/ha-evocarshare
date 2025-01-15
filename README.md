

<img src="docs/assets/evo-thumbnail.png" alt="Alt Text" height="200" style="display: block; margin: 0 auto" >

# Evo Car Share

![Status](https://img.shields.io/badge/Project_status-Beta-yellow)

An un-offical integration which brings data from the EvoCarShare service into Homeassistant.


![Example Usage](docs/assets/evo_baricon.png)
Here is a minimalist example of the data shown as a `chip` where you can easily see, how many evos are nearby.
## Installation

✨ Install via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jazzz&repository=ha-evocarshare)


## Configuration 

The `evocarshare` integration can be configured once per `Zone`.


| Name                             | Type                   | Requirement  | Description                                                                                                                                                     | Default             |
|----------------------------------|------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| `Zone`                           | Zone                 | **Required** | which location to use     | Home 
| `Search Radius`                  | number                 | **Required** | distance from the selected `Zone` which should be considered close    |  

The integration does not use the radius configured in the `Zone` as this can differ significantly from how far you are willing to walk for an evo.  

## Entities

The following entities are available for display or use automations, once a configuration has been completed. Multiple configurations results in a set of entities for each configured `Zone`

| Name          | Example | Type | Description |
|---------------|------|---|----|
| `<zone>_evo_count` | `home_evo_count` | number | Total count of vehicles within the configured range of the Zone.
| `<zone>_evo_dist`  | `home_evo_dist`  | number | Number of meters to the closest evo, regardless of whether it is inside the search radius or not.


## Questions?
Feel free to open a Github issue if you have found something that isn't working the way that you'd like.