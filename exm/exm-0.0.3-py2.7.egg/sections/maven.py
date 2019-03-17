# coding=utf-8
import os
import urllib
from jsonpath import jsonpath
import tarfile
import shutil
import ssl

ssl._create_default_https_context =ssl._create_unverified_context

def process(ctx):
    ctx["java"]["properties"].append("maven.multiModuleProjectDirectory=.")
    commands = list()
    commands.append('"${system.JAVA_HOME}/bin/java"')
    commands.extend(map(lambda x: "-%s" % x, jsonpath(ctx, "$.java['jvm-options']")[0]))
    commands.extend(map(lambda x: "-X%s" % x, jsonpath(ctx, "$.java['x-options']")[0]))
    commands.extend(map(lambda x: "-D%s" % x, jsonpath(ctx, "$.java['properties']")[0]))
    downloadWrapper(ctx)
    commands.append("-classpath ${exm.wrapper-classpath} org.apache.maven.wrapper.MavenWrapperMain --file ./assets/maven/runner.xml --quiet spring-boot:run")
    commands.extend(genernateMavenExecutionEnvironment(ctx))
    command = " ".join(commands)
    ctx["exm"]["command"] = command
    pass


def downloadWrapper(ctx):
    url = jsonpath(ctx, "$.maven.wrapper['download-url']")[0]
    try:
        os.makedirs(".exm/mvn-wrapper/")
    except Exception:
        pass
    if os.path.exists(".exm/mvn-wrapper/maven-wrapper-${maven.wrapper.version}"):
        return
    urllib.urlretrieve(url, ".exm/mvn-wrapper/maven-wrapper.tar.gz")
    tar = tarfile.open(".exm/mvn-wrapper/maven-wrapper.tar.gz")
    tar.extractall(".exm/mvn-wrapper")
    ctx["exm"]["wrapper-classpath"] = ".exm/mvn-wrapper/maven-wrapper-${maven.wrapper.version}/.mvn/wrapper/maven-wrapper.jar"
    # FIXME: 增加maven的下载地址覆盖到wrapper的properties中
    pass

def genernateMavenExecutionEnvironment(ctx):
    properties = list()
    properties.extend(jsonpath(ctx, "$.maven.properties")[0])
    properties.extend(map(lambda k: "exm.maven.execution.%s=%s" % (k,jsonpath(ctx, "$.maven.execution.%s" % k)[0]), jsonpath(ctx, "$.maven.execution")[0]))
    artifact = jsonpath(ctx, "$.maven.execution.artifact")[0].split(":")
    properties.append("exm.maven.execution.artifact.group=%s" % artifact[0])
    properties.append("exm.maven.execution.artifact.id=%s" % artifact[1])
    properties.append("exm.maven.execution.artifact.version=%s" % artifact[2])
    return map(lambda x: "-D%s" % x, properties)