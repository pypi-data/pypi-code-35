

class CSETracer(Tracer):
  __slots__ = ['cse_table', 'expr', 'id']

  def __init__(self, trace, cse_table, val, id):
    self.trace = trace
    self.cse_table = cse_table
    self.val = val
    self.id = id

  @property
  def aval(self):
    return core.get_aval(self.val)

  def unpack(self):
    t = type(self.id)
    if t is UniqueID:
      ids = (ID(('unpack', self.id, i)) for i in range(len(self.val)))
      return map(partial(CSETracer, self.trace, self.cse_table), self.val, ids)
    elif t is IDTuple:
      return map(partial(CSETracer, self.trace, self.cse_table), self.val, self.id)
    else:
      raise TypeError(t)

  def full_lower(self):
    return self

class CSETrace(Trace):
  def pure(self, val):
    return CSETracer(self, None, val, const_id(val))

  def lift(self, val):
    return CSETracer(self, None, val, const_id(val))

  def sublift(self, val):
    return CSETracer(self, None, val.val, val.id)

  def process_primitive(self, primitive, tracers, params):
    vals_in, ids_in = unzip2((t.val, t.id) for t in tracers)
    id = idfuns.get(primitive, default_id)(primitive, *ids_in, **params)
    cse_table = next(t.cse_table for t in tracers if t.cse_table is not None)
    if id not in cse_table:
      cse_table[id] = primitive.bind(*vals_in, **params)
    return CSETracer(self, cse_table, cse_table[id], id)

  def process_call(self, call_primitive, f, tracers, params):
    raise NotImplementedError

  def post_process_call(self, _, out_tracer):
    raise NotImplementedError

  def pack(self, tracers):
    val = pack([t.val for t in tracers])
    id = IDTuple([t.id for t in tracers])
    cse_table = next(t.cse_table for t in tracers if t.cse_table is not None)
    return CSETracer(self, cse_table, val, id)
