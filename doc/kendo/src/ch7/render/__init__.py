__pragma__('alias', 'jq', '$')


class PlainStateRenderer:
    """ depends on us being a Redux Component with state."""
    template = '{state}'
    select   = None
    _mp  = None
    _rendered_state_id = None # id of last render

    def __repr__(self):
        s = self.id
        if self.select:
            s += '@' + self.select
        return s

    def get_html(self):
        html = '<b>' + self.__repr__() + '</b>'
        for k, v in self.state.items():
            html += '<br>   ' + k + ': ' + v
        return html
    html = property(get_html)

    def dom_mount(self):
        self._mp = jq(self.select)
        self._mp.html(self.template.format({'state': self.html}))

    def dom_update(self):
        ''' re-render after state updates '''
        if self.state._id_ == self._rendered_state_id:
            return

        if not self._mp:
            self.dom_mount()
        else:
            self._mp.html(self.template.format({'state': self.html}))

