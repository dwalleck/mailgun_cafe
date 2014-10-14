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

import json

from cafe.engine.models.base import AutoMarshallingModel


class ExplicitMessageRequest(AutoMarshallingModel):

    def __init__(
            self, from_=None, to=None, cc=None, bcc=None, subject=None,
            text=None, html=None, attachment=None, inline=None, tag=None,
            campaign=None, dkim=None, delivery_time=None, test_mode=None,
            tracking=None, tracking_clicks=None, tracking_opens=None,
            my_var=None):
        super(ExplicitMessageRequest, self).__init__()
        # From is a keyword in Python, so the standard practice to append an
        # underscore to the name
        self.from_ = from_
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.text = text
        self.html = html
        self.attachment = attachment
        self.inline = inline
        self.tag = tag
        self.campaign = campaign
        self.dkim = dkim
        self.delivery_time = delivery_time
        self.test_mode = test_mode
        self.tracking = tracking
        self.tracking_clicks = tracking_clicks
        self.tracking_opens = tracking_opens
        self.my_var = my_var

    def _obj_to_json(self):
        message_request = {
            'from': self.from_,
            'to': self.to,
            'cc': self.cc,
            'bcc': self.bcc,
            'subject': self.subject,
            'text': self.text,
            'html': self.html,
            'attachment': self.attachment,
            'inline': self.inline,
            # Since the property names don't always make valid or clear
            # variable names, by performing a mapping of JSON to properties,
            # we can resolve that issue
            'o:tag': self.tag,
            'o:campaign': self.campaign,
            'o:dkim': self.dkim,
            'o:deliverytime': self.delivery_time,
            'o:testmode': self.test_mode,
            'o:tracking': self.tracking,
            'o:tracking-clicks': self.tracking_clicks,
            'o:tracking-opens': self.tracking_opens
        }

        # I'm choosing to make v: data a seperate parameter, but you could
        # possibly handle this cleverly with kwargs. I am assuming that
        # the end user formatted the key names correctly. We could handle
        # that here as well by pre-pending "v:" to each key name
        if my_var is not None:
            message_request.update(self.my_var)

        # This step removes any properties that were not set
        # from the dictionary
        self._remove_empty_values(message_request)
        return json.dumps(message_request)


class MappedMessageRequest(AutoMarshallingModel):

    property_map = {
         'from': 'from',
         'to': 'to',
         'cc': 'cc',
         'bcc': 'bcc',
         'subject': 'subject',
         'text': 'text',
         'html': 'html',
         'attachment': 'attachment',
         'inline': 'inline',
         'tag': 'o:tag',
         'campaign': 'o:campaign',
         'dkim': 'o:dkim',
         'delivery_time': 'o:deliverytime',
         'test_mode': 'o;testmode',
         'tracking': 'o:tracking',
         'tracking_clicks': 'o:tracking-clicks',
         'tracking_opens': 'o:tracking-opens'
    }

    def __init__(self, **kwargs):
        # You can do this without the mapping. We (Brandon) used to call it
        # dotted dictionaries. Not having some type of codified mapping makes
        # telling what properties a model has impossible until run time.
        # This is the happy middle ground

        for key, value in kwargs.iteritems():
            if key in self.property_map:
                setattr(self, self.property_map[key], value)

    def _obj_to_json(self):
        # TODO: Reverse the mapping and make the JSON dictionary from that.
        # There's still the special of the "v:" params to handle as well
