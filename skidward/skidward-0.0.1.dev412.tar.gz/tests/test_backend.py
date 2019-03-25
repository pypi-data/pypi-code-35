import os

from unittest import mock
import pytest
import redis

from skidward.backend import get_redis_backend, RedisProxy, RedisDummyBackend


class TestRedisBackend:
    def test_get_expected_backend(self):
        backend = get_redis_backend()
        assert backend.__class__.__name__ == "RedisProxy"
        assert backend.backend.__class__.__name__ == "RedisDummyBackend"

    @mock.patch("skidward.backend.StrictRedis")
    def test_get_actual_redis_backend(self, mock_redis):
        # TESTING env var is added via the autouse "enable_testing" fixture
        # Need to remove it to check the real case behavior
        os.environ.pop("WEB_TESTING")
        backend = get_redis_backend()
        assert backend.__class__.__name__ == "RedisProxy"
        assert backend.backend.__class__.__name__ == "MagicMock"

    @pytest.mark.skip(
        reason="What is the benefit of this test? It's frail and seems to test a mock implementation."
    )
    @mock.patch("skidward.backend.StrictRedis")
    def test_call_actual_redis_commands(self, mock_redis):
        backend = get_redis_backend()
        backend.lpush("jobs", 1)
        backend.lrange("jobs", 0, -1)

        calls = [
            mock.call(),
            mock.call().lpush("jobs", 1),
            mock.call().lrange("jobs", 0, -1),
        ]

        assert mock_redis.mock_calls == calls


class TestRedisProxy:
    @pytest.mark.parametrize("expected_class", (RedisDummyBackend, redis.Redis))
    def test_proxy_returns_expected_class(self, expected_class):
        backend = RedisProxy(expected_class)
        assert backend.backend == expected_class

    def test_do_not_compute_string_just_return_it(self, backend):
        input_expected = "task_1"
        assert backend._decode_response(input_expected) == input_expected

    def test_do_compute_byte_to_string(self, backend):
        input_expected = "task_id"
        assert (
            backend._decode_response(input_expected.encode("utf-8")) == input_expected
        )

    def test_do_compute_list_containing_bytes_to_list_of_string(self, backend):
        input = ["task_1", "task_2".encode("utf-8")]
        expected = ["task_1", "task_2"]
        assert backend._decode_response(input) == expected


class TestRedisDummyBackend:
    @pytest.mark.parametrize("list_name, expected", (("job", True), ("nope", False)))
    def test_is_task_new_in_redis_list(self, list_name, expected):
        dummy_backend = RedisDummyBackend()
        assert dummy_backend.is_task_new(list_name)
        dummy_backend.redis_lists["job"] = [1]
        assert not dummy_backend.is_task_new(list_name) is expected

    @pytest.mark.parametrize("jobs_id", (2, [2]))
    def test_lpush_handles_int_and_list(self, jobs_id):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["job"] = ["1".encode("utf-8")]

        dummy_backend.lpush("job", jobs_id)

        assert dummy_backend.redis_lists["job"] == [
            "2".encode("utf-8"),
            "1".encode("utf-8"),
        ]

    @pytest.mark.parametrize("list_name", ("job", "add_me"))
    def test_lpush_creates_redis_list_if_not_existing(self, list_name):
        dummy_backend = RedisDummyBackend()
        assert len(dummy_backend.redis_lists.keys()) == 1

        dummy_backend.lpush(list_name, 1)

        assert len(dummy_backend.redis_lists.keys()) == 2
        jobs = dummy_backend.redis_lists.keys()
        assert list_name in jobs

    @pytest.mark.parametrize("values", ([1], [1, 2], [1, 2, 3]))
    def test_lrange_on_an_existing_job_returns_values(self, values):
        dummy_backend = RedisDummyBackend()
        assert not dummy_backend.lrange("job", 0, -1)
        dummy_backend.redis_lists["job"] = values

        result = dummy_backend.lrange("job", 0, -1)

        assert values == result

    @pytest.mark.parametrize(
        "start, end, expected",
        ((0, -1, [1, 2, 3, 4, 5]), (0, 3, [1, 2, 3, 4]), (1, 3, [2, 3, 4])),
    )
    def test_lrange_returns_expected_segment(self, start, end, expected):
        dummy_backend = RedisDummyBackend()
        assert not dummy_backend.lrange("job", start, end)
        dummy_backend.redis_lists["job"] = [1, 2, 3, 4, 5]

        result = dummy_backend.lrange("job", start, end)

        assert result == expected

    @pytest.mark.parametrize(
        "start, end, expected",
        (
            (-10, 0, [1]),
            (-10, 10, [1, 2, 3, 4, 5]),
            (0, -10, []),
            (6, 10, []),
            (4, 2, []),
        ),
    )
    def test_lrange_when_start_end_are_out_of_bounds(self, start, end, expected):
        dummy_backend = RedisDummyBackend()
        assert not dummy_backend.lrange("job", start, end)
        dummy_backend.redis_lists["job"] = [1, 2, 3, 4, 5]

        result = dummy_backend.lrange("job", start, end)

        assert result == expected

    def test_erase_deletes_redis_list(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["job"] = [1, 2, 3, 4, 5]
        assert dummy_backend.redis_lists
        dummy_backend.erase()
        assert not dummy_backend.redis_lists

    def test_exception(self):
        dummy_backend = RedisDummyBackend()
        with pytest.raises(AttributeError) as attr_error:
            dummy_backend.fake_function()
        assert "'RedisDummyBackend' object has no attribute 'fake_function'" == str(
            attr_error.value
        )

    @pytest.mark.parametrize(
        "exists, expected", ((True, "host_id_1"), (False, "host_id_2"))
    )
    def test_set_creates_list_with_only_one_value(self, exists, expected):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["set"]["task_key_1"] = "host_id_1".encode("utf-8")
        dummy_backend.set("task_key_1", "host_id_2", ex=None, nx=exists)

        assert dummy_backend.redis_lists["set"]["task_key_1"] == expected.encode(
            "utf-8"
        )

    def test_get_function_return_from_set_list(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["set"]["task_key_1"] = "host_id_1".encode("utf-8")
        assert "host_id_1".encode("utf-8") == dummy_backend.get("task_key_1")

    def test_rpop_return_last_element_and_remove_it(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["task_key_1"] = ["host_1", "host_2"]
        assert len(dummy_backend.redis_lists["task_key_1"]) == 2
        assert "host_2" == dummy_backend.rpop("task_key_1")
        assert len(dummy_backend.redis_lists["task_key_1"]) == 1
        assert dummy_backend.redis_lists["task_key_1"] == ["host_1"]

    @pytest.mark.parametrize(
        "list_name, expected", (("task_key_1", False), ("task_key_2", True))
    )
    def test_exists_function_return_true_only_if_list_exists(self, list_name, expected):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["task_key_1"] = "host_1"
        assert dummy_backend.is_task_new(list_name) == expected

    @pytest.mark.parametrize(
        "list_name, expected", (("task_key_1", False), ("task_key_2", True))
    )
    def test_exists_function_return_true_only_if_set_exists(self, list_name, expected):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["set"]["task_key_1"] = "host_1"
        assert dummy_backend.is_task_new(list_name) == expected

    @pytest.mark.parametrize("list_name", ("job", "add_me"))
    def test_hmset_creates_redis_list_if_not_existing(self, list_name):
        dummy_backend = RedisDummyBackend()
        assert len(dummy_backend.redis_lists.keys()) == 1
        new_dict = {"a": 1, "b": "test_b"}
        dummy_backend.hmset(list_name, new_dict)

        assert len(dummy_backend.redis_lists.keys()) == 2
        jobs = dummy_backend.redis_lists.keys()
        assert list_name in jobs

    @pytest.mark.parametrize(
        "my_dict", ({"id": 1, "name": "dict1"}, {"id": 2, "name": "dict2"})
    )
    def test_hmset_pushes_dict_in_redis(self, my_dict):
        dummy_backend = RedisDummyBackend()
        dummy_backend.hmset("job", my_dict)
        assert my_dict in dummy_backend.redis_lists["job"]

    def test_hmget_returns_the_last_dict_from_redis(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["configured_tasks"] = [
            {"id": 1, "name": "dict1"},
            {"id": 2, "name": "dict2"},
        ]
        assert len(dummy_backend.redis_lists["configured_tasks"]) == 2
        assert dummy_backend.hmget("configured_tasks", ["id", "name"]) == (2, "dict2")

    def test_hdel_deletes_the_last_dict_from_redis(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["configured_tasks"] = [
            {"id": 1, "name": "dict1"},
            {"id": 2, "name": "dict2"},
        ]
        assert len(dummy_backend.redis_lists["configured_tasks"]) == 2
        dummy_backend.hdel("configured_tasks", ["id", "name"])
        assert dummy_backend.redis_lists["configured_tasks"] == [
            {"id": 1, "name": "dict1"}
        ]

    def test_list_is_deleted_if_expire(self):
        dummy_backend = RedisDummyBackend()
        dummy_backend.redis_lists["job"] = ["1"]

        assert "job" in dummy_backend.redis_lists
        dummy_backend.expire("job")
        assert not "job" in dummy_backend.redis_lists
