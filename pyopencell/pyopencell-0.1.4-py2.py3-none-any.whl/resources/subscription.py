from pyopencell.client import Client
from pyopencell.resources.base_resource import BaseResource
from pyopencell.responses.response import Response
from pyopencell.responses.action_status import ActionStatus


class Subscription(BaseResource):
    _name = "subscription"
    _url_path = "/billing/subscription"

    auditable = {
        "created": None,
        "updated": None,
        "creator": "",
        "updater": "",
    }
    code = ""
    description = ""
    userAccount = ""
    updatedCode = ""
    offerTemplate = ""
    subscriptionDate = None
    terminationDate = None
    endAgreementDate = None
    customFields = []
    terminationReason = ""
    orderNumber = ""
    minimumAmountEl = ""
    minimumAmountElSpark = ""
    minimumLabelEl = ""
    minimumLabelElSpark = ""
    subscribedTillDate = None
    renewed = None
    renewalNotifiedDate = None
    renewalRule = {
        "initialyActiveFor": None,
        "initialyActiveForUnit": "",
        "autoRenew": None,
        "daysNotifyRenewal": None,
        "endOfTermAction": "",
        "terminationReasonCode": "",
        "renewFor": None,
        "renewForUnit": "",
        "extendAgreementPeriodToSubscribedTillDate": None
    }
    billingCycle = "",
    seller = "",
    autoEndOfEngagement = None,
    ratingGroup = ""

    @classmethod
    def get(cls, subscriptionCode):
        """
        Returns a subscription instance obtained by code.

        :param subscriptionCode:
        :return: Subscription:
        """
        response_data = Client().get(
            cls._url_path,
            subscriptionCode=subscriptionCode
        )

        status = response_data.get("status")
        if status and status != "SUCCESS":
            return ActionStatus(**response_data)

        return Response(cls, **response_data)

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a subscription instance.

        :param kwargs:
        :return:
        """
        response_data = Client().post(cls._url_path, kwargs)

        return response_data

    def activate(self, services_to_activate):
        """
        Activate services. Subscription should not be in status (RESILIATED OR CANCELLED).

        :param services_to_activate:
        :return:
        """
        action = "activateServices"
        kwargs = {
            "subscription": self.code,
            "servicesToActivate": {
                "service": services_to_activate,
            }
        }
        response_data = Client().post(
            "{}/{}".format(self._url_path, action),
            kwargs)

        return response_data
