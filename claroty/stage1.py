import json
from pydantic import BaseModel, Field


class PolicyExistError(Exception):
  pass


class PolicyAPI:

  class Data(BaseModel):
    name: str = Field(max_length=32, pattern=r'^[A-Za-z0-9_-]*$')
    description: str

  def __init__(self) -> None:
    self._policies = {}
    pass    


  def create_policy(self, json_input: str) -> str:
    try: 
      data = PolicyAPI.Data(**json.loads(json_input))

      if data.name in self.policies:
        raise PolicyExistError(f'policy {data.name} is already exist!')

      self._policies[data.name] = data
      
      return json.dumps(data.__dict__)
    except json.JSONDecodeError:
      raise ValueError('unable to pasrse:', str)


  def list_policies(self) -> str:
    return json.dumps(list(self.policies.values()), default=lambda o: dict(o), 
      sort_keys=True, indent=2)


  # @property
  # def data(self):
  #   return self._data
  

  @property
  def policies(self):
    return self._policies
  