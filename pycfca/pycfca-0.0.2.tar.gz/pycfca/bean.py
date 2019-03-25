import hashlib

import xmltodict


class FieldBean:
    """PDF文本域"""

    def __init__(self, field_id, field_value):
        self.field_id = field_id  # PDF文本域id
        self.field_value = field_value  # 文本值
        self.field_type = "text"  # 类型

    def to_xml(self):
        _dict = dict()
        _dict["Field"] = dict()
        _dict["Field"]["FieldId"] = self.field_id
        _dict["Field"]["FieldValue"] = self.field_value
        _dict["Field"]["FieldType"] = self.field_type
        xml = xmltodict.unparse(_dict, full_document=False)
        return xml


class PdfBean:
    def __init__(
        self, pdf_id="", biz_serial_no="", output_file_path="", return_pdf_or_not="true"
    ):
        self.pdf_id = pdf_id  # 表示之前保存的savedPdfId
        self.biz_serial_no = biz_serial_no  # 业务流水号, 可以为空
        self.output_file_path = output_file_path  # 单据存放地址
        # 是否返回pdf文件流, 默认返回,取值false时，OutputFilePath不能为空
        self.return_pdf_or_not = return_pdf_or_not

    def to_xml(self):
        _dict = dict()
        _dict["PdfBean"] = dict()
        _dict["PdfBean"]["PdfId"] = self.pdf_id
        _dict["PdfBean"]["BizSerialNo"] = self.biz_serial_no
        _dict["PdfBean"]["OutputFilePath"] = self.output_file_path
        _dict["PdfBean"]["ReturnPdfOrNot"] = self.return_pdf_or_not
        xml = xmltodict.unparse(_dict, full_document=False)
        return xml


class SealUserInfo:
    """签章的用户信息类"""

    def __init__(
        self,
        user_name,
        identification_type,
        identification_no,
        phone="",
        seal_location="",
        seal_reason="",
    ):
        self.user_name = user_name  # 用户名称
        self.identification_type = identification_type  # 证件类型
        self.identification_no = identification_no  # 证件号
        self.phone = phone  # 手机号码
        self.seal_location = seal_location  # 签章位置
        self.seal_reason = seal_reason  # 签章原因


class SignLocation:
    """签章位置信息类"""

    def __init__(self):
        self.type = ""  # 1=空白标签签章,2=坐标签章,3=关键字签章，4=位置标识
        self.page = ""
        self.lx = ""
        self.ly = ""
        self.pdf_index = ""
        self.keyword = ""
        self.location_style = ""
        self.offset_x = ""
        self.offset_y = ""
        self.location_code = ""  # 位置标识（管理页面中配置的签章位置标识信息）
        self.from_page = ""
        self.to_page = ""
        # 关键字位置索引（1：第一个位置；2：第二个位置；0：默认全部位置盖章，支持1、2、1-3、3-9格式，如果输入非法数字或者负数当做0处理，如果输入的数字大于关键字数量时就在最后一个位置盖章处理）
        self.keyword_position_index = ""
        self.visible = ""


class MultiDataBean:
    """多媒体形式的证据信息类"""

    def __init__(self, file_data, file_name, type, descr=""):
        self.file_data = file_data
        self.file_name = file_name
        self.type = type
        self.descr = descr

    def to_proof_hash_xml(self):
        xml = f'<Proof fileName="{self.file_name}" hash="{hashlib.sha1(self.file_data.encode("utf-8")).hexdigest()}" type="{self.type}" descr="{self.descr}"></Proof>'
        return xml

    def to_str(self):
        return {
            "type": self.type,
            "fileName": self.file_name,
            "fileData": self.file_data,
        }
