#    This file is part of KTBS <http://liris.cnrs.fr/sbt-dev/ktbs>
#    Copyright (C) 2011-2012 Pierre-Antoine Champin <pchampin@liris.cnrs.fr> /
#    Universite de Lyon <http://www.universite-lyon.fr>
#
#    KTBS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KTBS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with KTBS.  If not, see <http://www.gnu.org/licenses/>.

"""
Implementation of the xapi-import builtin methods.
"""
from rdfrest.util.iso8601 import parse_date
import json
import logging
import requests
import traceback
from urllib import quote_plus
from urlparse import urljoin, urlparse

from rdflib import BNode, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF

from rdfrest.util.helper_service import make_helper_service
from rdfrest.util.iso8601 import ParseError
from rdfrest.util import Diagnosis
from ktbs.methods.interface import IMethod
from ktbs.engine.builtin_method import register_builtin_method_impl
from ktbs.engine.resource import METADATA
from ktbs.namespace import KTBS

LOG = logging.getLogger(__name__)

BASE_URI = "http://tbs-platform.org/2017/xapi-import/"
METHOD_URI = BASE_URI + "method"

XAPI = Namespace("%smodel#" % BASE_URI)
PROV = Namespace("http://www.w3.org/ns/prov#")

XAPI_HEADERS = {
    "X-Experience-API-Version": "1.0.0",
}

EPOCH = parse_date("1970-01-01T00:00:00Z")

class _XapiImportMethod(IMethod):
    """I implement the xapi-import builtin method.
    """
    uri = URIRef(METHOD_URI)

    def compute_trace_description(self, computed_trace):
        """I implement :meth:`.interface.IMethod.compute_trace_description`.
        """
        diag = Diagnosis("xapi-import.compute_trace_description")
        cstate = {
            "method": "xapi-import",
            "lrs": None,
            "last_seen_date": None,
            "last_seen_ids": [],
            "use-timestamp": False,
            "all-obsels": False,
        }

        params =  self._prepare_params(computed_trace, diag)

        if diag:
            assert params is not None
            model = XAPI[""]
            origin = Literal("1970-01-01T00:00:00Z")
            with computed_trace.edit(_trust=True) as editable:
                editable.add((computed_trace.uri, KTBS.hasModel, model))
                editable.add((computed_trace.uri, KTBS.hasOrigin, origin))
            cstate.update(params)

        else:
            cstate["errors"] = list(diag)


        computed_trace.metadata.set((
            computed_trace.uri,
            METADATA.computation_state,
            Literal(json.dumps(cstate))
        ))
        return diag

    def compute_obsels(self, computed_trace, from_scratch=False):
        """I implement :meth:`.interface.IMethod.compute_obsels`.
        """

        # computed trace is always considered dirty,
        # as the remote LRS may change at any time
        target_obsels = computed_trace.obsel_collection
        target_obsels.metadata.set((
            target_obsels.uri,
            METADATA.dirty,
            Literal("yes")
        ))

        diag = Diagnosis("feed-import.compute_obsels")
        cstate = json.loads(
            computed_trace.metadata.value(computed_trace.uri,
                                          METADATA.computation_state, default="{}"))
        errors = cstate.get("errors")
        if errors:
            for i in errors:
                diag.append(i)
                return diag
        if from_scratch:
            cstate["last_seen_date"] = None
            cstate["last_seen_ids"] = []

        # TODO add cache support?
        session = requests.Session()
        if 'user' in cstate and 'passwd' in cstate:
            session.auth = (cstate['user'], cstate['passwd'])
        session.headers.update(XAPI_HEADERS)

        url = cstate['lrs']
        params = { 'ascending': 'true' }
        last_seen_date = cstate['last_seen_date']
        use_timestamp = cstate['use-timestamp']
        all_obsels = cstate['all-obsels']
        last_seen_ids = set()
        if last_seen_date:
            params['since'] = last_seen_date
            last_seen_ids.update(cstate['last_seen_ids'])
        if 'registration' in cstate:
            params['registration'] = cstate['registration']
        param_str = '&'.join(['%s=%s' % (key, quote_plus(value))
                           for key, value in params.items()])
        url = "".join([url, ('&' if urlparse(url).query else '?'), param_str])

        if last_seen_date is None:
            LOG.debug("Restarting from the beginning")
            target_obsels._empty() # friend #pylint: disable=W0212

        target_uri = computed_trace.uri
        with target_obsels.edit(_trust=True) as editable:
            target_add = editable.add
            while url is not None:

                LOG.debug("Requesting <%s>", url)
                resp = session.get(url)
                if resp.status_code != 200:
                    message = "Could not load statements:\n%s %s\n%s" \
                              % (resp.status_code, resp.reason, resp.text)
                    diag.append(message)
                    return diag
                data = json.loads(resp.text)

                for stmt in data['statements']:
                    try:
                        st_id = stmt['id']
                        st_stored = stmt['stored']
                        if st_stored == last_seen_date:
                            if st_id in last_seen_ids:
                                LOG.debug(
                                    "Skipping %s (already imported)" % st_id)
                                continue
                            else:
                                last_seen_ids.add(st_id)
                        else:
                            last_seen_date = st_stored
                            last_seen_ids = {st_id}

                        _make_statement(target_add, stmt, target_uri,
                                        use_timestamp, all_obsels)
                        LOG.debug("Imported %s", stmt["id"])

                    except Exception as ex:
                        LOG.debug("Error while processing %s, added to diagnosis",
                                  stmt.get("id", "ID-less statement"))
                        diag.append(ex)
                        raise # DEBUG ONLY

                # loading next page, if any
                more = data.get('more')
                if more:
                    url = urljoin(url, more)
                else:
                    url = None


        cstate["last_seen_date"] = last_seen_date
        cstate["last_seen_ids"] = list(last_seen_ids)
        computed_trace.metadata.set((
            computed_trace.uri,
            METADATA.computation_state,
            Literal(json.dumps(cstate))
        ))
        return diag

    @staticmethod
    def _prepare_params(computed_trace, diag):
        """I check and prepare the data required by the method.

        I return the unique source of the computed trace, and a dict of
        useful parameters converted to the expected datatype. If this can not
        be done, I return ``(None, None)``.

        I also populate `diag` with error/warning messages.
        """
        sources = computed_trace.source_traces
        params = computed_trace.parameters_as_dict
        critical = False

        if len(sources) > 0:
            diag.append("Method XapiImport expects no source")
            critical = True

        for key, val in params.items():
            datatype = _PARAMETERS_TYPE.get(key)
            if datatype is None:
                diag.append("WARN: Parameter %s is not used by :xapi-import"
                            % key)
            else:
                try:
                    params[key] = datatype(val)
                except ValueError:
                    LOG.info(traceback.format_exc())

                    diag.append("Parameter %s has illegal value: %s"
                                % (key, val))
                    critical = True
                except ParseError:
                    LOG.info(traceback.format_exc())
                    diag.append("Parameter %s has illegal value: %s"
                                % (key, val))
                    critical = True

        if "lrs" not in params:
            diag.append("Parameter 'lrs' is required")
            critical = True

        if critical:
            return None, None
        else:
            return params


def _make_statement(add, stmt_json, target_uri, use_timestamp, all_obsels):
    st_id = stmt_json['id']
    st_uri = URIRef(st_id, target_uri)
    add((st_uri, KTBS.hasTrace, target_uri))
    add((st_uri, RDF.type, XAPI.Statement))
    if use_timestamp:
        timestamp = stmt_json['timestamp']
    else:
        timestamp = stmt_json['stored']
    beginend = Literal(int((parse_date(timestamp) - EPOCH)
                           .total_seconds() * 1000))
    add((st_uri, KTBS.hasBegin, beginend))
    add((st_uri, KTBS. hasEnd, beginend))
    add((st_uri, KTBS.hasEndDT, Literal(timestamp)))

    add((st_uri, XAPI.id, Literal(st_id)))

    gen_obsel = [all_obsels, st_uri, beginend, "xxx"]

    actor = stmt_json['actor']
    gen_obsel[-1] = "act"
    actor_node = _make_agent(add, actor, *gen_obsel)
    add((st_uri, XAPI.actor, actor_node))

    verb = stmt_json['verb']
    add((st_uri, XAPI.verb, URIRef(verb['id'])))
    _handle_language_map(add, verb.get('display'), st_uri, XAPI.verbDisplay)

    object = stmt_json['object']
    objectType = object.get('objectType', 'Activity')
    pred = XAPI.object
    if objectType == 'Activity':
        gen_obsel[-1] = "obj"
        object_node = _make_activity(add, object, *gen_obsel)
    elif objectType in ('Agent', 'Group'):
        object_node = _make_agent(add, object, *gen_obsel)
    elif objectType in ('StatementRef'):
        object_node = URIRef(object['id'], st_uri)
    else:
        object_node = Literal(json.dumps(object))
    add((st_uri, XAPI.object, object_node))

    if 'result' in stmt_json:
        add((st_uri, XAPI.result, Literal(json.dumps(stmt_json['result']))))
    if 'context' in stmt_json:
        context = stmt_json['context']
        _handle_context(add, context)
    if 'timestamp' in stmt_json:
        add((st_uri, XAPI.timestamp, Literal(stmt_json['timestamp'])))
    add((st_uri, XAPI.stored, Literal(stmt_json['stored'])))
    if 'authority' in stmt_json:
        authority = stmt_json['authority']
        gen_obsel[-1] = "aut"
        authority_node = _make_agent(add, authority, *gen_obsel)
        add((st_uri, XAPI.authority, authority_node))
    if 'attachments' in stmt_json:
        add((st_uri, XAPI.attachments, Literal(json.dumps(stmt_json['attachments']))))

    return st_uri


def _make_agent(add, agent_json, gen_obsel, parent_uri=None, beginend=None, suffix=None):
    if gen_obsel:
        agent_node = URIRef("%s@%s" % (parent_uri, suffix))
        add((agent_node, KTBS.hasTrace, URIRef("./", parent_uri)))
        add((agent_node, KTBS.hasBegin, beginend))
        add((agent_node, KTBS.hasEnd, beginend))
    else:
        agent_node = BNode()

    object_type = agent_json.get('objectType', 'Agent')
    if object_type == 'Agent':
        typ = XAPI.Agent
    elif object_type == 'Group':
        typ = XAPI.Group
    else:
        typ = XAPI[object_type]
    add((agent_node, RDF.type, typ))
    if 'name' in agent_json:
        add((agent_node, FOAF.name, Literal(agent_json['name'])))
    if 'mbox' in agent_json:
        add((agent_node, FOAF.mbox, URIRef(agent_json['mbox'])))
    if 'mbox_sha1sum' in agent_json:
        add((agent_node, FOAF.mbox_sha1sum, Literal(agent_json['mbox_sha1sum'])))
    if 'openid' in agent_json:
        add((agent_node, FOAF.openid, Literal(agent_json['openid'])))
    if 'account' in agent_json:
        account_node = _make_account(add, agent_json['account'])
        add((agent_node, FOAF.account, account_node))
    if 'member' in agent_json:
        for i, agent in enumerate(agent_json['member']):
            member_node = _make_agent(add, agent,
                                      gen_obsel, parent_uri, beginend,
                                      "%s@m%s" % (suffix, (i + 1)),
                                      )
            add((agent_node, FOAF.member, member_node))
    return agent_node

def _make_account(add, account_json):
    account_node = BNode()
    add((account_node, RDF.type, FOAF.OnlineAccount))
    add((account_node, FOAF.accountServiceHomepage, URIRef(account_json['homePage'])))
    add((account_node, FOAF.accountName, Literal(account_json['name'])))
    return account_node

def _handle_language_map(add, lmap_json, subject, predicate):
    if lmap_json is not None:
        for lang, name in lmap_json.items():
            add((subject, predicate, Literal(name, lang=lang)))

def _make_activity(add, activity_json, gen_obsel, parent_uri=None, beginend=None, suffix=None):
    if gen_obsel:
        activity_node = URIRef("%s@%s" % (parent_uri, suffix))
        add((activity_node, KTBS.hasTrace, URIRef("./", parent_uri)))
        add((activity_node, KTBS.hasBegin, beginend))
        add((activity_node, KTBS.hasEnd, beginend))
    else:
        activity_node = BNode()

    add((activity_node, RDF.type, XAPI.Activity))
    add((activity_node, PROV.specializationOf, URIRef(activity_json['id'])))
    # TODO handle all attributes of activity, including extensions
    return activity_node

def _handle_context(add, context_json):
    pass # TODO handle context and extensions



pseudo_bool = lambda x: str(x).lower() not in ("false", "no", "0")

_PARAMETERS_TYPE = {
    "lrs": URIRef,
    "user": unicode,
    "passwd": unicode,
    "registration": unicode,
    # use 'timestamp' instead of 'stored' (requires that 'timestamp is always set)
    "use-timestamp": pseudo_bool,
    # generate obsels (instead of bnodes) for agents and activities
    "all-obsels": pseudo_bool,
}


METHOD_DESCRIPTION = '''
@prefix : <http://liris.cnrs.fr/silex/2009/ktbs#> .

<%s> a :BuiltinMethod .
''' % METHOD_URI

def start_plugin(_config):
    """I get the configuration values from the main kTBS configuration.

    .. note:: This function is called automatically by the kTBS.
              It is called once when the kTBS starts, not at each request.
    """
    register_builtin_method_impl(_XapiImportMethod())
    make_helper_service(METHOD_URI, METHOD_DESCRIPTION, format='n3')

if __name__ == "__main__":
    print _XapiImportMethod()
