from dataset_service.dcdataset import get_all_known_dataset_names, get_dcdataset_version, download_dataset_by_name


def test_get_all_known_dataset_names():
    r = get_all_known_dataset_names()
    assert (len(r) > 0)


def test_get_dcdataset_version():
    version = get_dcdataset_version()
    assert version is not None


def test_download_datasets():
    for dataset_name in get_all_known_dataset_names():
        is_success = download_dataset_by_name(dataset_name, f"./{dataset_name}")
        assert is_success
