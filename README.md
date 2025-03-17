# ip-xact-ai-generator
AI-powered system for generating valid IP-XACT components using LLMs and reinforcement learning.

# Questions to ask from mentors (Week 1-2)
- What would be the ideal output? User enter's an input and get the HW component?
- How many data do we need?
- any idea how to integrate the validation? (from CMD?)
# Questions to ask from mentors (Week 2-3)
- Can we use other verification tools? (Kaktus2 does not provide CLI or api to use.

# Notes for the team
- To use verification please go to validation folder then run command:
  ```
  python validate_ipxact.py "../test_samples/valid_component.xml"
  python validate_ipxact.py "../test_samples/invalid_component.xml"
  ```

## Validation Instructions
1. The first time you run validation, the script will download all necessary IP-XACT schema files
2. Valid components should show a success message
3. Invalid components will display detailed validation errors
4. The schema files are stored in the `ipxact_schema` directory