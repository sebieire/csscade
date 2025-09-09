# CSSCade 🎨

[![PyPI version](https://badge.fury.io/py/csscade.svg)](https://pypi.org/project/csscade/)
[![Python Support](https://img.shields.io/pypi/pyversions/csscade.svg)](https://pypi.org/project/csscade/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent CSS merging with conflict resolution and multiple strategies**

CSSCade is a Python library that intelligently merges CSS properties from different sources, handling conflicts, preserving specificity, and supporting various merge strategies. Perfect for theme customization, runtime CSS manipulation, and CSS-in-JS implementations.

## Features ✨

- **3 Merge Modes**: Permanent, Component, and Replace strategies
- **Multi-Rule Support**: Process all CSS rules including pseudo-selectors with `rule_selection='all'`
- **Selective Application**: Target specific rules with the `apply_to` parameter
- **Intelligent Conflict Resolution**: Handle !important, shorthand properties, and duplicates
- **Smart Property Merging**: Configurable shorthand strategies (cascade, smart, expand)
- **CSS Validation**: Optional property and value validation with helpful warnings
- **Flexible Naming**: Multiple class naming strategies (semantic, hash, sequential)
- **Production Ready**: Used in real-world applications for dynamic theming

## Installation

```bash
pip install csscade
```

**Minimal Dependencies:** CSSCade has only ONE runtime dependency (`cssutils`) making it lightweight and fast to install!

## Quick Start 🚀

### Basic Usage

```python
from csscade import CSSMerger

# Create a merger (defaults to 'component' mode)
merger = CSSMerger()

# Merge CSS
source_css = ".btn { color: red; padding: 10px; }"
overrides = {"color": "blue", "margin": "5px"}

result = merger.merge(source_css, overrides)

# Result structure (all fields always present):
print(result['css'])        # List of generated CSS strings
print(result['add'])        # Classes to add: ['csscade-btn-xxxx']
print(result['remove'])     # Classes to remove: []
print(result['preserve'])   # Classes to keep: ['btn']
print(result['warnings'])   # Any warnings: []
print(result['info'])       # Informational messages: []
```

**Output:**
```python
{
    'css': ['.csscade-btn-3f4a { color: blue; padding: 10px; margin: 5px; }'],
    'add': ['csscade-btn-3f4a'],
    'remove': [],
    'preserve': ['btn'],
    'warnings': [],
    'info': ['Created override class .csscade-btn-3f4a with merged properties']
}
```

### Multi-Rule Support

Process multiple CSS rules including pseudo-selectors:

```python
# Process only first CSS rule/class (default)
merger = CSSMerger(rule_selection='first')
result = merger.merge(
    ".btn { color: red; } .btn:hover { color: darkred; }",
    {"background": "blue"}
)
# Only .btn is processed, warning about ignored rules

# Process ALL rules including pseudo-selectors
merger = CSSMerger(rule_selection='all')
result = merger.merge(
    ".btn { color: red; } .btn:hover { color: darkred; }",
    {"background": "blue"}
)
# Both .btn and .btn:hover get background: blue
```

## Merge Modes

### 1. Permanent Mode
**Directly modifies the original CSS rule. Best for build-time CSS generation.**

```python
merger = CSSMerger(mode='permanent')  # Required parameter

result = merger.merge(
    ".card { color: red; padding: 10px; }",
    {"color": "blue", "margin": "20px"}
)

# Output:
print(result['css'][0])
# .card {
#   color: blue;      /* Changed */
#   padding: 10px;    /* Preserved */
#   margin: 20px;     /* Added */
# }

# Usage: Apply the modified CSS directly
# No class changes needed
```

### 2. Component Mode (Default)
**Creates an override class while preserving the original. Perfect for theming systems.**

```python
merger = CSSMerger(mode='component')  # Optional (this is default)

result = merger.merge(
    ".btn { color: red; padding: 10px; }",
    {"color": "blue", "margin": "5px"}
)

# Output:
print(result['css'][0])
# .csscade-btn-3f4a {
#   color: blue;
#   padding: 10px;
#   margin: 5px;
# }

print(result['add'])       # ['csscade-btn-3f4a']
print(result['preserve'])  # ['btn']

# Usage: element.className = "btn csscade-btn-3f4a"
```

### 3. Replace Mode
**Creates a complete replacement class. Best for total style replacement.**

```python
merger = CSSMerger(mode='replace')  # Required parameter

result = merger.merge(
    ".old-style { color: red; padding: 10px; }",
    {"color": "blue", "margin": "5px"}
)

# Output:
print(result['css'][0])
# .csscade-8d2f {
#   color: blue;
#   padding: 10px;
#   margin: 5px;
# }

print(result['add'])     # ['csscade-8d2f']
print(result['remove'])  # ['old-style']

# Usage: element.className = "csscade-8d2f"
```

## Apply To Parameter (Selective Override)

The `apply_to` parameter lets you target specific rules when using `rule_selection='all'`.

### Basic Example

```python
merger = CSSMerger(rule_selection='all')

source = """
.btn { background: blue; color: white; }
.btn:hover { background: darkblue; }
"""

# Apply to all rules (default)
result = merger.merge(source, {"border": "2px solid red"}, apply_to='all')
# Both .btn and .btn:hover get the border

# Apply to base rule only
result = merger.merge(source, {"border": "2px solid red"}, apply_to='base')
# Only .btn gets the border, .btn:hover remains unchanged

# Apply to specific pseudo-selector
result = merger.merge(source, {"border": "2px solid red"}, apply_to=[':hover'])
# Only .btn:hover gets the border
```

### Advanced Example with Multiple Targets

```python
source = """
.btn { background: blue; }
.btn:hover { background: darkblue; }
.btn:active { background: navy; }
.btn:focus { outline: none; }
"""

# Target multiple specific states
result = merger.merge(
    source,
    {"box-shadow": "0 2px 4px rgba(0,0,0,0.2)"},
    apply_to=[':hover', ':focus']
)
# Only :hover and :focus states get the box-shadow
```

### Available Apply To Options

- `'all'` - Apply to all rules (default)
- `'base'` - Apply to base rule only (no pseudo-selectors)
- `[':hover']` - Apply to specific pseudo-selector
- `[':hover', ':active']` - Apply to multiple pseudo-selectors
- `['.btn']` - Apply to specific class
- `['.btn:hover']` - Apply to specific class with pseudo-selector

## Conflict Resolution

### !important Handling

CSSCade provides 5 strategies for handling !important declarations:

```python
# 'match' strategy (default) - Add !important if original had it
merger = CSSMerger(conflict_resolution={'important': 'match'})
result = merger.merge(
    ".text { color: blue !important; }",
    {"color": "red"}
)
# Output: .text { color: red !important; }

# 'respect' strategy - Never override !important
merger = CSSMerger(conflict_resolution={'important': 'respect'})
result = merger.merge(
    ".text { color: blue !important; }",
    {"color": "red"}
)
# Output: .text { color: blue !important; }  # Original preserved

# Other strategies:
# 'override': Override but don't add !important
# 'force': Always add !important to overrides
# 'strip': Remove all !important declarations
```

### Shorthand Properties

CSSCade offers three strategies for handling shorthand properties:

#### 1. Cascade Strategy (Default)
**Simple CSS cascade - later properties override**

```python
merger = CSSMerger(shorthand_strategy='cascade')
result = merger.merge(
    ".box { margin: 10px; padding: 20px; }",
    {"margin-top": "30px", "padding": "15px"}
)
# Output: .box {
#   margin: 10px;
#   padding: 15px;      /* Fully replaced */
#   margin-top: 30px;   /* Cascades over margin */
# }
```

#### 2. Smart Strategy
**Intelligent merging for margin/padding, cascade for complex properties**

```python
merger = CSSMerger(shorthand_strategy='smart')
result = merger.merge(
    ".box { margin: 10px; padding: 20px; }",
    {"margin-top": "30px", "padding": "15px"}
)
# Output: .box {
#   margin: 30px 10px 10px;  /* Smart merge: top changed, others preserved */
#   padding: 15px;           /* Fully replaced */
# }
```

#### 3. Expand Strategy
**Full expansion of all shorthands**

```python
merger = CSSMerger(shorthand_strategy='expand')
result = merger.merge(
    ".box { border: 1px solid red; }",
    {"border-width": "3px"}
)
# Output: .box {
#   border-top-width: 3px;
#   border-right-width: 3px;
#   border-bottom-width: 3px;
#   border-left-width: 3px;
#   border-top-style: solid;
#   border-right-style: solid;
#   /* ... all properties expanded ... */
# }
```

## Naming Configuration

Control how override classes are generated:

```python
# Semantic naming (default) - Readable class names
merger = CSSMerger(naming={
    'strategy': 'semantic',  # my-btn-3f4a
    'prefix': 'my-',
    'suffix': '-override'
})
# Output: my-btn-3f4a-override

# Hash naming - Content-based unique identifiers
merger = CSSMerger(naming={
    'strategy': 'hash',      # css-7a9f2c
    'hash_length': 6
})
# Output: css-7a9f2c (same content = same hash)

# Sequential naming - Simple counters
merger = CSSMerger(naming={
    'strategy': 'sequential'  # style-1, style-2, style-3
})
# Output: style-1
```

**Default naming configuration:**
```python
{
    'strategy': 'semantic',    # Readable names
    'prefix': 'csscade-',      # Default prefix
    'suffix': '',              # No suffix by default
    'hash_length': 8           # For hash strategy
}
```

## Validation Configuration

Catch CSS errors and typos with optional validation:

```python
# Development - Helpful warnings
merger = CSSMerger(validation={
    'enabled': True,
    'check_values': True  # Validate color values, units, etc.
})

result = merger.merge(
    ".card { padding: 10px; }",
    {
        "fake-property": "value",     # Unknown property
        "color": "not-a-color",       # Invalid value
        "margin": "10px",
        "margin-top": "20px"          # Duplicate warning
    }
)
# Warnings: [
#   "Unknown CSS property: 'fake-property'",
#   "Invalid color value: 'not-a-color'",
#   "Potential duplicate: 'margin-top'"
# ]

# Production - Strict validation (throws errors)
merger = CSSMerger(validation={
    'enabled': True,
    'strict': True  # Raises exception on invalid CSS
})

# Minimal - Just enable validation
merger = CSSMerger(validation={'enabled': True})
```

**Default validation configuration:**
```python
{
    'enabled': False,         # Off by default (backwards compatible)
    'strict': False,          # Warnings, not errors
    'check_properties': True, # Check property names when enabled
    'check_values': False,    # Don't check values by default (expensive)
    'allow_vendor': True,     # Allow -webkit-, -moz-, etc.
    'allow_custom': True,     # Allow --css-variables
    'check_duplicates': True  # Warn about duplicate properties
}
```

## Complete Configuration Examples 🎯

### Production Configuration

```python
merger = CSSMerger(
    mode='component',
    rule_selection='all',
    naming={
        'strategy': 'semantic',
        'prefix': 'app-',
        'suffix': ''
    },
    conflict_resolution={
        'important': 'match'
    },
    shorthand_strategy='smart',
    validation={
        'enabled': True,
        'strict': False,
        'check_properties': True
    }
)
```

### Development Configuration

```python
merger = CSSMerger(
    mode='component',
    rule_selection='all',
    naming={'strategy': 'sequential', 'prefix': 'dev-'},
    validation={
        'enabled': True,
        'check_values': True,
        'strict': False
    },
    shorthand_strategy='expand',  # See all properties
    debug=True
)
```

## Advanced Usage 🔧

### Real-World Example: Bootstrap Customization

Customize Bootstrap components while preserving all states:

```python
merger = CSSMerger(
    mode='component',
    rule_selection='all',
    shorthand_strategy='smart'
)

bootstrap_button = """
.btn-primary {
    background: #007bff;
    color: white;
    padding: 0.375rem 0.75rem;
    border: 1px solid #007bff;
}
.btn-primary:hover {
    background: #0056b3;
    border-color: #004085;
}
.btn-primary:active {
    background: #004085;
}
"""

brand_overrides = {
    "background": "#28a745",     # Green instead of blue
    "border-color": "#28a745",
    "font-weight": "bold"
}

result = merger.merge(bootstrap_button, brand_overrides, apply_to='all')

# Output:
# .app-btn-primary-x1a3 { 
#     background: #28a745; 
#     color: white;
#     padding: 0.375rem 0.75rem;
#     border-color: #28a745;
#     font-weight: bold;
# }
# .app-btn-primary-x1a3:hover {
#     background: #28a745;
#     border-color: #28a745;
#     font-weight: bold;
# }
# .app-btn-primary-x1a3:active {
#     background: #28a745;
#     border-color: #28a745;
#     font-weight: bold;
# }

# Usage: <button class="btn-primary app-btn-primary-x1a3">
```

### Runtime CSS Manipulation (Inline Styling)

Generate inline styles for dynamic theming:

```python
merger = CSSMerger(mode='permanent')

# User's theme preferences
user_theme = {
    "primary-color": "#FF5722",
    "font-size": "18px"
}

# Generate inline styles
result = merger.merge(
    "body { color: #333; font-size: 16px; }",
    user_theme
)

# Apply dynamically
element.style.cssText = result['css'][0]
```

### Batch Operations

Process multiple CSS operations efficiently:

```python
merger = CSSMerger(mode='component')
batch = merger.batch()

# Queue multiple operations
batch.add(".header { color: black; }", {"background": "white"})
batch.add(".footer { padding: 20px; }", {"border-top": "1px solid gray"})
batch.add(".sidebar { width: 200px; }", {"background": "#f5f5f5"})

# Execute all at once
results = batch.execute()

for i, result in enumerate(results):
    print(f"Operation {i+1}: {result['add']}")
```

## Result Dictionary Structure

All merge operations return a consistent structure:

```python
{
    'css': [],        # List of generated CSS strings (always list)
    'add': [],        # Classes to add to element (always list)
    'remove': [],     # Classes to remove from element (always list)
    'preserve': [],   # Original classes to keep (always list)
    'warnings': [],   # Validation/conflict warnings (always list)
    'info': []        # Informational messages (always list)
}
```

## API Reference

### CSSMerger Constructor

```python
CSSMerger(
    mode='component',              # 'permanent'|'component'|'replace'
    rule_selection='first',        # 'first'|'all'
    naming={                       # Class naming configuration
        'strategy': 'semantic',    # 'semantic'|'hash'|'sequential'
        'prefix': 'csscade-',
        'suffix': '',
        'hash_length': 8
    },
    conflict_resolution={          # Conflict handling
        'important': 'match'       # 'match'|'respect'|'override'|'force'|'strip'
    },
    shorthand_strategy='cascade',  # 'cascade'|'smart'|'expand'
    validation={                   # CSS validation
        'enabled': False,
        'strict': False,
        'check_properties': True,
        'check_values': False,
        'allow_vendor': True,
        'allow_custom': True,
        'check_duplicates': True
    },
    debug=False                    # Enable debug output
)
```

### merge() Method

```python
result = merger.merge(
    source,          # CSS string, rule, or properties dict
    override,        # Properties dict or CSS string
    component_id=None,  # Optional unique identifier
    apply_to='all'   # Which rules to apply overrides to
)
```

## Default Values Reference

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `mode` | `'component'` | Merge strategy |
| `rule_selection` | `'first'` | Process first CSS rule/class only |
| `shorthand_strategy` | `'cascade'` | Simple CSS cascade |
| `naming.strategy` | `'semantic'` | Readable class names |
| `naming.prefix` | `'csscade-'` | Class name prefix |
| `validation.enabled` | `False` | Validation off by default |
| `conflict_resolution.important` | `'match'` | Match original !important |

## Testing

Run the comprehensive test suite:

```bash
# Basic test
python _test_comprehensive.py

# Run all tests
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- [PyPI Package](https://pypi.org/project/csscade/)
- [GitHub Repository](https://github.com/yourusername/csscade)
- [Issue Tracker](https://github.com/yourusername/csscade/issues)