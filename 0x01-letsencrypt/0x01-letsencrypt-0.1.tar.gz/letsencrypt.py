"""Let's Encrypt library for human beings"""

__all__ = ['LetsEncrypt', 'LetsEncryptStaging']

import acme.challenges
import acme.client
import acme.crypto_util
import acme.errors
import acme.messages
import josepy
import OpenSSL


class LetsEncrypt:
    DIRECTORY_URL = 'https://acme-v02.api.letsencrypt.org/directory'

    def __init__(self, key: str, uri=None, *, phone=None, email=None):
        self.uri = uri
        if uri is None:
            self.account = None
        else:
            self.account = acme.messages.RegistrationResource(body={}, uri=uri)
        # noinspection PyTypeChecker
        self.key = josepy.JWK.load(key.encode('ascii'))
        self.session = acme.client.ClientNetwork(self.key, self.account)
        directory_json = self.session.get(self.DIRECTORY_URL).json()
        directory = acme.messages.Directory.from_json(directory_json)
        self.acme = acme.client.ClientV2(directory, self.session)
        if self.account is None:
            message = acme.messages.NewRegistration.from_data(
                phone=phone,
                email=email,
                terms_of_service_agreed=True,
            )
            self.account = self.acme.new_account(message)
            self.uri = self.account.uri

    def order(self, key: str, domains, perform_dns01):
        def select_dns01(challenges):
            for i in challenges:
                if isinstance(i.chall, acme.challenges.DNS01):
                    return i
            raise ValueError('DNS-01 not offered')

        csr = acme.crypto_util.make_csr(key, domains)
        order = self.acme.new_order(csr)
        for auth in order.authorizations:
            challenge = select_dns01(auth.body.challenges)
            response, validation = challenge.response_and_validation(self.key)
            name = auth.body.identifier.value
            domain = challenge.validation_domain_name(name)
            perform_dns01(domain, validation)
            self.acme.answer_challenge(challenge, response)
        return self.acme.poll_and_finalize(order).fullchain_pem

    def revoke(self, fullchain: str):
        # noinspection PyTypeChecker
        certificate = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, fullchain)
        certificate = josepy.ComparableX509(certificate)
        try:
            return self.acme.revoke(certificate, 0)
        except acme.errors.ConflictError:
            pass


class LetsEncryptStaging(LetsEncrypt):
    DIRECTORY_URL = 'https://acme-staging-v02.api.letsencrypt.org/directory'
