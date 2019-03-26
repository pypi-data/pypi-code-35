# system modules
import datetime
import random
import json
import shlex
import io
import re
import itertools
import collections
import sqlite3

# internal modules
from co2logserver import app
from co2logserver.utils import *
from co2logserver.config import (
    config,
    database,
    osem_account,
    needed_matching_hash_algorithmns,
)
from co2logserver.authentication import authentication
from co2logserver.exceptions import *

# external modules
from flask import request, render_template, Response, g
from flask.wrappers import BadRequest


@app.route("/uploadhelp", methods=["GET"])
def upload_instructions_page():
    """
    ``GET`` ``/upload`` method
    """
    if not config("UPLOAD_HELP"):
        raise NotFound()
    testdata = {
        "sensor_temperature_c": [
            round(20 * random.random(), 1) for i in range(5)
        ],
        "sensor_humidity_percent": [
            round(100 * random.random(), 1) for i in range(5)
        ],
    }
    testdata_str = shlex.quote(json.dumps(testdata))
    if config("UPLOAD_REQUIRES_AUTH"):
        needed_hashes = tuple(
            next(needed_matching_hash_algorithmns(), tuple())
        )
    else:
        needed_hashes = None
    return render_template(
        "upload.html",
        server={"name": config("NAME")},
        upload_requires_auth=config("UPLOAD_REQUIRES_AUTH"),
        needed_hashes=needed_hashes,
        testdata={"raw": testdata, "shell": testdata_str},
        request=request,
    )


@app.route("/upload", methods=["POST"])
@authentication(required="CO2LOGSERVER_UPLOAD_REQUIRES_AUTH")
def upload(matching_salts={}):
    """
    ``POST`` ``/upload`` method.
    """
    app.logger.debug("Matching salts: {}".format(matching_salts))
    # Check if this dataset should be included

    # parse the payload
    ctypes = {
        "application/json": lambda: request.get_json(),
        "application/msgpack": lambda: parse_msgpack(request.data),
        "application/x-www-form-urlencoded": lambda: {
            k: [str2num(x) for x in request.form.getlist(k)]
            for k in request.form.keys()
        },
        "text/csv": lambda: csv2table(
            io.StringIO(request.get_data().decode())
        ),
    }
    try:
        data = ctypes.get(request.content_type, lambda: None)()
    except BaseException as e:
        app.logger.error(
            "Could not parse received {} data: {}".format(
                repr(request.content_type), e
            )
        )
    if data is None:
        raise BadRequest(
            "Invalid Content-Type '{}'".format(request.content_type)
        )
    app.logger.debug("Parsed data:\n{}".format(data))

    # convert time
    time_converter = config("TIME_CONVERTER")
    for time_col in filter(lambda c: c in data, config("TIME_COLS")):
        for i, time_col_val in enumerate(data[time_col]):
            try:
                data[time_col][i] = time_converter(time_col_val, time_col)
            except BaseException:
                app.logger.error(
                    "Configured time converter "
                    "{} failed at conversion of '{}' column value "
                    "'{}'. Using current time instead.".format(
                        time_converter, time_col, time_col_val
                    )
                )
    app.logger.debug("Received parsed data: {}".format(data))
    # save the data into the database
    col_length = max([len(l) for l in data.values()])
    if config("CHECKSUM_SALTS"):
        data[config("MATCHED_CHECKSUMS_COL")] = [
            ",".join(
                alg for alg, salt in sorted(matching_salts.items()) if salt
            )
        ] * col_length
        data[config("FAILED_CHECKSUMS_COL")] = [
            ",".join(
                alg for alg, salt in sorted(matching_salts.items()) if not salt
            )
        ] * col_length
    else:
        data[config("MATCHED_CHECKSUMS_COL")] = [None] * col_length
        data[config("FAILED_CHECKSUMS_COL")] = [None] * col_length
    # save the received data into the database
    responsedata = collections.Counter()
    new_columns = set(data.keys()) - set(database().header)
    for new_column in new_columns:
        if not config("ACCEPT_NEW_COLUMN")(new_column):
            app.logger.info(
                "Ignoring {} data according to "
                "CO2LOGSERVER_ACCEPT_NEW_COLUMN".format(repr(new_column))
            )
            data.pop(new_column, None)
    if set(data) <= set(
        (config("MATCHED_CHECKSUMS_COL"), config("FAILED_CHECKSUMS_COL"))
    ) and not config("ALLOW_EMPTY_ROWS"):
        app.logger.info("No data to save and empty rows are disallowed.")
        responsedata["saved-in-db"] = 0
        return Response(json.dumps(responsedata), mimetype="application/json")
    else:
        try:
            rowcount = database().save_records(data)
            responsedata["saved-in-db"] = rowcount
        except sqlite3.OperationalError:
            raise BadRequest("Invalid input")

    # OpenSenseMap upload
    if config("OSEM_UPLOAD"):
        app.logger.debug("OpenSenseMap is wanted")
        time_upload_start = datetime.datetime.utcnow()
        try:
            import sensemapi
        except ImportError as e:  # pragma: no cover
            raise type(e)(
                "For OpenSenseMap integration "
                "the 'sensemapi' package is needed."
            )
        # drop unwanted columns
        data.pop(config("MATCHED_CHECKSUMS_COL"), None)
        for ignored_col in itertools.filterfalse(
            config("OSEM_COL_REDIRECT"),
            set(data.keys())
            - set(
                (
                    config("OSEM_LAT_COL"),
                    config("OSEM_LON_COL"),
                    config("OSEM_TIME_COL"),
                    config("OSEM_HEIGHT_COL"),
                    config("OSEM_BOX_COL"),
                )
            ),
        ):
            app.logger.info(
                "Ignoring column '{}' according to "
                "CO2LOGSERVER_OSEM_COL_REDIRECT".format(ignored_col)
            )
            data.pop(ignored_col, None)
        account = osem_account()
        account_boxes_fetched = False
        app.logger.debug("OpenSenseMap account:\n{}".format(account))
        for i, row in enumerate(listdict_to_dictlist(data)):
            box_col = config("OSEM_BOX_COL")
            app.logger.debug("Column identifying box is '{}'".format(box_col))
            box_col_val = row.get(box_col)
            if not box_col_val and not box_col_val == 0:
                box_col_val = config("OSEM_BOX_COL_DEFAULT")
                app.logger.info(
                    "Dataset Nr. {} has no identifying "
                    "column '{}'. Using default identifier '{}'".format(
                        i, box_col, box_col_val
                    )
                )
            app.logger.debug(
                "Dataset Nr. {} has identifying "
                "column '{}' value of '{}'".format(i, box_col, box_col_val)
            )
            if not config("OSEM_BOX_REDIRECT")(box_col_val):
                app.logger.info(
                    "Box '{}' should not be uploaded according "
                    "to CO2LOGSERVER_OSEM_BOX_REDIRECT".format(box_col_val)
                )
                continue
            lat_col = config("OSEM_LAT_COL")
            if lat_col in row:
                try:
                    lat = float(row.get(lat_col))
                    assert -180 < lat < 180
                except (ValueError, TypeError, AssertionError):
                    app.logger.warning(
                        "Dataset Nr. {} has invalid latitude "
                        "column value '{}'. Skipping upload.".format(
                            i, lat_col
                        )
                    )
                    lat = None
            else:
                lat = None
            lon_col = config("OSEM_LON_COL")
            if lon_col in row:
                try:
                    lon = float(row.get(lon_col))
                    assert -90 < lon < 90
                except (ValueError, TypeError, AssertionError):
                    app.logger.warning(
                        "Dataset Nr. {} has invalid longitude "
                        "column value '{}'. Skipping upload.".format(
                            i, lon_col
                        )
                    )
                    lon = None
            else:
                lon = None
            height_col = config("OSEM_HEIGHT_COL")
            if height_col in row:
                try:
                    height = float(row.get(height_col))
                except (ValueError, TypeError, AssertionError):
                    app.logger.warning(
                        "Dataset Nr. {} has invalid height "
                        "column value '{}'. Skipping upload.".format(
                            i, height_col
                        )
                    )
                    height = None
            else:
                height = None
            box_name = config("OSEM_BOX_NAME_GENERATOR")(
                servername=config("NAME"), box=box_col_val
            )
            box_exposure = config("OSEM_EXPOSURE_DETERMINER")(box=box_col_val)
            # TODO: make the grouptag dynamically determinable
            box_grouptag = config("NAME")
            box_weblink = config("OSEM_DEFAULT_WEBLINK")
            default_box_description = config(
                "OSEM_DEFAULT_DESCRIPTION"
            ).format(servername=config("NAME"))
            app.logger.debug(
                "Dataset Nr. {} is assigned a matching box name "
                "of '{}'".format(i, box_name)
            )
            time_col = config("OSEM_TIME_COL")
            if time_col in row:
                time_col_val = row[time_col]
                if isinstance(time_col_val, datetime.datetime):
                    app.logger.debug(
                        "Measurement time of this dataset "
                        "is {}".format(time_col_val)
                    )
                    last_time = time_col_val
                else:
                    app.logger.error(
                        "'{}' ({}) is {} instead of {} . "
                        "Using current time instead".format(
                            time_col,
                            time_col_val,
                            type(time_col),
                            datetime.datetime,
                        )
                    )
                    last_time = None
            else:
                app.logger.debug(
                    "There is no column named '{}' "
                    "containing the time. Using current time for "
                    "measurement.".format(time_col)
                )
                last_time = None
            if not account_boxes_fetched:
                app.logger.debug("Fetching boxes of OpenSenseMap account...")
                account.get_own_boxes()
            app.logger.debug(
                "The OpenSenseMap account has {} boxes.".format(
                    len(account.boxes)
                )
            )
            # determine the corresponding senseBox
            box = account.boxes.by_name.get(box_name)
            box_changed = False
            if box:
                app.logger.debug(
                    "There is already has a box named '{}':\n{}".format(
                        box_name, box
                    )
                )
                new_props = {
                    "exposure": box_exposure,
                    "grouptag": box_grouptag,
                    "weblink": box_weblink,
                }
                if lat is not None:
                    new_props.update({"current_lat": lat})
                if lon is not None:
                    new_props.update({"current_lon": lon})
                if height is not None:
                    new_props.update({"current_height": height})
                lat_change = abs(
                    box.current_lat
                    - new_props.get("current_lat", box.current_lat)
                )
                lon_change = abs(
                    box.current_lon
                    - new_props.get("current_lon", box.current_lon)
                )
                if lat_change > config("OSEM_MAX_POSITION_CHANGE"):
                    app.logger.warning(
                        "Latitude changed too much ({}°). "
                        "Ignoring value.".format(lat_change)
                    )
                    new_props.pop("current_lat", None)
                if lon_change > config("OSEM_MAX_POSITION_CHANGE"):
                    app.logger.warning(
                        "Longitude changed too much ({}°). "
                        "Ignoring value.".format(lon_change)
                    )
                    new_props.pop("current_lon", None)
                for prop, new_val in new_props.items():
                    if getattr(box, prop) != new_val:
                        app.logger.debug(
                            "Updating box '{}'s {} from '{}' to '{}'".format(
                                box.name,
                                prop,
                                repr(getattr(box, prop)),
                                new_val,
                            )
                        )
                        setattr(box, prop, new_val)
                        box_changed = True
            else:
                app.logger.debug(
                    "There is no box named '{}'. Creating new.".format(
                        box_name
                    )
                )
                if lat is None:
                    app.logger.info(
                        "No latitude available for box {}.".format(box_name)
                    )
                    default_lat = config("DEFAULT_LAT")(box=box_name)
                    if default_lat is not None:
                        app.logger.info(
                            "Default longitude for box {} is {}".format(
                                box_name, default_lat
                            )
                        )
                        lat = default_lat
                    else:
                        app.logger.warning(
                            "Could not determine default "
                            "latitude for box {}".format(box_name)
                        )
                        app.logger.warning(
                            "Cannot create box named '{}' without "
                            "latitude. Skipping.".format(box_name)
                        )
                        continue
                if lon is None:
                    app.logger.info(
                        "No longitude available for box {}.".format(box_name)
                    )
                    default_lon = config("DEFAULT_LON")(box=box_name)
                    if default_lon is not None:
                        app.logger.info(
                            "Default longitude for box {} is {}".format(
                                box_name, default_lon
                            )
                        )
                        lon = default_lon
                    else:
                        app.logger.warning(
                            "Could not determine default "
                            "longitude for box {}".format(box_name)
                        )
                        app.logger.warning(
                            "Cannot create box named '{}' without "
                            "longitude. Skipping.".format(box_name)
                        )
                        continue
                box = sensemapi.senseBox.senseBox(
                    name=box_name,
                    description=default_box_description,
                    weblink=box_weblink,
                    grouptag=box_grouptag,
                    exposure=box_exposure,
                    current_lat=lat,
                    current_lon=lon,
                )
                box_changed = True
            # determine and create/modify corresponding sensors
            sensors_to_upload = []
            for col, val in row.items():
                if val is None:
                    continue
                if col in (
                    box_col,
                    lat_col,
                    lon_col,
                    config("OSEM_LAT_COL"),
                    config("OSEM_LON_COL"),
                    config("OSEM_TIME_COL"),
                    config("OSEM_HEIGHT_COL"),
                    config("OSEM_BOX_COL"),
                    config("FAILED_CHECKSUMS_COL"),
                ):
                    continue
                match = config("OSEM_COL_REGEX").search(col)
                if match:
                    gd = match.groupdict()
                    sensor_type = gd.get("type")
                    unit_converter = config("OSEM_UNIT_COVERTER")
                    sensor_unit = unit_converter(gd.get("unit"))
                    sensor_quantity = gd.get("quantity")
                    sensor_title_generator_kwargs = gd.copy()
                    sensor_title_generator_kwargs.update({"column": col})
                    sensor_title = config("OSEM_SENSOR_TITLE_GENERATOR")(
                        **sensor_title_generator_kwargs
                    )
                    app.logger.debug(
                        "Column '{}' is assigned a sensor with "
                        "title '{}'".format(col, sensor_title)
                    )
                    sensor_icon = config("OSEM_ICON_DETERMINER")(
                        sensor_title_generator_kwargs
                    )
                    app.logger.debug(
                        "The icon for sensor '{}' was determined "
                        "to be '{}'".format(sensor_title, sensor_icon)
                    )
                    sensor_props = {
                        "type": sensor_type,
                        "unit": sensor_unit,
                        "title": sensor_title,
                        "icon": sensor_icon,
                    }
                    try:
                        filtered_val = config("OSEM_VALUE_FILTER")(
                            box=box_name, col=col, val=val
                        )
                        app.logger.debug(
                            "Converted {} value {} to {}".format(
                                repr(col), repr(val), repr(filtered_val)
                            )
                        )
                        val = filtered_val
                    except BaseException as e:
                        app.logger.error(
                            "Could not apply "
                            "CO2LOGSERVER_OSEM_VALUE_FILTER "
                            "to {} value {}: {}".format(
                                repr(col), repr(val), e
                            )
                        )
                    sensor = next(
                        filter(
                            lambda s: all(
                                getattr(s, attr) == val
                                for attr, val in sensor_props.items()
                            ),
                            box.sensors,
                        ),
                        None,
                    )
                    if sensor:
                        app.logger.debug(
                            "Corresponding sensor for column "
                            "'{}' is:\n{}".format(col, sensor)
                        )
                        new_props = {
                            "type": sensor_type,
                            "unit": sensor_unit,
                            "icon": sensor_icon,
                        }
                        for prop, new_val in new_props.items():
                            if getattr(sensor, prop) != new_val:
                                app.logger.debug(
                                    "Updating sensor "
                                    "'{}'s {} from '{}' to '{}'".format(
                                        sensor.title,
                                        prop,
                                        getattr(sensor, prop),
                                        new_val,
                                    )
                                )
                                box_changed = True
                    else:
                        app.logger.debug(
                            "There is no sensor with title '{}', "
                            "unit '{}' and type '{}' "
                            "in the box named '{}'".format(
                                sensor_title,
                                sensor_unit,
                                sensor_type,
                                box.name,
                            )
                        )
                        sensor = sensemapi.sensor.senseBoxSensor(
                            title=sensor_title,
                            unit=sensor_unit,
                            type=sensor_type,
                            icon=sensor_icon,
                        )
                        app.logger.info(
                            "Adding sensor '{}' to box '{}'".format(
                                sensor.title, box.name
                            )
                        )
                        box.add_sensor(sensor)
                        box_changed = True
                    # TODO: If sensemapi was able to update the uploaded box
                    # object correctly, sensors_to_upload could be a simple
                    # list of sensors
                    sensors_to_upload.append(
                        (
                            sensor,
                            last_time
                            or datetime.datetime.utcnow().replace(
                                tzinfo=datetime.timezone.utc
                            ),
                            val,
                        )
                    )
                else:
                    app.logger.debug(
                        "Column '{}' does not look like an "
                        "uploadable column. Skipping.".format(col)
                    )
                    continue
            # update the senseBox
            if box_changed:
                if box.name in account.boxes.by_name:
                    app.logger.debug(
                        "Updating box '{}':\n{}".format(box.name, box)
                    )
                    box.upload_metadata()
                    uploaded_box = box
                    app.logger.debug("Updated box:\n{}".format(uploaded_box))
                    responsedata["osem-updated-boxes"] += 1
                else:
                    if len(box.sensors):
                        app.logger.info(
                            "Uploading new box with name {}".format(
                                repr(box.name)
                            )
                        )
                        app.logger.debug("Box to upload:\n{}".format(box))
                        # TODO: Actually, sensemapi should take care of
                        # updating the uploaded box object with the new IDs...
                        uploaded_box = account.new_box(box)
                        # By design of the OpenSenseMap API, metadata can't
                        # be set during senseBox creation (see
                        # github.com/sensebox/openSenseMap-API/issues/172), so
                        # we have to set is afterwards.
                        for prop in ("description", "weblink"):
                            setattr(uploaded_box, prop, getattr(box, prop))
                        app.logger.debug(
                            "Uploading metadata of box\n{}".format(box)
                        )
                        uploaded_box.upload_metadata()
                        responsedata["osem-new-boxes"] += 1
                    else:
                        app.logger.warning(
                            "Not uploading new box '{}' "
                            "because it would have no sensors".format(box.name)
                        )
                        continue
            else:
                # TODO: If sensemapi was able to update the uploaded box object
                # properly, this would not be necessary
                uploaded_box = box
            # upload the measurements
            really_sensors_to_upload = []
            for old_sensor, sensor_time, sensor_value in sensors_to_upload:

                def sensors_equal(s1, s2):
                    return all(
                        getattr(s1, attr) == getattr(s2, attr)
                        for attr in ("title", "unit", "type", "icon")
                    )

                sensor = next(
                    filter(
                        lambda s: sensors_equal(s, old_sensor),
                        uploaded_box.sensors,
                    ),
                    None,
                )
                app.logger.debug("Matching Sensor: {}".format(sensor))
                if sensor is None:
                    app.logger.error("Could not find matching sensor")
                    raise ValueError("Could not find matching sensor")
                if sensor_time:
                    now = datetime.datetime.utcnow().replace(
                        tzinfo=datetime.timezone.utc
                    )
                    seconds = (now - sensor_time).total_seconds()
                    min_seconds = config("OSEM_MIN_SECONDS_BETWEEN_UPLOADS")
                    if seconds < min_seconds:
                        app.logger.info(
                            "Upload to sensor '{}' is {} seconds "
                            "in the past which is less than "
                            "the configured {} seconds. "
                            "Skipping upload.".format(
                                sensor.title, seconds, min_seconds
                            )
                        )
                        continue
                really_sensors_to_upload.append(
                    (sensor.id, sensor_time, sensor_value)
                )
            try:
                import pandas as pd

                measurements = pd.DataFrame.from_records(
                    really_sensors_to_upload,
                    columns=("sensor_id", "time", "value"),
                )
                app.logger.debug(
                    "measurements DataFrame:\n{}".format(measurements)
                )
                if len(measurements.index):
                    account.post_measurements(box.id, measurements)
                else:
                    app.logger.debug("Nothing to upload to the OpenSenseMap")
                responsedata["osem-uploaded-measurements"] = len(
                    measurements.index
                )
            except ImportError:
                app.logger.info(
                    "The 'pandas' package is not installed. "
                    "OpenSenseMap upload might be very slow."
                )
                for (
                    sensor_id,
                    sensor_time,
                    sensor_value,
                ) in really_sensors_to_upload:
                    sensor = box.sensors.by_id[sensor_id]
                    # The OpenSenseMap API clears all measurements if a sensor
                    # is changed. So we have to set the last measurements here
                    # before checking for the time
                    app.logger.debug(
                        "Setting last measurement value of "
                        "sensor '{}' to {}".format(sensor.title, sensor_value)
                    )
                    app.logger.debug(
                        "Setting time of last measurement of "
                        "sensor '{}' to {}".format(sensor.title, sensor_time)
                    )
                    sensor.last_time = sensor_time
                    sensor.last_value = sensor_value
                    try:
                        app.logger.debug(
                            "Uploading dataset Nr. {} as measurement "
                            "of sensor '{}'".format(i, sensor.title)
                        )
                        sensor.upload_measurement()
                    except sensemapi.errors.OpenSenseMapAPIError as e:
                        if re.search(
                            "cannot.*set.*property.*timestamp.*undefined",
                            str(e),
                            re.IGNORECASE,
                        ):
                            app.logger.error(
                                "A bug in the API (https://"
                                "github.com/sensebox/"
                                "openSenseMap-API/issues/169) "
                                "prevented uploading the measurement "
                                "of sensor '{}'. "
                                "Retrying with current time.".format(
                                    sensor.title
                                )
                            )
                            sensor.last_time = None
                            sensor.upload_measurement()
                            app.logger.debug(
                                "Retrying with current time worked."
                            )
                        else:
                            raise
                    responsedata["osem-uploaded-measurements"] += 1
        tdiff_osem_upload = datetime.datetime.utcnow() - time_upload_start
        app.logger.info(
            "OpenSenseMap upload took {} seconds".format(
                tdiff_osem_upload.total_seconds()
            )
        )

    return Response(json.dumps(responsedata), mimetype="application/json")
