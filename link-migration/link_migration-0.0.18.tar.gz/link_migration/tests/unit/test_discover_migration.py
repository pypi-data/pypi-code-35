# -*- coding: utf-8 -*-

import link_migration.example_migrations.conf

from link_migration.framework.model import DiscovererMigration, MigrationWrapper
from link_migration.example_migrations import delete_upgrade, without_docstring
from link_migration.example_migrations import using_self, hello_world, exception


class TestDiscovererMigrationMidleVersion:
    def setUp(self):
        self.old_current_version = link_migration.example_migrations.conf.current_version
        link_migration.example_migrations.conf.current_version = lambda: '0.0.2'
        self.discover_migrations = DiscovererMigration()

    def tearDown(self):
        link_migration.example_migrations.conf.current_version = self.old_current_version

    def test_should_upgrade(self):
        self.assertEqual([MigrationWrapper(delete_upgrade), MigrationWrapper(exception), MigrationWrapper(
            without_docstring)], list(self.discover_migrations.up_migrations()))

    def test_should_downgrade(self):
        self.assertListEqual([MigrationWrapper(using_self), MigrationWrapper(hello_world)], list(self.discover_migrations.down_migrations()))


class TestDiscovererMigration:

    def setUp(self):
        self.discover_migrations = DiscovererMigration()

    def test_should_upgrade(self):
        self.assertEqual([MigrationWrapper(using_self), MigrationWrapper(delete_upgrade), MigrationWrapper(exception), MigrationWrapper(
            without_docstring)], list(self.discover_migrations.up_migrations()))

    def test_should_downgrade(self):
        self.assertListEqual([MigrationWrapper(hello_world)], list(self.discover_migrations.down_migrations()))

    def test_should_get_migrations_files(self):
        submodules = self.discover_migrations.migrations_files()            
        self.assertListEqual([hello_world, using_self, delete_upgrade, exception, without_docstring], submodules)

    def test_should_get_migrations_files_in_reverse(self):
        submodules = self.discover_migrations.migrations_files(reverse=True)
        self.assertListEqual([without_docstring, exception, delete_upgrade, using_self, hello_world], submodules)

    def test_should_method_is_up(self):
        discover_migrations = DiscovererMigration(version_to='1.0.6')
        is_up = discover_migrations.is_up()
        self.assertTrue(is_up)
        
    def test_should_method_is_down(self):
        discover_migrations = DiscovererMigration(version_to='0.0.0')
        is_down = discover_migrations.is_down()
        self.assertTrue(is_down)

    def test_should_method_is_not_up(self):
        discover_migrations = DiscovererMigration(version_to='0.0.0')
        is_up = discover_migrations.is_up()
        self.assertFalse(is_up)

    def test_should_method_is_not_down(self):
        discover_migrations = DiscovererMigration(version_to='1.0.0')
        is_down = discover_migrations.is_down()
        self.assertFalse(is_down)

    def test_should_return_up_migrations_with_specific_version(self):
        discover_migrations = DiscovererMigration(version_to='0.0.3')
        espected_migrations = [MigrationWrapper(using_self), MigrationWrapper(delete_upgrade)]
        self.assertListEqual(espected_migrations, list(discover_migrations.to_migrations()))

    def test_should_return_down_migration_with_specific_version(self):
        discover_migrations = DiscovererMigration(version_to='0.0.0')
        espected_migrations = [MigrationWrapper(hello_world)]
        self.assertListEqual(espected_migrations, list(discover_migrations.to_migrations()))
