# OpenCTI Docker deployment

## Documentation

You can find the detailed documentation about the Docker installation in the [OpenCTI documentation space](https://docs.opencti.io/latest/deployment/installation/#using-docker).

## XTM One

This stack bundles [XTM One](https://filigran.io), Filigran's AI-powered assistant, alongside OpenCTI. The following services are started by default:

| Service | Description |
|---------|-------------|
| `xtm-one` | XTM One platform (web UI + API, exposed on `XTM_ONE_PORT`) |
| `xtm-one-worker` | XTM One background worker |
| `pgsql-xtm-one` | Dedicated PostgreSQL + `pgvector` instance for XTM One |

XTM One reuses the shared `redis` and `minio` services and connects to OpenCTI internally via `OPENCTI_API_URL`. OpenCTI registers itself with XTM One using `PLATFORM_REGISTRATION_TOKEN` — this shared secret **must be identical** across every platform connected to the same XTM One instance.

All XTM One configuration (admin credentials, dedicated Postgres credentials, S3 bucket, license, log settings) lives in the `XTM ONE` section of [.env.sample](.env.sample). Once the stack is healthy, XTM One is available on `http://localhost:${XTM_ONE_PORT}` (default `8090`).

### Public and internal URLs

Each product has two URLs in this stack:

- the **public URL** you open in your browser, built from `OPENCTI_EXTERNAL_SCHEME` / `OPENCTI_HOST` / `OPENCTI_PORT` and `XTM_ONE_EXTERNAL_SCHEME` / `XTM_ONE_HOST` / `XTM_ONE_PORT` (set the scheme to `https` together with the host when you publish them over TLS). It is also the identity each product signs its requests to the other with, so it is set on both XTM One containers (`BASE_URL`) and on OpenCTI (`APP__BASE_URL`);
- the **internal URL** the containers reach each other on: `http://opencti:8080` (`OPENCTI_API_URL` on XTM One) and `http://xtm-one:4000` (`XTM__XTM_ONE_URL` on OpenCTI).

The public host name does not need to resolve inside the containers: XTM One fetches OpenCTI's signing keys on the internal URL, and OpenCTI reads XTM One's public identity from `http://xtm-one:4000/xtm/auth/metadata`. This needs XTM One and OpenCTI releases that include [XTM-One-Platform/xtm-one#4883](https://github.com/XTM-One-Platform/xtm-one/pull/4883) and [OpenCTI-Platform/opencti#18585](https://github.com/OpenCTI-Platform/opencti/pull/18585).

If OpenCTI registers with XTM One but every assistant action on OpenCTI data fails with `401`, the XTM One logs (`XTM JWT rejected`) and the OpenCTI logs (`JWT issuer is not trusted`) name the URL that did not match.

## Community

### Status & bugs

Currently OpenCTI is under heavy development, if you wish to report bugs or ask for new features, you can directly use the [Github issues module](https://github.com/OpenCTI-Platform/opencti/issues).

### Discussion

If you need support or you wish to engage a discussion about the OpenCTI platform, feel free to join us on our [Slack channel](https://community.filigran.io). You can also send us an email to contact@opencti.io.

## About

OpenCTI is a product designed and developed by the company [Filigran](https://filigran.io).

<a href="https://filigran.io" alt="Filigran"><img src="https://github.com/OpenCTI-Platform/opencti/raw/master/.github/img/logo_filigran.png" width="300" /></a>