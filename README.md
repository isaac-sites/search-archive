# Isaac Koi Archive Search

GitHub Pages shell for the Isaac Koi archive search interface.

The working search package, generated search data, and public PDFs are currently
served from `https://files.afu.se/Downloads/search/`. This repository hosts the
Isaac Koi-branded entry point and CORS diagnostic page while the AFU-hosted data
remains on the AFU file server.

## Live URLs

- GitHub Pages: <https://isaac-sites.github.io/search-archive/>
- Intended custom domain: <https://search-archive.isaackoi.com/>
- AFU-hosted search package: <https://files.afu.se/Downloads/search/>

## CORS note

The shell embeds the AFU-hosted search interface in an iframe because direct
JavaScript reads from `files.afu.se` require CORS headers that are not currently
being emitted by the AFU server.
