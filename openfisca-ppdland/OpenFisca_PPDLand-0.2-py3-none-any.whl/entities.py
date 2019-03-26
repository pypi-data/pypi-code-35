from openfisca_core.entities import build_entity

Individu = build_entity(
    key = "individu",
    plural = "individus",
    label = u'Individu',
    is_person = True,
    )

entities = [Individu]
