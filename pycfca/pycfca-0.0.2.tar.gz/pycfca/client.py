import logging

import requests
from lxml import etree

from .exception import PaperlessClientError, PaperlessosServiceError
from .helper import base64_encode, get_code_msg, is_200_code, is_error, xml_to_dict

logger = logging.getLogger(__name__)


class PaperlessResponse:
    def __init__(self, data, code="200", msg=""):
        self.code = code
        self.msg = msg
        self.data = data

    def is_error(self):
        """是否请求失败"""
        return True if self.code != "200" else False


class PaperlessClient:
    def __init__(self, url, timeout=None, retry=1, session=None):
        self._base_url = f"http://{url}/PaperlessServer/PaperlessServlet"
        self._assist_url = f"http://{url}/PaperlessServer/PaperlessAssistServlet"
        self._timeout = timeout
        self._retry = retry
        if session is None:
            self._session = requests.session()
        else:
            self._session = session

    def send_request(self, url, timeout=15, **kwargs):
        """封装request库发起http请求"""
        timeout = self._timeout if self._timeout else timeout
        kwargs["headers"]["User-Agent"] = "PyCFCA-SDK"
        try:
            for j in range(self._retry):
                res = self._session.post(url, timeout=timeout, **kwargs)
                if res.status_code < 400:  # 2xx和3xx都认为是成功的
                    return res
        except Exception as e:  # 捕获requests抛出的如timeout等客户端错误,转化为客户端错误
            logger.exception("url:%s, exception:%s" % (url, str(e)))
            raise PaperlessClientError(str(e))

        if res.status_code >= 400:  # PaperlessosServiceError
            msg = res.text
            if msg == "":  # 服务器没有返回Error Body时 给出头部的信息
                msg = res.headers
            logger.error(msg)
            raise PaperlessosServiceError(msg)
        return None

    def parase_request(self, data):
        """处理请求返回值"""
        try:
            code, msg, data = get_code_msg(data)
            return PaperlessResponse(data, code, msg)
        except Exception as e:
            logger.error(str(e))
            return PaperlessResponse(data, "-1", str(e))

    def synthesize_template_with_pdfid(
        self, system_no, template_code, saved_pdfid, field_bean_list_xml, operator_code
    ):
        """合成业务数据内容到PDF模板
        systemNo : 流水号
        templateCode : 模版编号
        savedPdfId : 合成PDF临时PDF_ID
        fieldBeanListXml : 需要合成到模版文本域中的业务数据(PDF模版中需要编辑相应文本域)
        """
        payload = (
            f"functionType=synthesizeTemplateWithPdfId"
            f"&systemNo={system_no}"
            f"&savedPdfId={saved_pdfid}"
            f"&templateCode={template_code}"
            f"&fieldBeanListXml={base64_encode(field_bean_list_xml)}"
            f"&operatorCode={operator_code}"
        )
        response = self.send_request(
            self._base_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self.parase_request(response.content)

    def compound_signature_auto_pdf(
        self,
        system_no,
        pdf_bean_xml,
        multi_data,
        compound_seal_strategy_xml,
        operator_code,
    ):
        """PDF自动化复合签章
        systemNo : 流水号
        pdfBeanXml : PDF数据策略文件
        multiData : 需要合成到pdf的多媒体数据
        compoundSealStrategyXml : 复合签章策略文件
        """
        payload = (
            f"functionType=compoundSealAutoPdf"
            f"&systemNo={system_no}"
            f"&pdfBeanXml={pdf_bean_xml}"
            f"&multiData={multi_data}"
            f"&compoundSealStrategyXml={base64_encode(compound_seal_strategy_xml)}"
            f"&operatorCode={operator_code}"
            f"&sceneCertChannel=0"  # 获取场景证书的方式，与证据证书签章策略文件配合使用。默认值为0。
            f"&timestampChannel=0"  # 获取时间戳的方式。默认值为0。
        )
        response = self.send_request(
            self._base_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        content_length = int(response.headers["Content-Length"])
        if content_length < 1000 and is_error(response.content.decode("utf-8")):
            return self.parase_request(response.content)
        if "PDF" not in response.content[:4].decode("utf-8"):
            return self.parase_request(response.content)
        return PaperlessResponse(response.content)

    def get_template(self, template_code: str, operatorCode: str):
        """获取CFCA模版信息"""
        payload = (
            f"functionType=getTemplate"
            f"&templateCode={template_code}"
            f"&operatorCode={operatorCode}"
        )
        response = self.send_request(
            self._assist_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self.parase_request(response.content)
