
import json
from datetime import datetime, timezone, timedelta

name = 'ringcentral_bot_framework_extension_world_time'

locs = [
  'Etc/GMT+12', #-12
  'Pacific/Pago_Pago', #-11
  'Pacific/Honolulu', #-10
  'US/Anchorage', #-9
  'US/Los_Angeles', #-8
  'US/Denver', #-7
  'US/Chicago', #-6
  'US/New_York', #-5
  'US/Port_of_Spain', #-4
  'US/Argentina/Mendoza', #-3
  'US/Noronha', #-2
  'US/Scoresbysund', #-1
  'Africa/Abidjan', #0
  'Africa/Lagos', #1
  'Africa/Maputo', #2
  'Africa/Nairobi', #3
  'Europe/Samara', #4
  'Asia/Ashgabat', #5
  'Asia/Dhaka', #6
  'Asia/Bangkok', #7
  'Asia/Shanghai', #8
  'Asia/Seoul', #9
  'Australia/Sydney', #10
  'Pacific/Pohnpei', #11
  'Pacific/Auckland', #12
  'Pacific/Apia', #13
  'Pacific/Kiritimati', #14
]

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  event,
  handledByOtherExtension
):
  """
  bot got group chat message: text
  bot extension could send some response
  return True when bot send message, otherwise return False
  """
  if handledByOtherExtension or not f'![:Person]({bot.id})' in text:
    return False

  if f'![:Person]({bot.id}) world time' == text:
    res = ''
    start = -12
    for i in range(27):
      h = i + start
      d = timedelta(hours=h)
      tz = timezone(d)
      t = tz.fromutc(datetime.utcnow().replace(tzinfo=tz))
      res = res + f'\n' + t.strftime('%Y-%m-%d %H:%M:%S -- %Z ') + f'**{locs[i]}** '
    bot.sendMessage(
      groupId,
      {
        'text': res
      }
    )
    return True
  else:
    return False