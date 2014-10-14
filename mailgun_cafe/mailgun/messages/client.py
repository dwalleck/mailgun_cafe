"""
Copyright 2014 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64

from cafe.engine.http.client import AutoMarshallingHTTPClient

from mailgun_cafe.mailgun.messages.models.requests import \
    ExplicitMessageRequest
from mailgun_cafe.mailgun.messages.models.responses import \
    MessageResponse


class MessagesClient(AutoMarshallingHTTPClient):

    def __init__(self, base_url, username, password):
        super(MessagesClient, self).__init__('json', 'json')
        credentials = '{username}:{password}'.format(
            username=username, password=password)
        self.default_headers['Authorization'] = 'Basic {creds}'.format(
            creds=base64.b64encode(credentials))
        self.default_headers['Content-Type'] = 'application/json'
        self.default_headers['Accept'] = 'application/json'
        self.base_url = base_url

    def send_message(
            self, from_=None, to=None, cc=None, bcc=None,
            subject=None, text=None, html=None, attachment=None, inline=None,
            tag=None, campaign=None, dkim=None, delivery_time=None,
            test_mode=None, tracking=None, tracking_clicks=None,
            tracking_opens=None, my_var=None, my_headers):

        request_object = ExplicitMessageRequest(
            from_=from_,
            to=to,
            cc=cc,
            bcc=bcc,
            subject=subject,
            text=text,
            html=html,
            attachment=attachment,
            inline=inline,
            tag=tag,
            campaign=campaign,
            dkim=dkim,
            delivery_time=delivery_time,
            test_mode=test_mode,
            tracking=tracking,
            tracking_clicks=tracking_clicks,
            tracking_opens=tracking_opens,
            my_var=my_var
        )
        url = '{base_url}/messages'.format(base_url=self.url)
        response = self.request(
            'POST', url,
            # By providing this class, we're informing the auto-serialization about
            # how to deserialize the response
            response_entity_type=MessageResponse,
            request_entity=request_object,
            # requestslib_kwargs is a variable that gets passed
            # all the way down to the actual requests library call.
            # Using requestslib_kwargs is the way to overwrite anything
            # forcefully. For your custom headers, this is probably the
            # right solution.
            requestslib_kwargs={'headers': my_headers})
        return response
