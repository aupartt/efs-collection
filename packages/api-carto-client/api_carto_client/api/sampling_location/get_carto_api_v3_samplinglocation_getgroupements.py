from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_group_entity import SamplingGroupEntity
from ...types import UNSET, Response


def _get_kwargs(
    *,
    region_code: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["RegionCode"] = region_code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/carto-api/v3/samplinglocation/getgroupements",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list["SamplingGroupEntity"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SamplingGroupEntity.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list["SamplingGroupEntity"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    region_code: str,
) -> Response[Any | list["SamplingGroupEntity"]]:
    """Retourne la liste des régions

    Args:
        region_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['SamplingGroupEntity']]]
    """

    kwargs = _get_kwargs(
        region_code=region_code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    region_code: str,
) -> Any | list["SamplingGroupEntity"] | None:
    """Retourne la liste des régions

    Args:
        region_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['SamplingGroupEntity']]
    """

    return sync_detailed(
        client=client,
        region_code=region_code,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    region_code: str,
) -> Response[Any | list["SamplingGroupEntity"]]:
    """Retourne la liste des régions

    Args:
        region_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['SamplingGroupEntity']]]
    """

    kwargs = _get_kwargs(
        region_code=region_code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    region_code: str,
) -> Any | list["SamplingGroupEntity"] | None:
    """Retourne la liste des régions

    Args:
        region_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['SamplingGroupEntity']]
    """

    return (
        await asyncio_detailed(
            client=client,
            region_code=region_code,
        )
    ).parsed
