# TODO global:
#     inheritance from Prism

class PrismRegular:
    def __init__(self,
                       top_facet=None, bot_facet=None,
                       central_axe_segment=None, inner_r=None,  # TODO
                                                 outer_r=None,  # TODO
                       special_case_name=None):                 # TODO
        if not None in (top_facet, bot_facet):
            self.init_topbottom(top_facet, bot_facet)
        else:
            print('error in regular prism init:',
                  'incorrect args')
            return None

    def init_topbottom(self, top_facet, bot_facet):
        self.top_facet = top_facet
        self.bot_facet = bot_facet
