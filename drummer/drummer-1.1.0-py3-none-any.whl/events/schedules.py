#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.foundation import Response, StatusCode, FollowUp
from drummer.database import SqliteSession, Schedule


class ScheduleAddEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create(config)

        try:

            # get schedulation data from the user
            schedulation = request.data

            # create and add schedule object
            schedule = Schedule(
                name = schedulation.get('name'),
                description = schedulation.get('description'),
                cronexp = schedulation.get('cronexp'),
                parameters = schedulation.get('parameters'),
                enabled = schedulation.get('status')
            )

            # save
            session.add(schedule)
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to add the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been added.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleListEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        response = Response()

        follow_up = FollowUp(None)

        data = {}

        try:

            # get all schedules
            session = SqliteSession.create(config)

            schedules = session.query(Schedule).group_by(Schedule.name).all()

            session.close()

            schedule_list = []
            for s in schedules:

                d = {}
                d['id'] = s.id
                d['name'] = s.name
                d['description'] = s.description
                d['cronexp'] = s.cronexp
                d['enabled'] = s.enabled

                schedule_list.append(d)

            data['Result'] = schedule_list

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        else:
            response.set_status(StatusCode.STATUS_OK)

        finally:
            response.set_data(data)

        return response, follow_up


class ScheduleRemoveEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create(config)

        try:

            # delete
            sched_to_remove = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            session.delete(sched_to_remove)

            # save
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to remove the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been removed.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleDisableEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create(config)

        try:

            # disable
            sched = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            sched.enabled = False

            # save
            session.add(sched)
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to disable the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been disabled.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleEnableEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create(config)

        try:

            # enable
            sched = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            sched.enabled = True

            # save
            session.add(sched)
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to enable the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been enabled.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleExecEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        follow_up = FollowUp('EXECUTE', schedule_id)

        response = Response()
        response.set_status(StatusCode.STATUS_OK)
        response.set_data({'msg': 'Schedule has been queued for execution.'})

        return response, follow_up


class ScheduleGetEvent:

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        response = Response()
        follow_up = FollowUp(None)

        data = {}

        try:

            # get schedulation id
            args = request.data
            schedule_id = args['schedule_id']

            # get all schedules
            session = SqliteSession.create(config)

            schedule = session.query(Schedule).filter(Schedule.id==schedule_id).one()

            session.close()

            schedule_dict = {
                'id': schedule.id,
                'name': schedule.name,
                'description': schedule.description,
                'cronexp': schedule.cronexp,
                'enabled': schedule.enabled,
                'parameters': schedule.parameters,
            }

            data['Result'] = schedule_dict

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        else:
            response.set_status(StatusCode.STATUS_OK)

        finally:
            response.set_data(data)

        return response, follow_up
