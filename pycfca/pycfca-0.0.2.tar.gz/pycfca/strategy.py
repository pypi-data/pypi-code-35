# -*- coding=utf-8
import xmltodict

from .bean import SealUserInfo, SignLocation


class SealStrategy:
    @staticmethod
    def build_seal_strategy_xml(seal_code, seal_password, sign_location: SignLocation):
        _dict = dict()
        _dict["Request"] = dict()
        _dict["Request"]["SealCode"] = seal_code
        _dict["Request"]["SealPassword"] = seal_password
        _dict["Request"]["Type"] = sign_location.type
        _dict["Request"]["LX"] = sign_location.lx
        _dict["Request"]["LY"] = sign_location.ly
        _dict["Request"]["Keyword"] = sign_location.keyword
        _dict["Request"]["KeywordPositionIndex"] = sign_location.keyword_position_index
        _dict["Request"]["LocationStyle"] = sign_location.location_style
        _dict["Request"]["Page"] = sign_location.page
        _dict["Request"]["OffsetX"] = sign_location.offset_x
        _dict["Request"]["OffsetY"] = sign_location.offset_y
        _dict["Request"]["LocationCode"] = sign_location.location_code
        _dict["Request"]["Visible"] = sign_location.visible
        _dict["Request"]["SealPerson"] = ""
        _dict["Request"]["SealLocation"] = ""
        _dict["Request"]["SealReason"] = ""
        _dict["Request"]["SealImageSize"] = 100  # 印章图片大小
        xml = xmltodict.unparse(_dict, full_document=False)
        return xml

    @staticmethod
    def build_proof_seal_strategy_xml(
        handwriting_image,
        seal_layer_2_text,
        seal_layer_2_text_style,
        proof_hash_xml,
        seal_user_info: SealUserInfo,
        sign_location: SignLocation,
    ):
        """组装PDF数据策略文件"""
        proofSealStrategyXml = (
            "<Request>"
            f"<SealImageSize>50</SealImageSize>"
            # <!-- 手写签名图片（BASE64编码格式） -->
            f"<HandwritingImage>{handwriting_image}</HandwritingImage>"
            # <!-- 印章显示为文本内容（如用户姓名），可以为空，不为空时此文本会替代上面的图片 -->
            f"<SealLayer2Text>{seal_layer_2_text}</SealLayer2Text>"
            # <!-- 文本显示样式（文字大小、文字颜色、显示总宽度），可以为空 -->
            f"<SealLayer2TextStyle>{seal_layer_2_text_style}</SealLayer2TextStyle>"
            # <!-- 签章人，不能为空 -->
            f"<SealPerson>{seal_user_info.user_name}</SealPerson>"
            # <!-- 证件类型，不能为空 -->
            f"<IdentificationType>{seal_user_info.identification_type}</IdentificationType>"
            # <!-- 证件号码，不能为空 -->
            f"<IdentificationNo>{seal_user_info.identification_no}</IdentificationNo>"
            # <!-- 电话号码，可以为空 -->
            f"<PhoneNo>{seal_user_info.phone}</PhoneNo>"
            # <!-- 签章地点，可以为空 -->
            f"<SealLocation>{seal_user_info.seal_location}</SealLocation>"
            # <!-- 签章理由，可以为空 -->
            f"<SealReason>{seal_user_info.seal_reason}</SealReason>"
            # <!-- 秘钥算法那类型（RSA/SM2），默认使用RSA，不能为空 -->
            "<KeyAlg></KeyAlg>"
            # <!-- 是否显示，true or false，默认为true，可以为空 -->
            f"<Visible>{sign_location.visible}</Visible>"
            # <!-- 签章类型（不能为空），1=空白标签签章,2=坐标签章,3=关键字签章，4=位置标识 -->
            f"<Type>{sign_location.type}</Type>"
            # <!-- 左侧的x坐标（单位：像素）；左侧的y坐标（单位：像素）； -->
            f"<Page>{sign_location.page}</Page>"
            f"<LX>{sign_location.lx}</LX>"
            f"<LY>{sign_location.ly}</LY>"
            # <!-- 关键字，按关键字签章时不能为空； -->
            f"<Keyword>{sign_location.keyword}</Keyword>"
            # <!-- 关键字位置索引（1：第一个位置；2：第二个位置；0：默认全部位置盖章，支持1、2、1-3、3-9格式，如果输入非法数字或者负数当做0处理，如果输入的数字大于关键字数量时就在最后一个位置盖章处理） -->
            f"<KeywordPositionIndex>{sign_location.keyword_position_index}</KeywordPositionIndex>"
            # <!-- 位置风格：（上:U；下:D；左:L；右:R；中:C）；默认：C； -->
            f"<LocationStyle>{sign_location.location_style}</LocationStyle>"
            # <!-- 横轴偏移，默认为0（单位：像素）；纵轴偏移，默认为0（单位：像素） -->
            f"<OffsetX>{sign_location.offset_x}</OffsetX>"
            f"<OffsetY>{sign_location.offset_y}</OffsetY>"
            # <!-- 签章位置标识编码，按位置标识签章时不能为空； -->
            f"<LocationCode>{sign_location.location_code}</LocationCode>"
            # <!-- 证据hash，存放到证书的扩展域中 -->
            # <!-- 哈希算法：SHA-1；再转换为HEX字符串 -->
            f"{proof_hash_xml}"
            "</Request>"
        )
        return proofSealStrategyXml

    @staticmethod
    def buildcompound_seal_strategy_xml(seal_strategy_xml, proof_seal_strategy_xml):
        """组合复合签章策略文件"""
        return f"<List>{seal_strategy_xml}{proof_seal_strategy_xml}</List>"
