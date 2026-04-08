# Import adapter guide

## Implemented
- `imports.adapters.base.LegacyAdapter` protocol
- `imports.adapters.sample.FixtureSampleAdapter`
- `imports.services.run_import` generic orchestration

## Real legacy adapter (blocked)
Implement in a new module under `imports/adapters/real_legacy.py` once schema and fixtures are available.

Required output contract per record:
- external_id
- full_name
- company
- position
- image_path or image blob handling
- raw XML payload
- optional email/phone

The current placeholder class intentionally fails fast to avoid claiming unsupported compatibility.
