import json
from abc import ABC
from pydantic import BaseModel, Field, InstanceOf
import ipaddress


class Rule(ABC):
  name: str

  @classmethod
  def create(cls, json_input: str):
    data = json.loads(json_input)    
    if 'source_subnet' in data:            
      data['source_subnet'] = ipaddress.IPv4Network(data['source_subnet'])    
      return ArupaRule(**data)

    if 'source_ip' in data and 'destination_ip' in data:
      data['source_ip'] = ipaddress.IPv4Address(data['source_ip'])
      data['destination_ip'] = ipaddress.IPv4Address(data['destination_ip'])        
      return FriscoRule(**data)
  
    raise ValueError('illegal rule json input')


  def isArupa(self) -> True:
    return 'source_subnet' in dict(self)


  def isFrisco(self) -> True:
    return 'source_ip' in dict(self) and 'destination_ip' in dict(self) 


class ArupaRule(Rule, BaseModel):   
  name: str = Field(max_length=64, pattern=r'^[A-Za-z0-9_-]*$')
  ip_proto: int = Field(gt=0, le=255)
  source_port: int = Field(gt=0, le=65536)
  source_subnet: InstanceOf[ipaddress.IPv4Network]
  
  
class FriscoRule(Rule, BaseModel):   
  name: str = Field(max_length=64, pattern=r'^[A-Za-z0-9_-]*$')
  ip_proto: int = Field(gt=0, le=255)
  source_port: int = Field(gt=0, le=65536)
  source_ip: InstanceOf[ipaddress.IPv4Address]
  destination_ip: InstanceOf[ipaddress.IPv4Address]
  
