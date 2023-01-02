# Web-Link

The `link` spider create the linkgraph for a set of urls.

To run it:
`$ scrapy crawl link -a urls='https://example.com'`

To skip some hostname/domain, provide the argument `skips`.

The vertex of the graph are either hostname or domain, use the argument `data`
 to choose.

## License

Licensed under

 * MIT license
   ([LICENSE](LICENSE) or http://opensource.org/licenses/MIT)
