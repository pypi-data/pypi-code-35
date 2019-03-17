import datetime
import json
from os import remove

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from pdfkit import from_string

from .models import Meeting
from .settings import get_print_options, get_print_styles


class CacheMixin(object):
    cache_timeout = 3600 * 24 * 7

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)


class MeetingsBaseView(CacheMixin, TemplateView):
    DAY_OF_WEEK = (
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )

    def get_meetings(self):
        return Meeting.objects.filter(
            status=1,
        ).select_related(
            'meeting_location',
            'group',
        ).prefetch_related(
            'meeting_location__region',
            # 'types',  # ParentalManyToManyField instead of ManyToManyField causes Django to throw up on this
        ).order_by(
            'day_of_week',
            'start_time',
        )


class MeetingsReactJSView(CacheMixin, TemplateView):
    """
    List all meetings in the Meeting Guide ReactJS plugin.
    """
    template_name = 'meeting_guide/meetings_list_react.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_key'] = "pk.eyJ1IjoiZmxpcHBlcnBhIiwiYSI6ImNqcHZhbjZwdDBldDA0MXBveTlrZG9uaGIifQ.WpB5eRUcUnQh0-P_CX3nKg"
        return context


class MeetingsDataTablesView(MeetingsBaseView):
    """
    List all meetings in a jQuery datatable.
    """
    template_name = 'meeting_guide/meetings_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meetings'] = self.get_meetings()

        return context


class MeetingsPrintView(MeetingsBaseView):
    """
    List all meetings in an HTML printable format.
    """
    template_name = 'meeting_guide/meetings_list_print.html'

    def get_meetings(self):
        return Meeting.objects.select_related(
            'meeting_location__region__parent',
        ).filter(
            status=1,
        ).order_by(
            'day_of_week',
            'meeting_location__region__parent__name',
            'meeting_location__region__name',
            'start_time',
        )

    def get_context_data(self, **kwargs):
        meetings = self.get_meetings()
        meeting_dict = {}

        for m in meetings:
            day = m.get_day_of_week_display()
            region = m.meeting_location.region.parent.name
            sub_region = m.meeting_location.region.name

            if day not in meeting_dict:
                meeting_dict[day] = {}
            if region not in meeting_dict[day]:
                meeting_dict[day][region] = {}
            if sub_region not in meeting_dict[day][region]:
                meeting_dict[day][region][sub_region] = []

            meeting_dict[day][region][sub_region].append({
                "name": m.title,
                "time_formatted": f"{m.start_time:%I:%M%P}",
                "day": day,
                "types": list(m.types.values_list('meeting_guide_code', flat=True)),
                "location": m.meeting_location.title,
                "formatted_address": m.meeting_location.formatted_address,
                "group": m.group.name if m.group else '',
            })

        context = super().get_context_data(**kwargs)
        context['meetings'] = meeting_dict

        return context


class MeetingsPrintDownloadView(MeetingsPrintView):
    """
    Provide a PDF download of all active meetings, sourcing
    the HTML printable format.
    """

    def get(self, request, *args, **kwargs):
        options = get_print_options()
        styles = get_print_styles()

        context = self.get_context_data(**kwargs)
        html_content = render_to_string(self.template_name, context)

        style_filename = f"{get_random_string(50)}.css"
        with open(style_filename, "w") as css_file:
            css_file.write(styles)
            css_file.close()

        pdf_content = from_string(
            html_content,
            False,
            options=options,
            css=style_filename,
        )
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=meeting-guide.pdf"

        remove(style_filename)

        return response


class MeetingsAPIView(MeetingsBaseView):
    """
    Return a JSON response of the meeting list.
    """

    def get(self, request, *args, **kwargs):
        url = f"""{request.META["wsgi.url_scheme"]}://{request.META["SERVER_NAME"]}"""

        meetings = self.get_meetings()
        meetings_dict = []

        for meeting in meetings:
            meetings_dict.append({
                "id": meeting.id,
                "name": meeting.title,
                "slug": meeting.slug,
                "notes": meeting.meeting_details,
                "updated": f"{meeting.last_published_at if meeting.last_published_at else datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
                "location_id": meeting.meeting_location.id,
                "url": f"{url}{meeting.url_path}",
                "time": f"{meeting.start_time:%H:%M}",
                "end_time": f"{meeting.end_time:%H:%M}",
                "time_formatted": f"{meeting.start_time:%H:%M %P}",
                "distance": "",
                "day": str(meeting.day_of_week),
                "types": list(meeting.types.values_list('meeting_guide_code', flat=True)),
                "location": meeting.meeting_location.title,
                "location_notes": "",
                "location_url": f"{url}{meeting.meeting_location.url_path}",
                "formatted_address": meeting.meeting_location.formatted_address,
                "latitude": str(meeting.meeting_location.lat),
                "longitude": str(meeting.meeting_location.lng),
                "region_id": meeting.meeting_location.region.id,
                "region": f"{meeting.meeting_location.region.parent.name}: {meeting.meeting_location.region.name}",

                "group": meeting.group.name if meeting.group else '',
                "image": "",
            })

            """
            Eventually, we'll support regions and subregions:
                "region_id": meeting.meeting_location.region.parent.id,
                "region": meeting.meeting_location.region.parent.name,
                "sub_region_id": meeting.meeting_location.region.id,
                "sub_region": meeting.meeting_location.region.name,
            """

        if settings.DEBUG:
            meetings_dict = json.dumps(meetings_dict, indent=4)
        else:
            meetings_dict = json.dumps(meetings_dict)

        return HttpResponse(meetings_dict, content_type='application/json')


from django.views.generic.edit import UpdateView

from .models import Location


class LocationUpdate(UpdateView):
    model = Location
    fields = ['title', 'address1', 'address2', 'city', 'state', 'postal_code']
