from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

import requests
import json


class Gateway(ABC):
    """
    Gateway class to make requests.

    Use this class to abstract the authentication from requests and basic setups for communication
    as the server address.
    """

    @abstractmethod
    def post(
        self,
        relative_path: Optional[str] = None,
        params: Optional[Dict | bytes] = None,
        data: Optional[Dict | List[Tuple] | bytes | object] = None,
        headers: Optional[Dict | str] = None,
        cookies: Optional[Dict | object] = None,
        files: Optional[Dict | object] = None,
        auth: Optional[Tuple | str] = None,
        timeout: Optional[int | Tuple[int, int]] = None,
        allow_redirects: Optional[bool] = True,
        proxies: Optional[Dict | str] = None,
        hooks: Optional = None,
        stream: Optional = None,
        verify: Optional[bool | str] = None,
        cert: Optional[str | Tuple[str, str]] = None,
        json: Optional[json] = None,
    ) -> requests.models.Response:
        """Make post request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """

    @abstractmethod
    def get(
        self,
        relative_path: Optional[str] = None,
        params: Optional[Dict | bytes] = None,
        data: Optional[Dict | List[Tuple] | bytes | object] = None,
        headers: Optional[Dict | str] = None,
        cookies: Optional[Dict | object] = None,
        files: Optional[Dict | object] = None,
        auth: Optional[Tuple | str] = None,
        timeout: Optional[int | Tuple[int, int]] = None,
        allow_redirects: Optional[bool] = True,
        proxies: Optional[Dict | str] = None,
        hooks: Optional = None,
        stream: Optional = None,
        verify: Optional[bool | str] = None,
        cert: Optional[str | Tuple[str, str]] = None,
        json: Optional[json] = None,
    ) -> requests.models.Response:
        """Make get request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """

    @abstractmethod
    def delete(
        self,
        relative_path: Optional[str] = None,
        params: Optional[Dict | bytes] = None,
        data: Optional[Dict | List[Tuple] | bytes | object] = None,
        headers: Optional[Dict | str] = None,
        cookies: Optional[Dict | object] = None,
        files: Optional[Dict | object] = None,
        auth: Optional[Tuple | str] = None,
        timeout: Optional[int | Tuple[int, int]] = None,
        allow_redirects: Optional[bool] = True,
        proxies: Optional[Dict | str] = None,
        hooks: Optional = None,
        stream: Optional = None,
        verify: Optional[bool | str] = None,
        cert: Optional[str | Tuple[str, str]] = None,
        json: Optional[json] = None,
    ) -> requests.models.Response:
        """Make delete request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """
