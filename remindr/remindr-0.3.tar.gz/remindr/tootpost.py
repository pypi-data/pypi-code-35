# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2017-2019 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''Post a reminder through a toot'''

# 3rd party libraries imports
from mastodon import Mastodon

def tootpost(clioptions, cfgoptions, toot, language):
    '''post a reminder through a toot'''
    if clioptions.dryrun:
        print('Should have tooted with visibility [{visibility}]=> {toot}'.format(visibility=cfgoptions['mastodon']['toot_visibility'], toot=toot))
    else:
        mastodon = Mastodon(
            client_id=cfgoptions['mastodon']['client_credentials'],
            access_token=cfgoptions['mastodon']['user_credentials'],
            api_base_url=cfgoptions['mastodon']['instance_url']
        )
        # if the user users image_path
        if 'path_to_image' in cfgoptions['image'] and cfgoptions['mastodon']['image']:
            mediaid = mastodon.media_post(cfgoptions['image']['path_to_image'])
            mastodon.status_post(toot, media_ids=[mediaid], visibility=cfgoptions['mastodon']['toot_visibility'])
        elif '{lang}_image_path'.format(lang=language) in cfgoptions['image'] and cfgoptions['mastodon']['image']:
            mediaid = mastodon.media_post(cfgoptions['image']['{lang}_image_path'.format(lang=language)])
            mastodon.status_post(toot, media_ids=[mediaid], visibility=cfgoptions['mastodon']['toot_visibility'])
        # if the user uses mastodon_image_path
        elif 'mastodon_image_path' in cfgoptions['image'] and cfgoptions['mastodon']['image']:
            mediaid = mastodon.media_post(cfgoptions['image']['mastodon_image_path'])
            mastodon.status_post(toot, media_ids=[mediaid], visibility=cfgoptions['mastodon']['toot_visibility'])
        else:
            mastodon.status_post(toot, visibility=cfgoptions['mastodon']['toot_visibility'])
