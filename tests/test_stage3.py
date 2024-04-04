import json
import pytest
from claroty.rules import Rule, ArupaRule, FriscoRule
from claroty.stage3 import PolicyAPI


@pytest.fixture
def arupa_foo_json():
  return json.loads('{"name": "foo", "ip_proto": 1, "source_port": 2, "source_subnet": "192.168.1.0/24"}')


@pytest.fixture
def frisco_foo_json():  
  return json.loads('{"name": "foo", "ip_proto": 1, "source_port": 2, "source_ip": "192.168.1.0", "destination_ip": "192.168.1.1"}')


@pytest.fixture
def arupa_bar_json():
  return json.loads('{"name": "bar", "ip_proto": 1, "source_port": 2, "source_subnet": "192.168.1.0/24"}')


@pytest.fixture
def frisco_bar_json():  
  return json.loads('{"name": "bar", "ip_proto": 1, "source_port": 2, "source_ip": "192.168.1.0", "destination_ip": "192.168.1.1"}')


@pytest.fixture
def api():
  return PolicyAPI()


@pytest.fixture
def arupa_foo_policy_identifier(api):
  return api.create_policy(
    json.dumps(
      {
        "name": "foo",
        "description": "my foo policy",
        "type": "Arupa",
      }
    )
  )


@pytest.fixture
def frisco_foo_policy_identifier(api):
  return api.create_policy(
    json.dumps(
      {
        "name": "foo",
        "description": "my frisco policy",
        "type": "Frisco",
      }
    )
  )


@pytest.fixture
def arupa_bar_policy_identifier(api):
  return api.create_policy(
    json.dumps(
      {
        "name": "bar",
        "description": "my bar arupa policy",
        "type": "Arupa",
      }
    )
  )


@pytest.fixture
def frisco_bar_policy_identifier(api):
  return api.create_policy(
    json.dumps(
      {
        "name": "bar",
        "description": "my bar frisco policy",
        "type": "Frisco",
      }
    )
  )


class TestArupaRule:
  def test_rule_creation(self, arupa_foo_json):        
    r = Rule.create(json.dumps(arupa_foo_json))

    assert r.name == arupa_foo_json['name'], 'name should be foo but got {f.name}'
    assert r.ip_proto == arupa_foo_json['ip_proto']
    assert r.source_port == arupa_foo_json['source_port']
    assert str(r.source_subnet) == arupa_foo_json['source_subnet']
      

  def test_invalid_source_subnet(self, arupa_foo_json):
    arupa_foo_json["source_subnet"] = 'invalid'

    with pytest.raises(Exception):
      Rule.create(json.dumps(arupa_foo_json))


  def test_is_arupa_rule(self, arupa_foo_json):
    a: Rule = Rule.create(json.dumps(arupa_foo_json))
    assert a.isArupa()


  def test_is_frisco_rule(self, frisco_foo_json):
    f: Rule = Rule.create(json.dumps(frisco_foo_json))
    assert f.isFrisco()    


class TestFriscoRule:
  def test_rule_creation(self, frisco_foo_json):
    f = Rule.create(json.dumps(frisco_foo_json))

    assert f.name == frisco_foo_json['name'], 'name should be foo but got {f.name}'
    assert f.ip_proto == frisco_foo_json['ip_proto']
    assert f.source_port == frisco_foo_json['source_port']
    assert str(f.source_ip) == frisco_foo_json['source_ip']
    assert str(f.destination_ip) == frisco_foo_json['destination_ip']
      

  def test_invalid_source_subnet(self, frisco_foo_json):
    frisco_foo_json["source_ip"] = 'invalid'
    
    with pytest.raises(Exception):
      f = Rule.create(json.dumps(frisco_foo_json))


  def test_invalid_destination_subnet(self, frisco_foo_json):
    frisco_foo_json["destination_ip"] = 'invalid'
    
    with pytest.raises(Exception):
      f = Rule.create(json.dumps(frisco_foo_json))


class TestCreateRule:
  def test_create_arupa_rule(self, api, arupa_foo_policy_identifier, arupa_foo_json):
    rule_json = api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))
    rule: Rule = Rule.create(rule_json)

    assert rule.name == arupa_foo_json['name'], 'name should be foo but got {rule.name}'
    assert rule.ip_proto == arupa_foo_json['ip_proto']
    assert rule.source_port == arupa_foo_json['source_port']
    assert str(rule.source_subnet) == arupa_foo_json['source_subnet']


  def test_create_frisco_rule(self, api, frisco_foo_policy_identifier, frisco_foo_json):
    rule_json = api.create_rule(frisco_foo_policy_identifier, json.dumps(frisco_foo_json))
    rule: Rule = Rule.create(rule_json)

    assert rule.name == frisco_foo_json['name'], 'name should be foo but got {rule.name}'
    assert rule.ip_proto == frisco_foo_json['ip_proto']
    assert rule.source_port == frisco_foo_json['source_port']
    assert str(rule.source_ip) == frisco_foo_json['source_ip']
    assert str(rule.destination_ip) == frisco_foo_json['destination_ip']


class TestReadRule:  
  def test_read_arupa_rule(self, api: PolicyAPI, arupa_foo_policy_identifier, arupa_foo_json):
    api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))
    
    rules_json = json.loads(api.read_rule(json.dumps(arupa_foo_json)))
    assert len(rules_json) == 1
    assert rules_json[0] == arupa_foo_json


  def test_read_foo_bar_arupa_rule(self, api: PolicyAPI, arupa_foo_policy_identifier, arupa_foo_json, arupa_bar_json):
    api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))
    api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_bar_json))
    
    rules_json = json.loads(api.read_rule(json.dumps(arupa_foo_json)))
    assert len(rules_json) == 1
    assert rules_json[0] == arupa_foo_json


  def test_read_frisco_rule(self, api: PolicyAPI, frisco_foo_policy_identifier, frisco_foo_json):
    api.create_rule(frisco_foo_policy_identifier, json.dumps(frisco_foo_json))
    
    rule_json = json.loads(api.read_rule(json.dumps(frisco_foo_json)))    
    assert rule_json == frisco_foo_json


class TestUpdateRule:  
  def test_update_arupa_rule(self, api: PolicyAPI, arupa_foo_policy_identifier, arupa_foo_json):
    api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))

    arupa_foo_json['ip_proto'] = 5
    api.update_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))

    rules_json = json.loads(api.read_rule(json.dumps(arupa_foo_json)))    
    assert len(rules_json) == 1
    assert rules_json[0] == arupa_foo_json


  def test_update_frisco_rule(self, api: PolicyAPI, frisco_foo_policy_identifier, frisco_foo_json):
    api.create_rule(frisco_foo_policy_identifier, json.dumps(frisco_foo_json))

    frisco_foo_json['ip_proto'] = 6
    api.update_rule(frisco_foo_policy_identifier, json.dumps(frisco_foo_json))

    rule_json = json.loads(api.read_rule(json.dumps(frisco_foo_json)))        
    assert rule_json == frisco_foo_json


class TestDeleteRule:  
  def test_delete_arupa_rule(self, api: PolicyAPI, arupa_foo_policy_identifier, arupa_foo_json):
    api.create_rule(arupa_foo_policy_identifier, json.dumps(arupa_foo_json))    
    api.read_rule(json.dumps(arupa_foo_json))    

    api.delete_rule(json.dumps(arupa_foo_json))

    with pytest.raises(Exception):
      api.read_rule(json.dumps(arupa_foo_json))    


  def test_delete_frisco_rule(self, api: PolicyAPI, frisco_foo_policy_identifier, frisco_foo_json):
    api.create_rule(frisco_foo_policy_identifier, json.dumps(frisco_foo_json))    
    api.read_rule(json.dumps(frisco_foo_json))

    api.delete_rule(json.dumps(frisco_foo_json))

    with pytest.raises(Exception):
      api.read_rule(json.dumps(frisco_foo_json))    


class TestListRules:  
  