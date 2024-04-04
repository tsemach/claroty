# Claroty Home Assignment

## Stage 2 Assumptions

- Arupa policy are unique by name there is store as a dictionary 
- Frisco policy are store as a list

### Update Rules (Assumptions)

  1. if both are Arupa => replace the new one with the old one
  2. if currnet is Arupa and new is Firsco => remove from Arupa and add to Firsco 
  3. if currnet is Frisco and new is Arupa => replace all Firsco with Arupa
  4. if both Fisco => update all fields of current with the fields of new one

  #### constraines: 
    A. since this is update policy must be exist otherwise it is an error
    B. name of identifier must be equal to name of the input

  ## Stage 3 Assumptions
  > All policies requirements / rules from stage-2 are apply also in stage-3

  - Arupa rule are store in a list which is accessible by policy name
  - Fristor rules are globaly store in a dictionary access by rule name
  - `read_rule`: if rule is arupa then return all rules matching the rule name
  - `delete_rule`: if rule is arupa the delete all rules matching the rule name
  > the above assumptions are made cause read_rule and delete_rule apis are not specify 
    to which policy they are refer to. So Changing the API is much more dramatic approch with far more seriose consequences then assuming those assumptions

  

