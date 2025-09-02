import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sampling_square_entity import SamplingSquareEntity
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    center_latitude: float,
    center_longitude: float,
    city: Unset | str = UNSET,
    post_code: Unset | str = UNSET,
    map_width: float,
    map_height: float,
    padding: Unset | float = UNSET,
    padding_one_res: Unset | float = UNSET,
    limit: Unset | int = UNSET,
    distance_limit: Unset | float = UNSET,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["CenterLatitude"] = center_latitude

    params["CenterLongitude"] = center_longitude

    params["City"] = city

    params["PostCode"] = post_code

    params["MapWidth"] = map_width

    params["MapHeight"] = map_height

    params["Padding"] = padding

    params["PaddingOneRes"] = padding_one_res

    params["Limit"] = limit

    params["DistanceLimit"] = distance_limit

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

    params["GiveBlood"] = give_blood

    params["GivePlasma"] = give_plasma

    params["GivePlatelets"] = give_platelets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/carto-api/v3/samplingcollection/getmapsquare",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SamplingSquareEntity | None:
    if response.status_code == 200:
        response_200 = SamplingSquareEntity.from_dict(response.json())

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
) -> Response[Any | SamplingSquareEntity]:
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
    city: Unset | str = UNSET,
    post_code: Unset | str = UNSET,
    map_width: float,
    map_height: float,
    padding: Unset | float = UNSET,
    padding_one_res: Unset | float = UNSET,
    limit: Unset | int = UNSET,
    distance_limit: Unset | float = UNSET,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
) -> Response[Any | SamplingSquareEntity]:
    """Retourne les coordonées de zoom de la carte incluant les collectes de la recherche.

    Args:
        center_latitude (float):
        center_longitude (float):
        city (Union[Unset, str]):
        post_code (Union[Unset, str]):
        map_width (float):
        map_height (float):
        padding (Union[Unset, float]):
        padding_one_res (Union[Unset, float]):
        limit (Union[Unset, int]):
        distance_limit (Union[Unset, float]):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingSquareEntity]]
    """

    kwargs = _get_kwargs(
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        city=city,
        post_code=post_code,
        map_width=map_width,
        map_height=map_height,
        padding=padding,
        padding_one_res=padding_one_res,
        limit=limit,
        distance_limit=distance_limit,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
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
    city: Unset | str = UNSET,
    post_code: Unset | str = UNSET,
    map_width: float,
    map_height: float,
    padding: Unset | float = UNSET,
    padding_one_res: Unset | float = UNSET,
    limit: Unset | int = UNSET,
    distance_limit: Unset | float = UNSET,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
) -> Any | SamplingSquareEntity | None:
    """Retourne les coordonées de zoom de la carte incluant les collectes de la recherche.

    Args:
        center_latitude (float):
        center_longitude (float):
        city (Union[Unset, str]):
        post_code (Union[Unset, str]):
        map_width (float):
        map_height (float):
        padding (Union[Unset, float]):
        padding_one_res (Union[Unset, float]):
        limit (Union[Unset, int]):
        distance_limit (Union[Unset, float]):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingSquareEntity]
    """

    return sync_detailed(
        client=client,
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        city=city,
        post_code=post_code,
        map_width=map_width,
        map_height=map_height,
        padding=padding,
        padding_one_res=padding_one_res,
        limit=limit,
        distance_limit=distance_limit,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    city: Unset | str = UNSET,
    post_code: Unset | str = UNSET,
    map_width: float,
    map_height: float,
    padding: Unset | float = UNSET,
    padding_one_res: Unset | float = UNSET,
    limit: Unset | int = UNSET,
    distance_limit: Unset | float = UNSET,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
) -> Response[Any | SamplingSquareEntity]:
    """Retourne les coordonées de zoom de la carte incluant les collectes de la recherche.

    Args:
        center_latitude (float):
        center_longitude (float):
        city (Union[Unset, str]):
        post_code (Union[Unset, str]):
        map_width (float):
        map_height (float):
        padding (Union[Unset, float]):
        padding_one_res (Union[Unset, float]):
        limit (Union[Unset, int]):
        distance_limit (Union[Unset, float]):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SamplingSquareEntity]]
    """

    kwargs = _get_kwargs(
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        city=city,
        post_code=post_code,
        map_width=map_width,
        map_height=map_height,
        padding=padding,
        padding_one_res=padding_one_res,
        limit=limit,
        distance_limit=distance_limit,
        hide_private_collects=hide_private_collects,
        hide_non_publiable_collects=hide_non_publiable_collects,
        max_date=max_date,
        min_date=min_date,
        give_blood=give_blood,
        give_plasma=give_plasma,
        give_platelets=give_platelets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    center_latitude: float,
    center_longitude: float,
    city: Unset | str = UNSET,
    post_code: Unset | str = UNSET,
    map_width: float,
    map_height: float,
    padding: Unset | float = UNSET,
    padding_one_res: Unset | float = UNSET,
    limit: Unset | int = UNSET,
    distance_limit: Unset | float = UNSET,
    hide_private_collects: Unset | bool = UNSET,
    hide_non_publiable_collects: Unset | bool = UNSET,
    max_date: Unset | datetime.datetime = UNSET,
    min_date: Unset | datetime.datetime = UNSET,
    give_blood: Unset | bool = UNSET,
    give_plasma: Unset | bool = UNSET,
    give_platelets: Unset | bool = UNSET,
) -> Any | SamplingSquareEntity | None:
    """Retourne les coordonées de zoom de la carte incluant les collectes de la recherche.

    Args:
        center_latitude (float):
        center_longitude (float):
        city (Union[Unset, str]):
        post_code (Union[Unset, str]):
        map_width (float):
        map_height (float):
        padding (Union[Unset, float]):
        padding_one_res (Union[Unset, float]):
        limit (Union[Unset, int]):
        distance_limit (Union[Unset, float]):
        hide_private_collects (Union[Unset, bool]):
        hide_non_publiable_collects (Union[Unset, bool]):
        max_date (Union[Unset, datetime.datetime]):
        min_date (Union[Unset, datetime.datetime]):
        give_blood (Union[Unset, bool]):
        give_plasma (Union[Unset, bool]):
        give_platelets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SamplingSquareEntity]
    """

    return (
        await asyncio_detailed(
            client=client,
            center_latitude=center_latitude,
            center_longitude=center_longitude,
            city=city,
            post_code=post_code,
            map_width=map_width,
            map_height=map_height,
            padding=padding,
            padding_one_res=padding_one_res,
            limit=limit,
            distance_limit=distance_limit,
            hide_private_collects=hide_private_collects,
            hide_non_publiable_collects=hide_non_publiable_collects,
            max_date=max_date,
            min_date=min_date,
            give_blood=give_blood,
            give_plasma=give_plasma,
            give_platelets=give_platelets,
        )
    ).parsed
