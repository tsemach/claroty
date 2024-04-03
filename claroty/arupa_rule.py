# import json
# import ipaddress
# from pydantic import BaseModel, Field, InstanceOf
# from abc import ABC


# class ArupaRule(Rule, BaseModel):   
#   name: str = Field(max_length=64, pattern=r'^[A-Za-z0-9_-]*$')
#   ip_proto: int = Field(gt=0, le=255)
#   source_port: int = Field(gt=0, le=65536)
#   source_subnet: InstanceOf[ipaddress.IPv4Network]

#   @classmethod
#   def create(cls, json_input: str):
#     data = json.loads(json_input)    
#     data['source_subnet'] = ipaddress.IPv4Network(data['source_subnet'])    

#     return ArupaRule(**data)
  
# # foo = '{"name": "foo", "ip_proto": 1, "source_port": 2, "source_subnet": "192.168.1.0/24"}'
# foo = '{"name": "foo", "ip_proto": 1, "source_port": 2, "source_subnet": "192.168.1.0/24"}'
# f = ArupaRule.create(foo)
# print('f:', f)

# def print_rule(rule: Rule):
#   print('print_rule:', rule.name)
#   print('print_rule:', rule)
#   print(rule.isArupaRule())
#   print(rule.isFriscoRule())

# print_rule(f)  

