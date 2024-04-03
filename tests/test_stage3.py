import json
import pytest
from claroty.rules import Rule, ArupaRule, FriscoRule
from claroty.stage3 import PolicyAPI


@pytest.fixture
def arupa_json():
  return json.loads('{"name": "foo", "ip_proto": 1, "source_port": 2, "source_subnet": "192.168.1.0/24"}')


@pytest.fixture
def frisco_json():  
  return json.loads('{"name": "foo", "ip_proto": 1, "source_port": 2, "source_ip": "192.168.1.0", "destination_ip": "192.168.1.1"}')


class TestArupaRule:
  def test_rule_creation(self, arupa_json):        
    f = Rule.create(json.dumps(arupa_json))

    assert f.name == arupa_json['name'], 'name should be foo but got {f.name}'
    assert f.ip_proto == arupa_json['ip_proto']
    assert f.source_port == arupa_json['source_port']
    assert str(f.source_subnet) == arupa_json['source_subnet']
      

  def test_invalid_source_subnet(self, arupa_json):
    arupa_json["source_subnet"] = 'invalid'

    with pytest.raises(Exception):
      f = Rule.create(json.dumps(arupa_json))


  def test_is_arupa_rule(self, arupa_json):
    f: Rule = Rule.create(json.dumps(arupa_json))
    assert f.isArupa()


  def test_is_frisco_rule(self, frisco_json):
    f: Rule = Rule.create(json.dumps(frisco_json))
    assert f.isFrisco()    


class TestFriscoRule:
  def test_rule_creation(self, frisco_json):
    f = Rule.create(json.dumps(frisco_json))

    assert f.name == frisco_json['name'], 'name should be foo but got {f.name}'
    assert f.ip_proto == frisco_json['ip_proto']
    assert f.source_port == frisco_json['source_port']
    assert str(f.source_ip) == frisco_json['source_ip']
    assert str(f.destination_ip) == frisco_json['destination_ip']
      

  def test_invalid_source_subnet(self, frisco_json):
    frisco_json["source_ip"] = 'invalid'
    
    with pytest.raises(Exception):
      f = Rule.create(json.dumps(frisco_json))


  def test_invalid_destination_subnet(self, frisco_json):
    frisco_json["destination_ip"] = 'invalid'
    
    with pytest.raises(Exception):
      f = Rule.create(json.dumps(frisco_json))
