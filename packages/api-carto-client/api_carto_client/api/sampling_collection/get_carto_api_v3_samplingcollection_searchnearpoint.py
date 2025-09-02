import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_collection_result import SamplingCollectionResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    center_latitude: float,
    center_longitude: float,
    diameter_latitude: float,
    diameter_longitude: float,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    locations_only: Unset | bool = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["CenterLatitude"] = center_latitude

    params["CenterLongitude"] = center_longitude

    params["DiameterLatitude"] = diameter_latitude

    params["DiameterLongitude"] = diameter_longitude

    params["HidePrivateCollects"] = hide_private_collects

    params["HideNonPubliableCollects"] = hide_non_publiable_collects

    json_max_date: Unset | str = UNSET
    if not isinstance(max_date, Unset):
        json_max_date = max_date.isoformat()
    params["MaxDate"] = json_max_date

    json_min_date: Unset | str = UNSET
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
        "url": "/carto-api/v3/samplingcollection/searchnearpoint",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SamplingCollectionResult | None:
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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | SamplingCollectionResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    diameter_latitude: float,
    diameter_longitude: float,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    locations_only: Unset | bool = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Any | SamplingCollectionResult]:
    """Retourne une liste de collectes autour d'un point.

    Args:
        center_latitude (float):
        center_longitude (float):
        diameter_latitude (float):
        diameter_longitude (float):
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
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        diameter_latitude=diameter_latitude,
        diameter_longitude=diameter_longitude,
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
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    diameter_latitude: float,
    diameter_longitude: float,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    locations_only: Unset | bool = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Any | SamplingCollectionResult | None:
    """Retourne une liste de collectes autour d'un point.

    Args:
        center_latitude (float):
        center_longitude (float):
        diameter_latitude (float):
        diameter_longitude (float):
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
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        diameter_latitude=diameter_latitude,
        diameter_longitude=diameter_longitude,
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
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    diameter_latitude: float,
    diameter_longitude: float,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    locations_only: Unset | bool = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Response[Any | SamplingCollectionResult]:
    """Retourne une liste de collectes autour d'un point.

    Args:
        center_latitude (float):
        center_longitude (float):
        diameter_latitude (float):
        diameter_longitude (float):
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
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        diameter_latitude=diameter_latitude,
        diameter_longitude=diameter_longitude,
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
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    diameter_latitude: float,
    diameter_longitude: float,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    locations_only: Unset | bool = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
    page: Unset | int = UNSET,
    limit: Unset | int = UNSET,
    user_latitude: float,
    user_longitude: float,
) -> Any | SamplingCollectionResult | None:
    """Retourne une liste de collectes autour d'un point.

    Args:
        center_latitude (float):
        center_longitude (float):
        diameter_latitude (float):
        diameter_longitude (float):
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
            center_latitude=center_latitude,
            center_longitude=center_longitude,
            diameter_latitude=diameter_latitude,
            diameter_longitude=diameter_longitude,
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
