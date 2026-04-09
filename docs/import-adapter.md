# Import adapter guide

Implemented:
- Generic adapter protocol (`ImportAdapter`)
- Import orchestration service (`run_import`)
- Sample fixture adapter (`SampleFixtureAdapter`)

Not implemented:
- Real legacy DB adapter. `LegacyDbAdapter` is a deliberate placeholder pending schema + sample dump.

To add real adapter:
1. Implement `iter_records()` in `LegacyDbAdapter`.
2. Map schema fields into `ImportRecord`.
3. Add integration tests with real fixtures.
