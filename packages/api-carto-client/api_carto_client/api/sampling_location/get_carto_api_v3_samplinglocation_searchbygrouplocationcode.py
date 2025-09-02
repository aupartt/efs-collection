from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_location_result import SamplingLocationResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    group_code: str,
    sampling_location_code: Unset | str = UNSET,
    region_code: Unset | str = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["GroupCode"] = group_code

    params["SamplingLocationCode"] = sampling_location_code

    params["RegionCode"] = region_code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/carto-api/v3/samplinglocation/searchbygrouplocationcode",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SamplingLocationResult | None:
    if response.status_code == 200:
        response_200 = SamplingLocationResult.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | SamplingLocationResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    group_code: str,
    sampling_location_code: Unset | str = UNSET,
    region_code: Unset | str = UNSET,
) -> Response[Any | SamplingLocationResult]:
    """Retourne le lieu de prélévement en fonction du GroupCode et samplingLocationCode.

    Args:
        group_code (str):
        sampling_location_code (Union[Unset, str]):
        region_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingLocationResult]]
    """

    kwargs = _get_kwargs(
        group_code=group_code,
        sampling_location_code=sampling_location_code,
        region_code=region_code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    group_code: str,
    sampling_location_code: Unset | str = UNSET,
    region_code: Unset | str = UNSET,
) -> Any | SamplingLocationResult | None:
    """Retourne le lieu de prélévement en fonction du GroupCode et samplingLocationCode.

    Args:
        group_code (str):
        sampling_location_code (Union[Unset, str]):
        region_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingLocationResult]
    """

    return sync_detailed(
        client=client,
        group_code=group_code,
        sampling_location_code=sampling_location_code,
        region_code=region_code,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    group_code: str,
    sampling_location_code: Unset | str = UNSET,
    region_code: Unset | str = UNSET,
) -> Response[Any | SamplingLocationResult]:
    """Retourne le lieu de prélévement en fonction du GroupCode et samplingLocationCode.

    Args:
        group_code (str):
        sampling_location_code (Union[Unset, str]):
        region_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingLocationResult]]
    """

    kwargs = _get_kwargs(
        group_code=group_code,
        sampling_location_code=sampling_location_code,
        region_code=region_code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    group_code: str,
    sampling_location_code: Unset | str = UNSET,
    region_code: Unset | str = UNSET,
) -> Any | SamplingLocationResult | None:
    """Retourne le lieu de prélévement en fonction du GroupCode et samplingLocationCode.

    Args:
        group_code (str):
        sampling_location_code (Union[Unset, str]):
        region_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingLocationResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            group_code=group_code,
            sampling_location_code=sampling_location_code,
            region_code=region_code,
        )
    ).parsed
