class PolicyAPI: 
  def create_policy(self, json_input: str) -> str:
    pass

  def read_policy(self, json_identifier: str) -> str:
    pass

  def update_policy(self, json_identifier: str, json_input: str) -> None:
      raise NotImplementedError


  def delete_policy(self, json_identifier: str) -> None:
      raise NotImplementedError


  def list_policies(self) -> str:
      raise NotImplementedError
