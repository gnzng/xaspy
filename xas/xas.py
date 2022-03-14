
class group():
    """
    Group: a container for variables, modules, and subgroups.
    heavy influenced by xraylarch https://github.com/xraypy/xraylarch 
    """
    __private = ('__private', '_repr_html_')

    def __init__(self, name=None, **kws):
        if name is None:
            name = hex(id(self))
        self.__name__ = name
        for key, val in kws.items():
            setattr(self, key, val)
            
    def __id__(self):
        return id(self)

    def __dir__(self):
        '''
        return list of member names, attached variable spectras and so on
        '''
        cls_members = []
        
        dict_keys = [key for key in self.__dict__]

        return [key for key in cls_members + dict_keys
                if (not key.startswith('_Group_') and
                    not (key.startswith('__') and key.endswith('__')) and
                    key not in self.__private)]

    def _repr_html_(self):
        """
        HTML representation for Jupyter notebook
        """
        html = [f"group name: {self.__name__} | id:{self.__id__()}"]
        html.append("<table>")
        html.append("<tr><td><b>attribute</b></td><td><b>type</b></td><td><b>value</b></td></tr>")
        attrs = self.__dir__()
        atypes = [type(getattr(self, attr)).__name__ for attr in attrs]
        atvalues = [getattr(self, attr) for attr in attrs]
        
        
        html.append(''.join([f"<tr><td>{attr}</td><td><i>{atp}</i></td><td><i>{atv}</i></td></tr>" 
                             for attr, atp, atv in zip(attrs, atypes,atvalues)]))
        html.append("</table>")
        return ''.join(html)


