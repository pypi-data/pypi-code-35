import specular


@specular.make_constructor
def processor_constructor(spec):
    return specular.getval(spec, ('module_path',))


@specular.make_constructor
def action_constructor(context):
    processors = specular.iter_spec_artifacts(context, ('processors',))
    return set(processors)


@specular.make_constructor
def collection_constructor(context):
    v = set().union(
        *specular.iter_spec_artifacts(context, ('actions',)))

    return v.union(
        *specular.iter_spec_artifacts(context, ('fields',)))


@specular.make_constructor
def endpoint_constructor(context):
    return set().union(
        *specular.iter_spec_artifacts(context, ('collections',)))


@specular.make_constructor
def app_constructor(context):
    return set().union(
        *specular.iter_spec_artifacts(context, ('endpoints',)))


COLLECT_CONSTRUCTORS = {
    '.action': action_constructor,
    '.processor': processor_constructor,
    '.collection': collection_constructor,
    '.endpoint': endpoint_constructor,
    '.apimas_app': app_constructor,
}


def collect_processors(spec):
    constructions = {'collect': COLLECT_CONSTRUCTORS}
    artifacts = spec.construct(constructions=constructions)
    return artifacts['collect'][()]
