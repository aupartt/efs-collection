from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_location_result import SamplingLocationResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    post_code: str,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["PostCode"] = post_code

    params["GiveBlood"] = give_blood

    params["GivePlasma"] = give_plasma

    params["GivePlatelets"] = give_platelets

    params["Page"] = page

    params["Limit"] = limit

    params["UserLatitude"] = user_latitude

    params["UserLongitude"] = user_longitude

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/carto-api/v3/samplinglocation/searchbypostcode",
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
    post_code: str,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Any | SamplingLocationResult]:
    """Retourne une liste de lieux de prélévement situés dans un code postal.

    Args:
        post_code (str):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        user_latitude (float):
        user_longitude (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingLocationResult]]
    """

    kwargs = _get_kwargs(
        post_code=post_code,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
        page=page,
        limit=limit,
        user_latitude=user_latitude,
        user_longitude=user_longitude,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    post_code: str,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Any | SamplingLocationResult | None:
    """Retourne une liste de lieux de prélévement situés dans un code postal.

    Args:
        post_code (str):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        user_latitude (float):
        user_longitude (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingLocationResult]
    """

    return sync_detailed(
        client=client,
        post_code=post_code,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
        page=page,
        limit=limit,
        user_latitude=user_latitude,
        user_longitude=user_longitude,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    post_code: str,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Any | SamplingLocationResult]:
    """Retourne une liste de lieux de prélévement situés dans un code postal.

    Args:
        post_code (str):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        user_latitude (float):
        user_longitude (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingLocationResult]]
    """

    kwargs = _get_kwargs(
        post_code=post_code,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
        page=page,
        limit=limit,
        user_latitude=user_latitude,
        user_longitude=user_longitude,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    post_code: str,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Any | SamplingLocationResult | None:
    """Retourne une liste de lieux de prélévement situés dans un code postal.

    Args:
        post_code (str):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        user_latitude (float):
        user_longitude (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingLocationResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            post_code=post_code,
            give_blood=give_blood,
            give_plasma=give_plasma,
            give_platelets=give_platelets,
            page=page,
            limit=limit,
            user_latitude=user_latitude,
            user_longitude=user_longitude,
        )
    ).parsed
