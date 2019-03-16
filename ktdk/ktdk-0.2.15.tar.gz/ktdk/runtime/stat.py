import logging

from ktdk import utils
from ktdk.core.tests import Test
from ktdk.utils.flatters import flatten_all_tasks, flatten_tests

log = logging.getLogger(__name__)


def _get_tests_with_result(tests, result, res_type='effective'):
    return [t for t in tests if utils.dig_class(t.result, res_type, result)]


def _count_for_tasks(test):
    tasks = flatten_all_tasks(test)
    return _count_for_collection(tasks)


def _count_for_collection(coll, with_checked=False):
    count = dict(all=len(coll))
    if with_checked:
        count['all_checked'] = len([test for test in coll if test.has_checked])
    for res_type in ['passed', 'failed', 'skipped', 'errored']:
        filtered = _get_tests_with_result(coll, res_type)
        count[res_type] = len(filtered)
        if with_checked:
            checked = [test for test in filtered if test.has_checked]
            count[res_type + '_checked'] = len(checked)
        current_tests = _get_tests_with_result(coll, res_type='current', result=res_type)
        count[res_type + '_current'] = len(current_tests)

    return count


def _get_tests_names(tests):
    result = {}

    def __names(res_type):
        sel = _get_tests_with_result(tests, res_type)
        if sel:
            result[res_type] = [selected.namespace for selected in sel]

    for rtype in ['failed', 'errored', 'skipped']:
        __names(res_type=rtype)
    return result


def get_task_info(task):
    return dict(
        name=task.name,
        namespace=task.namespace,
        tags=list(task.tags),
        description=task.desc,
        result=dict(effective=task.result.effective.state, current=task.result.current.state)
    )


def get_tasks_info(test):
    return [get_task_info(task) for task in flatten_all_tasks(test)]


def _get_test_info(test, with_tasks=False):
    test_info = dict(name=test.name, namespace=test.namespace, description=test.desc,
                     tags=list(test.tags),
                     effective_tags=list(test.effective_tags), points=test.points,
                     result=dict(effective=test.result.effective.state,
                                 current=test.result.current.state,
                                 reduced_points=test.result.reduced_points,
                                 effective_points=test.result.effective_points))
    if with_tasks:
        test_info['tasks'] = get_tasks_info(test)
    return test_info


def _get_tests_info(all_tests, with_tasks=False):
    return [_get_test_info(test, with_tasks=with_tasks) for test in all_tests]


def stat_test(test) -> dict:
    """Statistics of the tests
    Args:
        test(Test): Root test

    Returns(dict): computed statistics

    """
    all_tests = flatten_tests(test)
    points = test.result.effective_points
    result = dict(final_points=round(points, 4),
                  result=test.result.effective.state)
    context = test.context or None
    with_tasks = context.config.get('dump_passed') if context else False
    result['tests_count'] = _count_for_collection(all_tests, with_checked=True)
    result['tasks_count'] = _count_for_tasks(test)
    tests = _get_tests_with_result(all_tests, result='passed')
    result['passed_tests'] = [test.namespace for test in tests]
    tests = _get_tests_with_result(all_tests, result='failed')
    result['failed_tests'] = [test.namespace for test in tests]
    result['all_tests'] = _get_tests_info(all_tests, with_tasks=with_tasks)
    return result
