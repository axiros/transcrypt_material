import tools
class KendoComponent:
    _k_cls, _k_obj = None, None # the kendo component and instance
    # containing direct callable functions, e.g. open on a datepicker:
    # to be set by a descendant
    _functions = None

    def __init__(self, opts):
        opts = dict(opts)
        for k in opts.keys():
            setattr(self, k, opts[k])
        self.post_init()
        if not self.mount:
            self.instantiate()

    def post_init(self):
        """ customization hook"""
        pass

    def instantiate(self):
        # instantiation of dom-less components:
        if self._jqel:
            self._k_obj = __new__(self._k_cls(self._jqel, self.opts()))
        else:
            self._k_obj = __new__(self._k_cls(self.opts()))

        if self._functions:
            # setting the functions into our selfes, take care of 'this' in the
            # funcs:
            for k in self._functions:
                setattr(self, k, getattr(self._k_obj, k).bind(self._k_obj))
        return self

    def opts(self):
        ''' deliver all our non _ params '''
        __pragma__('js', '{}', '''var jsopts = {}''') # want a plain js obj
        for k in dir(self):
            if not k.startswith('_'):
                v = self[k]
                if not tools.jstype(v, 'function'):
                    jsopts[k] = v
                else:
                    if k.startswith('on_'):
                        jsopts[k[3:]] = v
        return jsopts





__pragma__('alias', 'jq', '$')
class KendoWidget(KendoComponent):
    _jqel      = None # the jquery wrapper where we are mounted
    def __init__(self, opts, selector):
        KendoComponent.__init__(self, opts)
        if selector:
            self.mount(selector)

    def mount(self, selector):
        jels = jq(selector)
        if len(jels) != 1:
            raise Exception("You have 0 or more than one match on the selector")
        self._jqel = jels[0]
        return self.instantiate()

