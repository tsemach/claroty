import json
from pydantic import BaseModel, Field
from typing import Literal
# from .arupa_rule import ArupaRule
# from .frisco_rule import FriscoRule

class PolicyExistError(Exception):
  pass

class Policy(BaseModel):
  pass

class Policy(BaseModel):
  name: str = Field(max_length=32, pattern=r'^[A-Za-z0-9_-]*$')
  description: str    
  type: Literal['Arupa', 'Frisco']

  def update(self, data: Policy):
    self.__dict__.update(data.__dict__)

  def isArupa(self):
    return self.type == 'Arupa'
  
  def isFrisco(self):
    return self.type == 'Frisco'


class PolicyAPI:
  
  def __init__(self) -> None:
    self._policies = {}
    pass    


  def create_policy(self, json_input: str) -> str:
    try: 
      data = Policy(**json.loads(json_input))

      if data.isArupa():
        # this is Arupa object trite like stage1
        if data.name in self.policies:
          raise PolicyExistError(f'policy {data.name} is already exist!')
        
        self._policies[data.name] = data
        return json.dumps(data.__dict__)

      # at this point data.type must be Frisco is it is validated and not Arupa
      if not data.name in self.policies:        
        self._policies[data.name] = []

      self._policies[data.name].append(data)      
      return json.dumps(data.__dict__)    
    except json.JSONDecodeError:
      raise ValueError('unable to pasrse:', str)


  def read_policy(self, json_identifier: str) -> str:
    data = Policy(**json.loads(json_identifier))

    if data.name not in self.policies:
      raise PolicyExistError(f'unable to read policy {data.name}, not exist')

    return json.dumps(self.policies[data.name], default=lambda o: dict(o), 
      sort_keys=True, indent=2)


  """ rules of updates
  1. if both are Arupa => replace the new one with the old one
  2. if idnt is Arupa and data is Firsco => remove from Arupa and add to Firsco 
  3. if idnt is Frisco and data is Arupa => replace all Firsco with Arupa
  4. if both Fisco => update all fields of idnt with the fields of data

  constraines: 
    A. since this is update policy must be exist otherwise it is an error
    B. name of identifier must be equal to name of the input
  """
  def update_policy(self, json_identifier: str, json_input: str) -> None:
    idnt: Policy = Policy(**json.loads(json_identifier))
    data: Policy = Policy(**json.loads(json_input))

    if idnt.name not in self.policies:
      raise PolicyExistError('unable to find {idnt.name} in polices')

    if idnt.name != data.name:
      raise ValueError('update policy: names are equals')

    # cases 1 and 3: input type is Arupa is just set the policy by its name
    if idnt.isArupa() and data.isArupa() or idnt.isFrisco() and data.isArupa():
      self.policies[data.name] = data
      return self._parse(data.name)

    # case 3: moving from Arupa to Firsco create new list and distroy old Arupa
    if idnt.isArupa() and data.isFrisco():
      self.policies[data.name] = [data]
      return self._parse(data.name)

    # case 4: Firsco update, update all policies identify by data.name with the fields from data
    for policy in self.policies[data.name]:
      policy.update(data)


  def delete_policy(self, json_identifier: str) -> None:
    data: Policy = Policy(**json.loads(json_identifier))    
    del self.policies[data.name]


  def list_policies(self) -> str:
    return json.dumps(list(self.policies.values()), default=lambda o: dict(o), 
      sort_keys=True, indent=2)
  

  def create_rule(self, json_policy_identifier: str, json_rule_input: str) -> str:
      raise NotImplementedError


  def read_rule(self, json_identifier: str) -> str:
      raise NotImplementedError


  def update_rule(self, json_identifier: str, json_rule_input: str) -> None:
      raise NotImplementedError


  def delete_rule(self, json_identifier: str) -> None:
      raise NotImplementedError


  def list_rules(self, json_policy_identifier: str) -> str:
      raise NotImplementedError
  

  def _parse(self, name):
    return json.dumps(self.policies[name], default=lambda o: dict(o), 
      sort_keys=True, indent=2)


  @property
  def policies(self):
    return self._policies
  


