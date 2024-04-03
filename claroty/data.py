class Data():

  def __init__(self, from_dict=None) -> None:
    if from_dict is not None:       
      self._load(self, from_dict)


  def _load(self, _data, _dict):
    def _get_list_element(o):
      if type(o) == dict:
        return Data(o)
      return o
        
    for k, v in _dict.items():
      if isinstance(v, dict):
        _data.set(k, Data(v))
        continue

      if isinstance(v, list):        
        _data.set(k, list(map(_get_list_element, v)))  
        continue

      _data.set(k, v)


  def set(self, key, value):
    try:        
      setattr(self, key, value)
    except:
      setattr(self, key, None)


  def get(self, attr, _default=None):
    return getattr(self, attr, _default)


  def add(self, from_dict):
    for k,v in from_dict.item():
      self.set(k, v)


  def has(self, attr):
    return hasattr(self, attr)


  def delete(self, attr):
    if self.has(attr):
      delattr(self, attr)


  def pick(self, attributes: list) -> dict:
    return {k: self.get(k) for k in attributes}


  def asdict(self):
    result = {}

    def _get_v(v):
      if isinstance(v, Data):
        result = {}
        for k, v in v.__dict__.items():
          result[k] = _get_v(v)
        return result

      if isinstance(v, dict):
        return {k: _get_v(v) for k,v in v.items()}
      
      if isinstance(v, list):
        return [_get_v(item) for item in v]        

      return v 

    for k, v in self.__dict__.items():
      result[k] = _get_v(v)

    return result


  def __getitem__(self, key):
    return getattr(self, key)


  def __setitem__(self, key, value):    
    self.set(key, value)
  

  def __repr__(self) -> str:
    return str(self.__dict__)        


# if __name__ == "__main__":
#   from_dict = {
#     'name': 'ayalon',
#     'type': 'parent',
#     "more": {
#       'host': 'hidden'
#     }
#   }
#   data = Data(from_dict)
#   print(data.name)
#   print(data.type)
#   data.set('whois', 'tsemach')
#   print(data.whois)  
#   print(data.__dict__)
#   print(data)
#   print(data.get('name'))
#   print(data.get('nameb', 'else'))

#   print(data.more, data.more)
#   print(data.more.host)
#   print(data.more, type(data.more))

#   data = {
#     'some_attr': 'this_is_attr',
#     'some_dict': {
#       '1': 'a',
#       '2': 'b',
#     },
#     'polygons': [{
#       "id": "e6719ec4-6989-4242-b749-0f6753e822d0",     
#       "parent_id": None
#     },
#     {
#       "id": "e6719ec4-6989-4242-b749-0f6753e822d0",      
#       "parent_id": None
#     },
#     [1,2]],
    
#   }
#   print('asdist:', Data(data).asdict())