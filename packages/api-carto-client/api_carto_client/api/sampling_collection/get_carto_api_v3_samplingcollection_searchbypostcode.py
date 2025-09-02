import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_collection_result import SamplingCollectionResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    post_code: str,
    hide_private_collects: Union[Unset, bool] = UNSET,
    hide_non_publiable_collects: Union[Unset, bool] = UNSET,
    max_date: Union[Unset, datetime.datetime] = UNSET,
    min_date: Union[Unset, datetime.datetime] = UNSET,
    locations_only: Union[Unset, bool] = UNSET,
    give_blood: Union[Unset, bool] = UNSET,
    give_plasma: Union[Unset, bool] = UNSET,
    give_platelets: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["PostCode"] = post_code

    params["HidePrivateCollects"] = hide_private_collects

    params["HideNonPubliableCollects"] = hide_non_publiable_collects

    json_max_date: Union[Unset, str] = UNSET
    if not isinstance(max_date, Unset):
        json_max_date = max_date.isoformat()
    params["MaxDate"] = json_max_date

    json_min_date: Union[Unset, str] = UNSET
    if not isinstance(min_date, Unset):
        json_min_date = min_date.isoformat()
    params["MinDate"] = json_min_date

    params["LocationsOnly"] = locations_only

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
        "url": "/carto-api/v3/samplingcollection/searchbypostcode",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SamplingCollectionResult]]:
    if response.status_code == 200:
        response_200 = SamplingCollectionResult.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, SamplingCollectionResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    post_code: str,
    hide_private_collects: Union[Unset, bool] = UNSET,
    hide_non_publiable_collects: Union[Unset, bool] = UNSET,
    max_date: Union[Unset, datetime.datetime] = UNSET,
    min_date: Union[Unset, datetime.datetime] = UNSET,
    locations_only: Union[Unset, bool] = UNSET,
    give_blood: Union[Unset, bool] = UNSET,
    give_plasma: Union[Unset, bool] = UNSET,
    give_platelets: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Union[Any, SamplingCollectionResult]]:
    """Retourne une liste de collectes situés dans un code postal.

    Args:
        post_code (str):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        locations_only (Union[Unset, bool]):
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
        Response[Union[Any, SamplingCollectionResult]]
    """

    kwargs = _get_kwargs(
        post_code=post_code,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        locations_only=locations_only,
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
    client: Union[AuthenticatedClient, Client],
    post_code: str,
    hide_private_collects: Union[Unset, bool] = UNSET,
    hide_non_publiable_collects: Union[Unset, bool] = UNSET,
    max_date: Union[Unset, datetime.datetime] = UNSET,
    min_date: Union[Unset, datetime.datetime] = UNSET,
    locations_only: Union[Unset, bool] = UNSET,
    give_blood: Union[Unset, bool] = UNSET,
    give_plasma: Union[Unset, bool] = UNSET,
    give_platelets: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Optional[Union[Any, SamplingCollectionResult]]:
    """Retourne une liste de collectes situés dans un code postal.

    Args:
        post_code (str):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        locations_only (Union[Unset, bool]):
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
        Union[Any, SamplingCollectionResult]
    """

    return sync_detailed(
        client=client,
        post_code=post_code,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        locations_only=locations_only,
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
    client: Union[AuthenticatedClient, Client],
    post_code: str,
    hide_private_collects: Union[Unset, bool] = UNSET,
    hide_non_publiable_collects: Union[Unset, bool] = UNSET,
    max_date: Union[Unset, datetime.datetime] = UNSET,
    min_date: Union[Unset, datetime.datetime] = UNSET,
    locations_only: Union[Unset, bool] = UNSET,
    give_blood: Union[Unset, bool] = UNSET,
    give_plasma: Union[Unset, bool] = UNSET,
    give_platelets: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Union[Any, SamplingCollectionResult]]:
    """Retourne une liste de collectes situés dans un code postal.

    Args:
        post_code (str):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        locations_only (Union[Unset, bool]):
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
        Response[Union[Any, SamplingCollectionResult]]
    """

    kwargs = _get_kwargs(
        post_code=post_code,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        locations_only=locations_only,
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
    client: Union[AuthenticatedClient, Client],
    post_code: str,
    hide_private_collects: Union[Unset, bool] = UNSET,
    hide_non_publiable_collects: Union[Unset, bool] = UNSET,
    max_date: Union[Unset, datetime.datetime] = UNSET,
    min_date: Union[Unset, datetime.datetime] = UNSET,
    locations_only: Union[Unset, bool] = UNSET,
    give_blood: Union[Unset, bool] = UNSET,
    give_plasma: Union[Unset, bool] = UNSET,
    give_platelets: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Optional[Union[Any, SamplingCollectionResult]]:
    """Retourne une liste de collectes situés dans un code postal.

    Args:
        post_code (str):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        locations_only (Union[Unset, bool]):
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
        Union[Any, SamplingCollectionResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            post_code=post_code,
            hide_private_collects=hide_private_collects,
            hide_non_publiable_collects=hide_non_publiable_collects,
            max_date=max_date,
            min_date=min_date,
            locations_only=locations_only,
            give_blood=give_blood,
            give_plasma=give_plasma,
            give_platelets=give_platelets,
            page=page,
            limit=limit,
            user_latitude=user_latitude,
            user_longitude=user_longitude,
        )
    ).parsed
