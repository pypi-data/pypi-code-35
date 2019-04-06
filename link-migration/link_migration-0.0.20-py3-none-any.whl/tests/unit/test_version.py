# -*- coding: utf-8 -*-

import link_migration.example_migrations.conf


class TestVersion:

    # def setUp(self):
    #     self.version = Version()

    def test_should_get_current_version_in_configuration(self):
        self.assertEqual("0.0.1", self.version.get_current())

    def test_should_get_current_version_in_current_version_dot_txt(self):
        original_current_version = link_migration.example_migrations.conf.current_version
        del link_migration.example_migrations.conf.current_version
        link_migration.example_migrations.conf.folder = "%s/example_migrations" % link_migration.example_migrations.conf.abs_path
        self.assertEqual("0.0.1", self.version.get_current())
        link_migration.example_migrations.conf.current_version = original_current_version

    def test_should_get_method_set_the_current_version_in_configuration(self):
        original_current_version = link_migration.example_migrations.conf.current_version()
        self.version.set_current("0.0.2")
        self.assertEqual("0.0.2", self.version.get_current())
        self.version.set_current(original_current_version)

    def test_should_set_the_current_version_in_dot_txt(self):
        original_set_current_version = link_migration.example_migrations.conf.set_current_version
        original_current_version = link_migration.example_migrations.conf.current_version
        del link_migration.example_migrations.conf.current_version
        del link_migration.example_migrations.conf.set_current_version
        old_version = self.version.get_current()
        self.version.set_current(version="0.0.3")
        new_version = self.version.get_current()

        self.assertNotEqual(new_version, old_version)
        self.version.set_current(version="0.0.1")
        link_migration.example_migrations.conf.current_version = original_current_version
        link_migration.example_migrations.conf.current_version = original_set_current_version

