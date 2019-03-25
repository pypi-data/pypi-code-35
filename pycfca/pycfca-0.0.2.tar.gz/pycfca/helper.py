import base64

import xmltodict
from lxml import etree


def xml_to_dict(data):
    """解析CFCA接口返回XML"""
    parser = etree.XMLParser(encoding="UTF-8", recover=True)
    tree = etree.fromstring(data, parser)
    xml_str = etree.tostring(tree)
    xmldict = xmltodict.parse(xml_str)
    return xmldict


def is_error(data):
    if data.startswith("<Error>"):
        return False
    return True


def is_200_code(data):
    xmldict = xml_to_dict(data)
    if xmldict.get("Result") and xmldict.get("Result")["Code"] == "200":
        return True
    return False


def get_code_msg(data):
    """
    正常返回:
    <Result>
        <Code>200</Code>
        <Message>successfully!</Message>
    </Result>
    异常返回：
    <Error>
        <!-- 错误码 -->
        <ErrorCode></ErrorCode>
        <!-- 错误信息说明 -->
        <ErrorMessage></ErrorMessage>
    </Error>
    """
    xmldict = xml_to_dict(data)
    if "Error" in xmldict:
        return xmldict["Error"]["ErrorCode"], xmldict["Error"]["ErrorMessage"], xmldict
    elif "Result" in xmldict:
        return xmldict["Result"]["Code"], xmldict["Result"]["Message"], xmldict
    else:
        return None, None, xmldict


def base64_encode(string):
    """base64编码"""
    return str(base64.b64encode(string.encode("utf-8")), "utf-8")


def build_multidata_proof_hash_xml(multidata_list):
    """多媒体文件证据hashXML"""
    proof = []
    for multidata in multidata_list:
        proof.append(multidata.to_proof_hash_xml())
    proof_xml = "".join(proof)
    xml = "<ProofHashXml>" f"{proof_xml}" "</ProofHashXml>"
    return xml


def build_field_bean_list_xml(field_bean_list):
    """组装合成到PDF文本域的业务XML数据"""
    tmp_list = [bean.to_xml() for bean in field_bean_list]
    pdfs_bean_xml = "".join(tmp_list)
    fieldListXml = (
        f'<FieldList hashAlg="sha1" savedBizXmlId="" savedTimeIncrement="" partialFlattening="false">'
        f"{pdfs_bean_xml}"
        f"</FieldList>"
    )
    return fieldListXml
