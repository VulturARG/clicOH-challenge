from __future__ import annotations

import json
import requests

from typing import Optional, Dict, List, Tuple

from domain.gateway import ServerConfiguration
from domain.gateway.exceptions import GatewayUnauthorized, GatewayEndpointNotFound
from domain.gateway.gateway import Gateway


class DollarURLGateway(Gateway):
    """
    Gateway class make requests.

    This class automates routing and authentication in the Dollar server handling API.
    """

    def __init__(
        self, server_configuration: ServerConfiguration,
    ):
        self._server_configuration = server_configuration

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
        """
        Make post request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """

        response = requests.post(
            self._server_configuration.api_root_url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=self._auth_in_server(),
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )
        return self._verify_response(response)

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
        """
        Make get request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """

        response = requests.get(
            self._server_configuration.api_root_url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=self._auth_in_server(),
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )
        return self._verify_response(response)

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
        """
        Make delete request.

        A more complete explanation of these parameters can be found in the request, class session,
        request method library. Line 457 at
        https://github.com/psf/requests/blob/main/requests/sessions.py.
        """

        response = requests.delete(
            self._server_configuration.api_root_url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=self._auth_in_server(),
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )
        return self._verify_response(response)

    def _auth_in_server(self) -> Tuple[str, str]:
        return (
            self._server_configuration.user,
            self._server_configuration.password,
        )

    def _verify_response(
        self, response: requests.models.Response
    ) -> requests.models.Response:
        """Verify response status code.

        Raise an exception if the response status code is 401 or 404.
        """
        if response.status_code == 401:
            raise GatewayUnauthorized()
        if response.status_code == 404:
            raise GatewayEndpointNotFound()

        return response
