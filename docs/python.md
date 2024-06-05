- requests

    ```python
    # python -m pip install requests-mock
    import requests
    import json

    # Config
    url = os.environ.get("T_API_URL", "https://sampletestfiles.com/wp-content/uploads/2024/04/file-example_PDF_100kb.pdf")
    headers: dict[str, str] = json.loads(os.environ.get("T_API_HEADERS", '{"Cache-Control": "no-cache"}'))

    def download_file(url, headers, filename: str = url.split("/")[-1]):
        """
        Using the NewsAPI, get results.
        """
        days_str = (datetime.now() - timedelta(days=days_since)).strftime('%Y-%m-%d')

        headers = {"x-api-key": config.NEWS_API_KEY}
        url = (f'https://newsapi.org/v2/everything?'
            f'q={query}&'
            f'from={days_str}&'
            f'sortBy={sort_by}&'
            f'apiKey={config.NEWS_API_KEY}')

        logger.debug("New news query URL: %s, using headers: %s.", url, headers)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")  # pylint: disable=logging-fstring-interpolation
            raise NewsAPIException(f"Request failed: {e}") from e
        except ValueError as e:
            logger.error(f"JSON decoding failed: {e}")  # pylint: disable=logging-fstring-interpolation
            raise NewsAPIException(f"JSON decoding failed: {e}") from e
        except KeyError as e:
            logger.error(f"Unexpected response format: missing key {e}")  # pylint: disable=logging-fstring-interpolation
            raise NewsAPIException(f"Unexpected response format: missing key {e}") from e

        logger.debug(f"days_since {days_since} result_count {data['totalResults']} search term {query}")  # pylint: disable=logging-fstring-interpolation

        with open(filename, 'wb') as file:
            file.write(response.content)

        return data

    download_file(url, headers)
    ```

    - httpx synchronous

    ```python
    import httpx
    import json

    # Config
    url = os.environ.get("T_API_URL", "https://sampletestfiles.com/wp-content/uploads/2024/04/file-example_PDF_100kb.pdf")
    headers: dict[str, str] = json.loads(os.environ.get("T_API_HEADERS", '{"Cache-Control": "no-cache"}'))

    def download_file(url, headers, filename: str = url.split("/")[-1]):
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            with open(filename, 'wb') as file:
                file.write(response.content)

    download_file(url, headers)
    ```

    - httpx async

    ```python
    import httpx
    import asyncio
    import json
    # This cannot be tested from jupyter as asyncio cannot be called from a running event loop.

    # Config
    url = os.environ.get("T_API_URL", "https://sampletestfiles.com/wp-content/uploads/2024/04/file-example_PDF_100kb.pdf")
    headers: dict[str, str] = json.loads(os.environ.get("T_API_HEADERS", '{"Cache-Control": "no-cache"}'))

    async def download_file(url, headers, filename: str = url.split("/")[-1]) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            with open(filename, 'wb') as file:
                file.write(response.content)

    asyncio.run(download_file(url, headers))
    ```
