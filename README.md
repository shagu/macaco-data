# macaco-data

A [python script](build-data.py) and [GitHub workflow](.github/workflows/nightly.yml) to automatically gather and process latest [MTGJSON](https://mtgjson.com/) data. [Macaco](https://github.com/shagu/macaco) is written in node.js and it seems to be nearly impossible to process JSON files larger than 1GB in a meaningful way. However, [MTGJSON](https://mtgjson.com/) data tends to be quite large, so what this job does, is fetching all data and combining/shrinking it into a smaller JSON in order to make it possible for node.js to load it without troubles.

Latest builds are always attached to the [Nightly Release](https://github.com/shagu/macaco-data/releases/tag/nightly).
