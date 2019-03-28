import os
import sys
import platform
import argparse
import traceback
from deriva.core import DerivaServer, ErmrestCatalog, HatracStore, AttrDict, BaseCLI, KeyValuePairArgs, \
    get_credential, format_credential, __version__
from deriva.core.ermrest_model import builtin_types, Table, Column, Key, ForeignKey


class DerivaInitializer(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.hostname = self.kwargs.get("hostname", platform.node())
        self.catalog_id = self.kwargs.get("catalog_id", 1)

        self.server = None
        self.catalog = None
        self.object_store = None
        self.object_store_namespace = "/hatrac/"
        self.groups = AttrDict({})

        # get credential
        token = kwargs.get("token")
        credential_file = kwargs.get("credential_file")
        if token:
            self.credentials = format_credential(token=token)
        elif credential_file:
            self.credentials = get_credential(self.hostname, credential_file)
        else:
            self.credentials = get_credential(self.hostname)


class TutorialInitializer(DerivaInitializer):

    def __init__(self, **kwargs):
        super(TutorialInitializer, self).__init__(**kwargs)

    def initialize_groups(self):
        # initialize groups
        self.groups = AttrDict({
            "admin":   "https://auth.globus.org/5a773142-e2ed-11e8-a017-0e8017bdda58",
            "curator": "https://auth.globus.org/a5cfa412-e2ed-11e8-a768-0e368f3075e8",
            "writer":  "https://auth.globus.org/caa11064-e2ed-11e8-9d6d-0a7c1eab007a",
            "reader":  "https://auth.globus.org/b9100ea4-e2ed-11e8-8b39-0e368f3075e8",
        })

    def initialize_hatrac(self):
        self.object_store = HatracStore('https', self.hostname, self.credentials)
        self.object_store_namespace += "tutorial_project_data"
        if not self.object_store.is_valid_namespace(self.object_store_namespace):
            self.object_store.create_namespace(self.object_store_namespace)
        self.object_store.set_acl(self.object_store_namespace, 'owner', [self.groups.admin])
        self.object_store.set_acl(self.object_store_namespace, 'subtree-create', [self.groups.curator, self.groups.writer])
        self.object_store.set_acl(self.object_store_namespace, 'subtree-update', [self.groups.curator])
        self.object_store.set_acl(self.object_store_namespace, 'subtree-read', [self.groups.reader])

    def initialize_catalog(self):
        self.server = DerivaServer('https', self.hostname, self.credentials)
        self.catalog = self.server.connect_ermrest(self.catalog_id)
        if not self.catalog.exists():
            self.catalog = self.server.create_ermrest_catalog()
        model = self.catalog.getCatalogModel()

        # 1. Modify local representation of catalog ACL config
        model.acls.update({
            "owner": [self.groups.admin],
            "insert": [self.groups.curator, self.groups.writer],
            "update": [self.groups.curator],
            "delete": [self.groups.curator],
            "select": [self.groups.writer, self.groups.reader],
            "enumerate": ["*"]
        })
        # apply these local config changes to the server
        model.apply(self.catalog)

        # 2. Mutate local configuration of client_table which is part of model
        client_table = model.schemas["public"].tables["ermrest_client"]
        client_table.acls.update({
          "select": [self.groups.curator, self.groups.writer, self.groups.reader],
        })
        client_table.column_definitions["client_obj"].acls.update({
          "select": [],
        })
        # apply these local changes to server
        model.apply(self.catalog)

        # 3. Create "Journal" table
        model.schemas["public"].create_table(
            Table.define(
                "Journal",
                [
                    Column.define(
                        "Notes",
                        builtin_types["markdown"],
                        nullok=False,
                        comment="User-provided notes.",
                    )
                ],
                comment="A journal of user-provided notes."
            )
        )
        # retrieve catalog model again to ensure we reflect latest structural changes
        model = self.catalog.getCurrentModel()

        # 4. Create "Journal_Attachment" asset table
        model.schemas["public"].create_table(
            Table.define(
                "Journal_Attachment",
                [
                    Column.define(
                        "journal_rid",
                        builtin_types["text"],
                        nullok=False,
                        comment="The journal entry to which this asset is attached."
                    ),
                    Column.define(
                        "url",
                        builtin_types["text"],
                        nullok=False,
                        comment="The URL of the stored attachment."
                    ),
                    Column.define(
                        "length",
                        builtin_types["int8"],
                        nullok=False,
                        comment="The asset length (byte count)."
                    ),
                    Column.define(
                        "md5",
                        builtin_types["text"],
                        nullok=False,
                        comment="The hexadecimal encoded MD5 checksum of the asset."
                    ),
                    Column.define(
                        "content_type",
                        builtin_types["text"],
                        nullok=True,
                        comment="The content-type of the asset."
                    ),
                    Column.define(
                        "file_name",
                        builtin_types["text"],
                        nullok=True,
                        comment="The suggested local filename on client systems."
                    ),
                ],
                fkey_defs=[
                    ForeignKey.define(
                        ["journal_rid"],
                        "public",
                        "Journal",
                        ["RID"],
                        on_delete="CASCADE",
                        constraint_names=[["public", "Journal_Attachment_journal_rid_fkey"]]
                    ),
                ],
                comment="Assets (files) attached to Journal entries.",
            )
        )
        # retrieve catalog model again to ensure we reflect latest structural changes
        model = self.catalog.getCurrentModel()

        # 5. Annotate "Journal_Attachment" table
        attachment_table = model.schemas["public"].tables["Journal_Attachment"]
        url_column = attachment_table.column_definitions["url"]
        url_column.annotations.update({
            "tag:isrd.isi.edu,2017:asset": {
                "filename_column": "file_name",
                "byte_count_column": "length",
                "md5": "md5",
                "url_pattern": "/hatrac/%s/journal_attachment/{{{journal_rid}}}/{{{_url.md5_hex}}}" %
                               self.object_store_namespace
            }
        })
        attachment_table.annotations.update({
            "tag:isrd.isi.edu,2015:display": {
                "name_style": {"underline_space": True}
            },
            "tag:isrd.isi.edu,2016:visible-columns": {
                "entry": [
                    ["public", "Journal_Attachment_journal_rid_fkey"],
                    "url"
                ]
            }
        })
        model.apply(self.catalog)

        # 6. Allow Self-Service Editing by Writers
        journal_table = model.schemas["public"].tables["Journal"]
        attachment_table = model.schemas["public"].tables["Journal"]
        # we can re-use this generic policy on any table since they all have an RCB column
        self_service_policy = {
            "self_service": {
                "types": ["update", "delete"],
                "projection": ["RCB"],
                "projection_type": "acl"
            }
        }
        journal_table.acl_bindings.update(self_service_policy)
        attachment_table.acl_bindings.update(self_service_policy)

        # apply these local config changes to the server
        model.apply(self.catalog)

        # 7. Prevent Attachments by Unrelated Writers
        journal_fkey = attachment_table.foreign_keys[
            ("public", "Journal_Attachment_journal_rid_fkey")
        ]
        journal_fkey.acls.update({
            "insert": [grps.curator],
            "update": [grps.curator],
        })
        journal_fkey.acl_bindings.update({
            "self_linkage": {
                "types": ["insert", "update"],
                "projection": ["RCB"],
                "projection_type": "acl",
            }
        })

        # 8. Add column to "Journal" table
        # retrieve catalog model again to ensure we reflect latest structural changes
        model = self.catalog.getCurrentModel()
        journal_table.add_column(
            "Date",
            builtin_types["timestamptz"],
            nullok=False,
            comment="User-provided timestamp."
        )
        # apply these local config changes to the server
        model.apply(self.catalog)

    def initialize(self):
        self.initialize_groups()
        self.initialize_hatrac()
        self.initialize_catalog()


class DerivaTutorialCLI(BaseCLI):
    def __init__(self, description, epilog):

        BaseCLI.__init__(self, description, epilog, __version__)
        self.remove_options(['--host', '--config-file'])
        self.parser.add_argument('host', default='localhost', metavar='<host>', help="Fully qualified host name.")
        self.parser.add_argument("kwargs", metavar="[key=value key=value ...]",
                                 nargs=argparse.REMAINDER, action=KeyValuePairArgs, default=dict(),
                                 help="Variable length of whitespace-delimited key=value pair arguments. "
                                      "For example: key1=value1 key2=value2")

    def main(self):
        try:
            args = self.parse_cli()
        except ValueError as e:
            sys.stderr.write(str(e))
            return 2
        if not args.quiet:
            sys.stderr.write("\n")

        try:
            tutorial = TutorialInitializer(hostname=args.host,
                                           token=args.token,
                                           credential_file=args.credential_file,
                                           **args.kwargs)
            tutorial.initialize()
        except:
            traceback.print_exc()
            return 1
        finally:
            if not args.quiet:
                sys.stderr.write("\n\n")
        return 0


def main():
    desc = "DERIVA Tutorial Command-Line Interface"
    info = "For more information see: https://github.com/informatics-isi-edu/deriva-py"
    return DerivaTutorialCLI(desc, info).main()


if __name__ == '__main__':
    sys.exit(main())
