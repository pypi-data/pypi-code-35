import logging
logger = logging.getLogger()

has_icalendar = False
try:
    from icalendar import Calendar, Event, Todo, Journal
    from icalendar.caselessdict import CaselessDict
    from icalendar.prop import vDate, vDatetime
    has_icalendar = True
    import pytz
except ImportError:
    if has_icalendar:
        logger.info('Could not import pytz')
    else:
        logger.info('Could not import icalendar and/or pytz')
    has_icalendar = False



def import_ical(ics="", txt="", vcal=""):
    if not has_icalendar:
        logger.error("Could not import icalendar")
        return False
    logger.debug("ics: {0}, txt: {1}, vcal:{2}".format(ics, txt, vcal))
    if vcal:
        cal = Calendar.from_ical(vcal)
    else:
        g = open(ics, 'rb')
        cal = Calendar.from_ical(g.read())
        g.close()
    ilst = []
    for comp in cal.walk():
        clst = []
        # dated = False
        start = None
        t = ''  # item type
        s = ''  # @s
        e = ''  # @e
        f = ''  # @f
        tzid = comp.get('tzid')
        if comp.name == "VEVENT":
            t = '*'
            start = comp.get('dtstart')
            if start:
                s = start.to_ical().decode()[:16]
                # dated = True
                end = comp.get('dtend')
                if end:
                    e = end.to_ical().decode()[:16]
                    logger.debug('start: {0}, s: {1}, end: {2}, e: {3}'.format(start, s, end, e))
                    extent = parse(e) - parse(s)
                    e = fmt_period(extent)
                else:
                    t = '^'

        elif comp.name == "VTODO":
            t = '-'
            tmp = comp.get('completed')
            if tmp:
                f = tmp.to_ical().decode()[:16]
            due = comp.get('due')
            start = comp.get('dtstart')
            if due:
                s = due.to_ical().decode()
            elif start:
                s = start.to_ical().decode()

        elif comp.name == "VJOURNAL":
            t = u'!'
            tmp = comp.get('dtstart')
            if tmp:
                s = tmp.to_ical().decode()[:16]
        else:
            continue
        summary = comp.get('summary')
        clst = [t, summary]
        if start:
            if 'TZID' in start.params:
                logger.debug("TZID: {0}".format(start.params['TZID']))
                clst.append('@z %s' % start.params['TZID'])

        if s:
            clst.append("@s %s" % s)
        if e:
            clst.append("@e %s" % e)
        if f:
            clst.append("@f %s" % f)
        tzid = comp.get('tzid')
        if tzid:
            clst.append("@z %s" % tzid.to_ical().decode())
            logger.debug("Using tzid: {0}".format(tzid.to_ical().decode()))
        else:
            logger.debug("Using tzid: {0}".format(local_timezone))
            clst.append("@z {0}".format(local_timezone))

        tmp = comp.get('description')
        if tmp:
            clst.append("@d %s" % tmp.to_ical().decode('utf-8'))
        rule = comp.get('rrule')
        if rule:
            rlst = []
            keys = rule.sorted_keys()
            for key in keys:
                if key == 'FREQ':
                    rlst.append(ical_freq_hsh[rule.get('FREQ')[0].to_ical().decode()])
                elif key in ical_rrule_hsh:
                    rlst.append("&%s %s" % (
                        ical_rrule_hsh[key],
                        ", ".join(map(str, rule.get(key)))))
            clst.append("@r %s" % " ".join(rlst))

        tags = comp.get('categories')
        if tags:
            if type(tags) is list:
                tags = [x.to_ical().decode() for x in tags]
                clst.append("@t %s" % u', '.join(tags))
            else:
                clst.append("@t %s" % tags)

        invitees = comp.get('attendee')
        if invitees:
            if type(invitees) is list:
                invitees = [x.to_ical().decode() for x in invitees]
                ilst = []
                for x in invitees:
                    if x.startswith("MAILTO:"):
                        x = x[7:]
                    ilst.append(x)
                clst.append("@i %s" % u', '.join(ilst))
            else:
                clst.append("@i %s" % invitee)

        tmp = comp.get('organizer')
        if tmp:
            clst.append("@u %s" % tmp.to_ical().decode())

        item = u' '.join(clst)
        ilst.append(item)
    if ilst:
        if txt:
            if os.path.isfile(txt):
                tmpfile = "{0}.tmp".format(os.path.splitext(txt)[0])
                shutil.copy2(txt, tmpfile)
            fo = codecs.open(txt, 'w', file_encoding)
            fo.write("\n".join(ilst))
            fo.close()
        elif vcal:
            return "\n".join(ilst)
        return True

def hsh2ical(hsh):
    """
        Convert hsh to ical object and return tuple (Success, object)
    """
    summary = hsh['_summary']
    if hsh['itemtype'] in ['*', '^']:
        element = Event()
    elif hsh['itemtype'] in ['-', '%', '+']:
        element = Todo()
    elif hsh['itemtype'] in ['!', '~']:
        element = Journal()
    else:
        return False, 'Cannot export item type "%s"' % hsh['itemtype']

    element.add('uid', hsh[u'I'])
    if 'z' in hsh:
        # pytz is required to get the proper tzid into datetimes
        tz = pytz.timezone(hsh['z'])
    else:
        tz = None
    if 's' in hsh:
        dt = hsh[u's']
        dz = dt.replace(tzinfo=tz)
        tzinfo = dz.tzinfo
        dt = dz
        dd = dz.date()
    else:
        dt = None
        tzinfo = None
        # tzname = None

    if u'_r' in hsh:
        # repeating
        rlst = hsh[u'_r']
        for r in rlst:
            if 'f' in r and r['f'] == 'l':
                if '+' not in hsh:
                    logger.warn("An entry for '@+' is required but missing.")
                    continue
                    # list only kludge: make it repeat daily for a count of 1
                # using the first element from @+ as the starting datetime
                dz = parse_str(hsh['+'].pop(0), hsh['z']).replace(tzinfo=tzinfo)
                dt = dz
                dd = dz.date()

                r['r'] = 'd'
                r['t'] = 1

            rhsh = {}
            for k in ical_rrule_keys:
                if k in r:
                    if k == 'f':
                        rhsh[ical_hsh[k]] = freq_hsh[r[k]]
                    elif k == 'w':
                        if type(r[k]) == list:
                            rhsh[ical_hsh[k]] = [x.upper() for x in r[k]]
                        else:
                            rhsh[ical_hsh[k]] = r[k].upper()
                    elif k == 'u':
                        uz = parse_str(r[k], hsh['z']).replace(tzinfo=tzinfo)
                        rhsh[ical_hsh[k]] = uz
                    else:
                        rhsh[ical_hsh[k]] = r[k]
            chsh = CaselessDict(rhsh)
            element.add('rrule', chsh)
        if '+' in hsh:
            for pd in hsh['+']:
                element.add('rdate', pd)
        if '-' in hsh:
            for md in hsh['-']:
                element.add('exdate', md)

    element.add('summary', summary)

    if 'q' in hsh:
        element.add('priority', hsh['_p'])
    if 'l' in hsh:
        element.add('location', hsh['l'])
    if 't' in hsh:
        element.add('categories', hsh['t'])
    if 'd' in hsh:
        element.add('description', hsh['d'])
    if 'm' in hsh:
        element.add('comment', hsh['m'])
    if 'u' in hsh:
        element.add('organizer', hsh['u'])
    if 'i' in hsh:
        for x in hsh['i']:
            element.add('attendee', "MAILTO:{0}".format(x))


    if hsh['itemtype'] in ['-', '+', '%']:
        done, due, following = getDoneAndTwo(hsh)
        if 's' in hsh:
            element.add('dtstart', dt)
        if done:
            finz = done.replace(tzinfo=tzinfo)
            fint = vDatetime(finz)
            element.add('completed', fint)
        if due:
            duez = due.replace(tzinfo=tzinfo)
            dued = vDate(duez)
            element.add('due', dued)
    elif hsh['itemtype'] == '^':
        element.add('dtstart', dd)
    elif dt:
        try:
            element.add('dtstart', dt)
        except:
            logger.exception('exception adding dtstart: {0}'.format(dt))

    if hsh['itemtype'] == '*':
        if 'e' in hsh and hsh['e']:
            ez = dz + hsh['e']
        else:
            ez = dz
        try:
            element.add('dtend', ez)
        except:
            logger.exception('exception adding dtend: {0}, {1}'.format(ez, tz))
    elif hsh['itemtype'] == '~':
        if 'e' in hsh and hsh['e']:
            element.add('comment', timedelta2Str(hsh['e']))
    return True, element


def export_ical_item(hsh, vcal_file):
    """
        Export a single item in iCalendar format
    """
    if not has_icalendar:
        logger.error("Could not import icalendar")
        return False

    cal = Calendar()
    cal.add('prodid', '-//etm_tk %s//dgraham.us//' % version)
    cal.add('version', '2.0')

    ok, element = hsh2ical(hsh)
    if not ok:
        return False
    cal.add_component(element)
    (name, ext) = os.path.splitext(vcal_file)
    pname = "%s.ics" % name
    try:
        cal_str = cal.to_ical()
    except Exception:
        logger.exception("could not serialize the calendar")
        return False
    try:
        fo = open(pname, 'wb')
    except:
        logger.exception("Could not open {0}".format(pname))
        return False
    try:
        fo.write(cal_str)
    except Exception:
        logger.exception("Could not write to {0}".format(pname))
    finally:
        fo.close()
    return True


def export_ical_active(file2uuids, uuid2hash, vcal_file, calendars=None):
    """
    Export items from active calendars to an ics file with the same name in vcal_folder.
    """
    if not has_icalendar:
        logger.error('Could not import icalendar')
        return False
    logger.debug("vcal_file: {0}; calendars: {1}".format(vcal_file, calendars))

    calendar = Calendar()
    calendar.add('prodid', '-//etm_tk {0}//dgraham.us//'.format(version))
    calendar.add('version', '2.0')

    cal_tuples = []
    if calendars:
        for cal in calendars:
            logger.debug('processing cal: {0}'.format(cal))
            if not cal[1]:
                continue
            name = cal[0]
            regex = re.compile(r'^{0}'.format(cal[2]))
            cal_tuples.append((name, regex))
    else:
        logger.debug('processing cal: all')
        regex = re.compile(r'^.*')
        cal_tuples.append(('all', regex))

    if not cal_tuples:
        return

    logger.debug('using cal_tuples: {0}'.format(cal_tuples))
    for rp in file2uuids:
        match = False
        for name, regex in cal_tuples:
            if regex.match(rp):
                for uid in file2uuids[rp]:
                    this_hsh = uuid2hash[uid]
                    ok, element = hsh2ical(this_hsh)
                    if ok:
                        calendar.add_component(element)
                break
        if not match:
            logger.debug('skipping {0} - no match in calendars'.format(rp))

    try:
        cal_str = calendar.to_ical()
    except Exception:
        logger.exception("Could not serialize the calendar: {0}".format(calendar))
        return False
    try:
        fo = open(vcal_file, 'wb')
    except:
        logger.exception("Could not open {0}".format(vcal_file))
        return False
    try:
        fo.write(cal_str)
    except Exception:
        logger.exception("Could not write to {0}" .format(vcal_file))
        return False
    finally:
        fo.close()
    return True

