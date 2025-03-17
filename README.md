# ip-xact-ai-generator
AI-powered system for generating valid IP-XACT components using LLMs and reinforcement learning.

# Questions to ask from mentors (Week 1-2)
- What would be the ideal output? User enter's an input and get the HW component?
- How many data do we need?
- any idea how to integrate the validation? (from CMD?)
# Questions to ask from mentors (Week 2-3)
- Can we use other verification tools? (Kaktus2 does not provide CLI or api to use.)

# Notes for the team
- To use verification please go to validation folder then run command:
  ```
  python simple_validator.py "../test_samples/minimal_valid_component.xml"
  python simple_validator.py "../test_samples/valid_component.xml"
  python simple_validator.py "../test_samples/invalid_component.xml"
  ```

## Validation Instructions
1. Make sure you have the required packages installed:
   ```
   pip install xmlschema
   ```

2. The `simple_validator.py` script validates IP-XACT components:
   - It performs schema validation with fallback to content validation
   - It provides detailed error messages for schema violations
   - It works with all versions of xmlschema package

3. Sample validation output:
   - Valid components will show: ✅ Success: XML validates against schema
   - Invalid components will show details about schema violations