# import json
# import ipaddress
# from pydantic import BaseModel, Field, InstanceOf

# class FriscoRule(BaseModel):   
#   name: str = Field(max_length=64, pattern=r'^[A-Za-z0-9_-]*$')
#   ip_proto: int = Field(gt=0, le=255)
#   source_ip: int = InstanceOf[ipaddress.IPv4Address]
#   destination_ip: InstanceOf[ipaddress.IPv4Address]
  

#   @classmethod
#   def create(cls, json_input: str):
#     data = json.loads(json_input)    
#     data['source_ip'] = ipaddress.IPv4Address(data['source_ip'])
#     data['destination_ip'] = ipaddress.IPv4Address(data['destination_ip'])        

#     return FriscoRule(**data)