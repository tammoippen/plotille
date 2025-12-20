# Float Normalization Refactor - Summary

## What Changed

This refactor simplified the type system by normalizing all input data
(datetime and numeric) to `float` immediately upon entry to the system.

### Before
- Data stored as `DataValue = Real | DatetimeLike` throughout
- Type unions propagated through the codebase
- 26+ mypy type errors
- Datetime conversion happened in multiple places

### After
- Data normalized to `float` in Plot/Text/Histogram constructors
- Original type tracked with `DataMetadata` objects
- 0 mypy errors
- Datetime conversion centralized in one place (InputFormatter)

## Files Changed

### New Files
- `plotille/_data_metadata.py` - Tracks original data types
- `tests/test_data_metadata.py` - Tests for metadata tracking

### Modified Files
- `plotille/_util.py` - Updated `hist()` to accept normalized floats
- `plotille/_figure_data.py` - Normalize data in Plot, Text, Histogram
- `plotille/_figure.py` - Simplified limits and axis methods
- `tests/test_plot.py` - Added integration tests
- `tests/test_histogram.py` - Added normalization tests

## API Compatibility

**Public API unchanged** - Users can still pass datetime or numeric values
to `plot()`, `scatter()`, `histogram()`, and `text()` methods.

**Internal changes only** - All internal operations now use `float`.

## Type Safety Improvements

- Before: 26 mypy errors
- After: 0 mypy errors
- Clearer type signatures throughout
- Better IDE autocomplete and type checking

## Performance Impact

Neutral to slight improvement:
- Conversion happens once (in constructor) instead of repeatedly
- Simpler code paths (no type checking in hot paths)
- Slightly more memory (storing both original and normalized data)

## Testing

All existing tests pass. New tests added:
- DataMetadata functionality
- Plot/Text/Histogram normalization
- Integration tests for datetime and numeric plotting

## Migration Guide for Contributors

When adding new plot types or modifying data handling:

1. Accept `DataValues` in public API (for compatibility)
2. Normalize to `float` immediately using `InputFormatter.convert()`
3. Track original type with `DataMetadata.from_sequence()`
4. Work with `list[float]` or `Sequence[float]` internally
5. Use metadata for display formatting (if needed)

Example pattern:
```python
def __init__(self, X: DataValues, Y: DataValues):
    self.X = X  # Keep original for compatibility
    self.Y = Y

    # Normalize
    self._formatter = InputFormatter()
    self.X_metadata = DataMetadata.from_sequence(X)
    self.Y_metadata = DataMetadata.from_sequence(Y)
    self.X_normalized = [self._formatter.convert(x) for x in X]
    self.Y_normalized = [self._formatter.convert(y) for y in Y]

def width_vals(self) -> list[float]:
    return self.X_normalized  # Return normalized
```
