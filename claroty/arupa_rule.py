import json
import ipaddress
from pydantic import BaseModel, Field, InstanceOf

class ArupaRule(BaseModel):   
  name: str = Field(max_length=64, pattern=r'^[A-Za-z0-9_-]*$')
  ip_proto: int = Field(gt=0, le=255)
  source_port: int = Field(gt=0, le=65536)
  source_subnet: InstanceOf[ipaddress.IPv4Network]

  @classmethod
  def create(cls, json_input: str):
    data = json.loads(json_input)    
    data['source_subnet'] = ipaddress.IPv4Network(data['source_subnet'])    

    return ArupaRule(**data)