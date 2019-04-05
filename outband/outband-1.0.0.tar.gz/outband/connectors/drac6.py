import os
import subprocess
import tempfile
import typing
import urllib.parse

import lxml.etree

import outband.base_connector
import outband.util

JNLP_FILE_PREFIX = "outband-jnlp-"
SECURITY_FILE_PREFIX = "outband-security-"
SENSIBLE_DISABLED_JAR_SIGNING_ALGORITHMS = {
	"MD2",
	"MD5",
	"RSA keySize < 1024",
	"DSA keySize < 1024",
}
SENSIBLE_DISABLED_SSL_ALGORITHMS = {
	"SSLv3",
	"RC4",
	"DES",
	"MD5withRSA",
	"DH keySize < 1024",
	"EC keySize < 224",
	"3DES_EDE_CBC",
}

def _host_to_url(netloc:str) -> str:
	return urllib.parse.urlunparse(("https", netloc, "", "", "", ""))

class DRAC6(outband.base_connector.BaseConnector):
	@staticmethod
	def probe(host:str) -> bool:
		netloc = host
		url = _host_to_url(netloc)
		response = outband.util.get_session().get(url + "/login.html")
		return "<title>Integrated Dell Remote Access Controller 6 - Enterprise</title>" in response.text

	@staticmethod
	def connect(host:str, username:typing.Optional[str], password:typing.Optional[str], preserve_temp_files:bool) -> None:
		if username is None:
			username = "root"
		if password is None:
			password = "calvin"
		netloc = host
		url = _host_to_url(netloc)
		root = lxml.etree.Element("jnlp", codebase=url, spec="1.0+")
		document = lxml.etree.ElementTree(root)
		information = lxml.etree.SubElement(root, "information")
		lxml.etree.SubElement(information, "title").text = "iDRAC6 Virtual Console Client"
		lxml.etree.SubElement(information, "vendor").text = "Dell Inc."
		lxml.etree.SubElement(information, "icon", href="%s/images/logo.gif" % url, kind="splash")
		lxml.etree.SubElement(information, "shortcut", online="true")
		application_desc = lxml.etree.SubElement(root, "application-desc", attrib={"main-class": "com.avocent.idrac.kvm.Main"})
		lxml.etree.SubElement(application_desc, "argument").text = "title=DRAC KVM: %s" % netloc
		lxml.etree.SubElement(application_desc, "argument").text = "ip=%s" % netloc
		lxml.etree.SubElement(application_desc, "argument").text = "vmprivilege=true"
		lxml.etree.SubElement(application_desc, "argument").text = "helpurl=%s/help/contents.html" % url
		lxml.etree.SubElement(application_desc, "argument").text = "user=%s" % username
		lxml.etree.SubElement(application_desc, "argument").text = "passwd=%s" % password
		lxml.etree.SubElement(application_desc, "argument").text = "kmport=5900"
		lxml.etree.SubElement(application_desc, "argument").text = "vport=5900"
		lxml.etree.SubElement(application_desc, "argument").text = "apcp=1"
		lxml.etree.SubElement(application_desc, "argument").text = "version=2"
		security = lxml.etree.SubElement(root, "security")
		lxml.etree.SubElement(security, "all-permissions")
		resources = lxml.etree.SubElement(root, "resources")
		lxml.etree.SubElement(resources, "j2se", version="1.6 1.5 1.4+")
		lxml.etree.SubElement(resources, "jar", href="%s/software/avctKVM.jar" % url, download="eager", main="true")
		lxml.etree.SubElement(resources, "jar", href="%s/software/jpcsc.jar" % url, download="eager")
		operating_systems = {
			"Windows": "Win",
			"Linux": "Linux",
			"Mac OS X": "Mac",
		}
		architectures = {
			"x86": "32",
			"i386": "32",
			"i486": "32",
			"i586": "32",
			"i686": "32",
			"x86_64": "64",
			"amd64": "64",
		}
		for java_operating_system, dell_operating_system in operating_systems.items():
			for java_architecture, dell_architecture in architectures.items():
				dell_suffix = "%s%s" % (dell_operating_system, dell_architecture)
				resources_native = lxml.etree.SubElement(root, "resources", os=java_operating_system, arch=java_architecture)
				lxml.etree.SubElement(resources_native, "jar", href="%s/software/avctKVMIO%s.jar" % (url, dell_suffix), download="eager")
				lxml.etree.SubElement(resources_native, "jar", href="%s/software/avctVM%s.jar" % (url, dell_suffix), download="eager")

		disabled_jar_signing_algorithms = SENSIBLE_DISABLED_JAR_SIGNING_ALGORITHMS.copy()
		disabled_jar_signing_algorithms.discard("MD5")
		disabled_ssl_algorithms = SENSIBLE_DISABLED_SSL_ALGORITHMS.copy()
		disabled_ssl_algorithms.discard("3DES_EDE_CBC")

		with tempfile.NamedTemporaryFile(prefix=JNLP_FILE_PREFIX, delete=(not preserve_temp_files)) as jnlp_file, tempfile.NamedTemporaryFile(mode="w", prefix=SECURITY_FILE_PREFIX, delete=(not preserve_temp_files)) as security_file:
			document.write(jnlp_file, encoding="utf-8", xml_declaration=True)
			jnlp_file.flush()
			security_file.write("jdk.jar.disabledAlgorithms=%s\n" % (", ".join(disabled_jar_signing_algorithms)))
			security_file.write("jdk.tls.disabledAlgorithms=%s\n" % (", ".join(disabled_ssl_algorithms)))
			security_file.flush()

			environment = os.environ.copy()
			environment["JAVA_TOOL_OPTIONS"] = "-Djava.security.properties=%s" % security_file.name
			subprocess.check_call(["javaws", "-jnlp", jnlp_file.name], env=environment)
