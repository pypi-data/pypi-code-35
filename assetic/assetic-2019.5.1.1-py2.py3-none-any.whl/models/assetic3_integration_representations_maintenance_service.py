# coding: utf-8

"""
    Assetic Integration API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

##from assetic.models.web_api_hal_embedded_resource import WebApiHalEmbeddedResource  # noqa: F401,E501
##from assetic.models.web_api_hal_link import WebApiHalLink  # noqa: F401,E501


class Assetic3IntegrationRepresentationsMaintenanceService(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'description': 'str',
        'linked_work_task_id': 'str',
        'planned_quantity': 'float',
        'purchase_order_number': 'str',
        'service_activity_id': 'str',
        'unit_type': 'str',
        'planned_unit_rate': 'float',
        'planned_cost': 'float',
        'actual_quantity': 'float',
        'actual_unit_rate': 'float',
        'actual_cost': 'float',
        'cost_code': 'str',
        'general_ledger': 'str',
        'links': 'list[WebApiHalLink]',
        'embedded': 'list[WebApiHalEmbeddedResource]'
    }

    attribute_map = {
        'id': 'Id',
        'description': 'Description',
        'linked_work_task_id': 'LinkedWorkTaskId',
        'planned_quantity': 'PlannedQuantity',
        'purchase_order_number': 'PurchaseOrderNumber',
        'service_activity_id': 'ServiceActivityId',
        'unit_type': 'UnitType',
        'planned_unit_rate': 'PlannedUnitRate',
        'planned_cost': 'PlannedCost',
        'actual_quantity': 'ActualQuantity',
        'actual_unit_rate': 'ActualUnitRate',
        'actual_cost': 'ActualCost',
        'cost_code': 'CostCode',
        'general_ledger': 'GeneralLedger',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, id=None, description=None, linked_work_task_id=None, planned_quantity=None, purchase_order_number=None, service_activity_id=None, unit_type=None, planned_unit_rate=None, planned_cost=None, actual_quantity=None, actual_unit_rate=None, actual_cost=None, cost_code=None, general_ledger=None, links=None, embedded=None):  # noqa: E501
        """Assetic3IntegrationRepresentationsMaintenanceService - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._description = None
        self._linked_work_task_id = None
        self._planned_quantity = None
        self._purchase_order_number = None
        self._service_activity_id = None
        self._unit_type = None
        self._planned_unit_rate = None
        self._planned_cost = None
        self._actual_quantity = None
        self._actual_unit_rate = None
        self._actual_cost = None
        self._cost_code = None
        self._general_ledger = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if description is not None:
            self.description = description
        if linked_work_task_id is not None:
            self.linked_work_task_id = linked_work_task_id
        if planned_quantity is not None:
            self.planned_quantity = planned_quantity
        if purchase_order_number is not None:
            self.purchase_order_number = purchase_order_number
        if service_activity_id is not None:
            self.service_activity_id = service_activity_id
        if unit_type is not None:
            self.unit_type = unit_type
        if planned_unit_rate is not None:
            self.planned_unit_rate = planned_unit_rate
        if planned_cost is not None:
            self.planned_cost = planned_cost
        if actual_quantity is not None:
            self.actual_quantity = actual_quantity
        if actual_unit_rate is not None:
            self.actual_unit_rate = actual_unit_rate
        if actual_cost is not None:
            self.actual_cost = actual_cost
        if cost_code is not None:
            self.cost_code = cost_code
        if general_ledger is not None:
            self.general_ledger = general_ledger
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def id(self):
        """Gets the id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param id: The id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def description(self):
        """Gets the description of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The description of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param description: The description of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def linked_work_task_id(self):
        """Gets the linked_work_task_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The linked_work_task_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._linked_work_task_id

    @linked_work_task_id.setter
    def linked_work_task_id(self, linked_work_task_id):
        """Sets the linked_work_task_id of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param linked_work_task_id: The linked_work_task_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._linked_work_task_id = linked_work_task_id

    @property
    def planned_quantity(self):
        """Gets the planned_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The planned_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._planned_quantity

    @planned_quantity.setter
    def planned_quantity(self, planned_quantity):
        """Sets the planned_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param planned_quantity: The planned_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._planned_quantity = planned_quantity

    @property
    def purchase_order_number(self):
        """Gets the purchase_order_number of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The purchase_order_number of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._purchase_order_number

    @purchase_order_number.setter
    def purchase_order_number(self, purchase_order_number):
        """Sets the purchase_order_number of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param purchase_order_number: The purchase_order_number of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._purchase_order_number = purchase_order_number

    @property
    def service_activity_id(self):
        """Gets the service_activity_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The service_activity_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._service_activity_id

    @service_activity_id.setter
    def service_activity_id(self, service_activity_id):
        """Sets the service_activity_id of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param service_activity_id: The service_activity_id of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._service_activity_id = service_activity_id

    @property
    def unit_type(self):
        """Gets the unit_type of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The unit_type of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._unit_type

    @unit_type.setter
    def unit_type(self, unit_type):
        """Sets the unit_type of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param unit_type: The unit_type of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._unit_type = unit_type

    @property
    def planned_unit_rate(self):
        """Gets the planned_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The planned_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._planned_unit_rate

    @planned_unit_rate.setter
    def planned_unit_rate(self, planned_unit_rate):
        """Sets the planned_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param planned_unit_rate: The planned_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._planned_unit_rate = planned_unit_rate

    @property
    def planned_cost(self):
        """Gets the planned_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The planned_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._planned_cost

    @planned_cost.setter
    def planned_cost(self, planned_cost):
        """Sets the planned_cost of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param planned_cost: The planned_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._planned_cost = planned_cost

    @property
    def actual_quantity(self):
        """Gets the actual_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The actual_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._actual_quantity

    @actual_quantity.setter
    def actual_quantity(self, actual_quantity):
        """Sets the actual_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param actual_quantity: The actual_quantity of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._actual_quantity = actual_quantity

    @property
    def actual_unit_rate(self):
        """Gets the actual_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The actual_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._actual_unit_rate

    @actual_unit_rate.setter
    def actual_unit_rate(self, actual_unit_rate):
        """Sets the actual_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param actual_unit_rate: The actual_unit_rate of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._actual_unit_rate = actual_unit_rate

    @property
    def actual_cost(self):
        """Gets the actual_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The actual_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: float
        """
        return self._actual_cost

    @actual_cost.setter
    def actual_cost(self, actual_cost):
        """Sets the actual_cost of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param actual_cost: The actual_cost of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: float
        """

        self._actual_cost = actual_cost

    @property
    def cost_code(self):
        """Gets the cost_code of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The cost_code of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._cost_code

    @cost_code.setter
    def cost_code(self, cost_code):
        """Sets the cost_code of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param cost_code: The cost_code of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._cost_code = cost_code

    @property
    def general_ledger(self):
        """Gets the general_ledger of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The general_ledger of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: str
        """
        return self._general_ledger

    @general_ledger.setter
    def general_ledger(self, general_ledger):
        """Sets the general_ledger of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param general_ledger: The general_ledger of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: str
        """

        self._general_ledger = general_ledger

    @property
    def links(self):
        """Gets the links of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The links of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: list[WebApiHalLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param links: The links of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: list[WebApiHalLink]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501


        :return: The embedded of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :rtype: list[WebApiHalEmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this Assetic3IntegrationRepresentationsMaintenanceService.


        :param embedded: The embedded of this Assetic3IntegrationRepresentationsMaintenanceService.  # noqa: E501
        :type: list[WebApiHalEmbeddedResource]
        """

        self._embedded = embedded

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Assetic3IntegrationRepresentationsMaintenanceService, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Assetic3IntegrationRepresentationsMaintenanceService):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
