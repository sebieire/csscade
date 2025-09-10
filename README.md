# CSSCade 🎨

[![PyPI version](https://img.shields.io/pypi/v/csscade.svg)](https://pypi.org/project/csscade/)
[![Python Support](https://img.shields.io/pypi/pyversions/csscade.svg)](https://pypi.org/project/csscade/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent CSS merging and conflict resolution with two powerful systems**

CSSCade provides two complementary systems for CSS manipulation:

1. **CSSMerger** - Property-level CSS merging with multiple strategies
2. **Combinator** (v0.3.0) - Intelligent conflict detection for existing CSS frameworks

Perfect for theme customization, CSS framework overrides, runtime CSS manipulation, and CSS-in-JS implementations.

I was looking for something like this in the python ecosystem and couldn't find anything that matched my usecase so here it is. Enjoy!

## Features ✨

### Core Features
- **Intelligent Conflict Resolution**: Handle !important, shorthand properties, and duplicates
- **Pseudo-selector Support**: Full support for :hover, :focus, :before, :after, etc.
- **Media Query Support**: Responsive design support with @media rules
- **Production Ready**: Used in real-world applications for dynamic theming

### CSSMerger System
- **3 Merge Modes**: Permanent, Component, and Replace strategies
- **Multi-Rule Support**: Process all CSS rules including pseudo-selectors with `rule_selection='all'`
- **Selective Application**: Target specific rules with the `apply_to` parameter
- **Smart Property Merging**: Configurable shorthand strategies (cascade, smart, expand)
- **CSS Validation**: Optional property and value validation with helpful warnings
- **Flexible Naming**: Multiple class naming strategies (semantic, hash, sequential)

### Combinator System (v0.3.0)
- **Automatic Conflict Detection**: Analyzes existing CSS classes and finds conflicts
- **Framework Integration**: Works with Bootstrap, Tailwind, or any CSS framework
- **Smart Class Management**: Automatically determines which classes to keep/remove
- **Override Generation**: Creates optimized override CSS with minimal !important usage
- **Inline Fallback**: Generates React/JS-compatible inline styles
- **Batch Processing**: Efficiently process multiple elements

## Installation

```bash
pip install csscade
```

**Minimal Dependencies:** CSSCade has only ONE runtime dependency (`cssutils`) making it lightweight and fast to install!

## Quick Start 🚀

CSSCade offers two approaches depending on your needs:

### Method 1: CSSMerger - For Manual CSS Generation

```python
from csscade import CSSMerger

# Create a merger (defaults to 'component' mode)
merger = CSSMerger()

# Merge CSS
source_css = ".btn { color: red; padding: 10px; }"
overrides = {"color": "blue", "margin": "5px"}

result = merger.merge(source_css, overrides)

# Result structure:
print(result['css'])        # ['.csscade-btn-3f4a { color: blue; padding: 10px; margin: 5px; }']
print(result['add'])        # ['csscade-btn-3f4a']
print(result['preserve'])   # ['btn']
```

### Method 2: Combinator - For Working with Existing CSS Frameworks

```python
from csscade.combinator import Combinator

# Load your CSS framework
combinator = Combinator()
combinator.load_css(['bootstrap.css', 'custom.css'])

# Process an element with conflicts
result = combinator.process(
    element_classes=['btn', 'btn-primary', 'p-3'],
    overrides={
        'background': '#28a745',
        'padding': '2rem',
        ':hover': {
            'background': '#218838'
        }
    },
    element_id='my_button'
)

# Result structure:
print(result['remove_classes'])  # ['btn-primary', 'p-3'] - conflicting classes
print(result['keep_classes'])    # ['btn'] - non-conflicting classes  
print(result['add_classes'])     # ['csso-my_button'] - generated override class
print(result['generated_css'])   # Complete CSS with !important only where needed
print(result['fallback_inline']) # {'background': '#28a745', 'padding': '2rem'}
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

## Combinator System (v0.3.0)

The Combinator system automatically detects conflicts between existing CSS classes and your desired style overrides, intelligently managing which classes to keep, remove, or add.

### When to Use Combinator vs CSSMerger

**Use Combinator when:**
- Working with existing CSS frameworks (Bootstrap, Tailwind, etc.)
- You need automatic conflict detection
- Managing class lists on existing elements
- You want to minimize !important usage

**Use CSSMerger when:**
- Generating CSS from scratch
- You need fine-grained control over merge strategies
- Building CSS programmatically
- Working with CSS strings rather than class lists

### Basic Combinator Usage

```python
from csscade.combinator import Combinator

# Step 1: Load your CSS
combinator = Combinator()
combinator.load_css(['bootstrap.css', 'theme.css'])  # Can be files
or
combinator.load_css(['{...valid css string...}'])  # CSS strings

# Step 2: Process an element
result = combinator.process(
    element_classes=['col-lg-6', 'bg-primary', 'p-3', 'text-white'],
    overrides={
        'background': 'linear-gradient(to right, #667eea, #764ba2)',
        'padding': '2rem',
        'margin': '1rem'
    },
    element_id='hero_section'
)

# Step 3: Use the results
print(result['remove_classes'])  # ['bg-primary', 'p-3'] - have conflicts
print(result['keep_classes'])    # ['col-lg-6', 'text-white'] - no conflicts
print(result['add_classes'])     # ['csso-hero_section'] - new override class
```

### Combinator with Pseudo-selectors and Media Queries

```python
result = combinator.process(
    element_classes=['btn', 'btn-primary'],
    overrides={
        'background': '#28a745',
        'padding': '1rem 2rem',
        ':hover': {
            'background': '#218838',
            'transform': 'scale(1.05)'
        },
        ':focus': {
            'outline': '3px solid #ffc107'
        },
        '@media (min-width: 768px)': {
            'padding': '1.5rem 3rem',
            'font-size': '1.25rem'
        }
    },
    element_id='cta_button'
)

# Generated CSS includes:
# - Base styles with !important only for conflicting properties
# - Hover and focus states
# - Media query for responsive design
print(result['generated_css'])
```

### Processing HTML Elements Directly

```python
# You can also process HTML strings directly
html = '<div class="card shadow p-4 mt-3">Content</div>'

result = combinator.process_element(
    html=html,
    overrides={
        'background': '#f8f9fa',
        'padding': '2rem',
        'margin-top': '2rem'
    },
    element_id='custom_card'
)
```

### Batch Processing Multiple Elements

```python
# Process multiple elements efficiently
elements = [
    {
        'element_classes': ['btn', 'btn-primary'],
        'overrides': {'background': '#28a745'},
        'element_id': 'btn1'
    },
    {
        'element_classes': ['card', 'p-3'],
        'overrides': {'padding': '2rem'},
        'element_id': 'card1'
    }
]

results = combinator.process_batch(elements)
```

### Understanding Conflict Detection

The Combinator uses intelligent conflict detection that understands CSS property relationships:

```python
# Example: Shorthand vs Longhand conflicts
result = combinator.process(
    element_classes=['p-3', 'pt-2', 'border', 'rounded'],
    overrides={
        'padding-top': '3rem',    # Conflicts with both p-3 and pt-2
        'border-color': '#ff0000'  # Conflicts with border shorthand
    },
    element_id='test'
)

# Result:
# - Removes: ['p-3', 'pt-2', 'border'] (all have conflicts)
# - Keeps: ['rounded'] (border-radius is independent)
```

### Complete Combinator Example

```python
from csscade.combinator import Combinator

# Load CSS from your framework
combinator = Combinator()
combinator.load_css([
    'path/to/bootstrap.min.css',
    'path/to/custom-theme.css'
])

# Define your element and overrides
element_classes = [
    'container-fluid', 'row', 'col-lg-6',
    'bg-gradient-primary', 'shadow-lg',
    'text-white', 'p-5', 'rounded-lg'
]

style_overrides = {
    # Regular properties
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'padding': '3rem',
    'box-shadow': '0 20px 40px rgba(0,0,0,0.1)',
    
    # Pseudo-selectors
    ':hover': {
        'transform': 'translateY(-5px)',
        'box-shadow': '0 25px 50px rgba(0,0,0,0.15)'
    },
    
    # Media queries
    '@media (min-width: 992px)': {
        'padding': '5rem',
        'font-size': '1.25rem'
    }
}

# Process the element
result = combinator.process(
    element_classes=element_classes,
    overrides=style_overrides,
    element_id='hero_block'
)

# Apply the results to your HTML
print(f"Remove these classes: {result['remove_classes']}")
print(f"Keep these classes: {result['keep_classes']}")
print(f"Add this class: {result['add_classes'][0]}")

# Inject the generated CSS
print(f"<style>\n{result['generated_css']}\n</style>")

# Or use inline styles as fallback (excludes pseudo-selectors and media queries)
print(f"Inline fallback: {result['fallback_inline']}")
```

### Combinator API Reference

#### Constructor
```python
combinator = Combinator()
```

#### Methods

**`load_css(css_sources)`**
- Load CSS files or strings for analysis
- `css_sources`: List of file paths or CSS strings

**`process(element_classes, overrides, element_id)`**
- Process style overrides for given classes
- `element_classes`: List of CSS class names
- `overrides`: Dictionary of CSS properties (supports pseudo-selectors and media queries)
- `element_id`: Unique identifier for generating class names
- Returns: Dictionary with conflict analysis and generated CSS

**`process_element(html, overrides, element_id)`**
- Process an HTML element string
- Automatically extracts classes from HTML

**`process_batch(elements)`**
- Process multiple elements efficiently
- `elements`: List of dictionaries with element configurations

**`clear_cache()`**
- Clear loaded CSS cache

### Result Dictionary Structure

```python
{
    'remove_classes': [],     # Classes that conflict with overrides
    'keep_classes': [],       # Classes without conflicts
    'add_classes': [],        # Generated override class name(s)
    'generated_css': '',      # Complete CSS with override rules
    'fallback_inline': {},    # Inline styles (camelCase, no pseudo/media)
    'conflicts_found': []     # Detailed conflict descriptions
}
```

## CSSMerger System

### CSSMerger Merge Modes

#### 1. Permanent Mode
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

#### 2. Component Mode (Default)
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

#### 3. Replace Mode
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

## CSSMerger Apply To Parameter (Selective Override)

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

**Special Keywords:**
- `'all'` - Apply to all rules (default)
- `'base'` - Apply to base rule only (no pseudo-selectors)
- `'states'` - Apply only to pseudo-class selectors (all states)

**Wildcards:**
- `'*'` - Apply to all rules (same as 'all')
- `'.*'` - Apply to all base classes (no pseudo-selectors)
- `'*:hover'` - Apply to all rules with :hover pseudo-class
- `'*:active'` - Apply to all rules with :active pseudo-class
- `'*:focus'` - Apply to all rules with :focus pseudo-class

**Specific Selectors:**
- `['.btn']` - Apply to specific class (base rule only)
- `['.btn:hover']` - Apply to specific class with pseudo-selector
- `[':hover']` - Apply to any rule with :hover pseudo-class
- `[':active']` - Apply to any rule with :active pseudo-class
- `[':focus']` - Apply to any rule with :focus pseudo-class

**Multiple Targets:**
- `[':hover', ':active']` - Apply to multiple pseudo-selectors
- `['.btn', '.btn:hover']` - Apply to specific class and its hover state
- `['base', ':active']` - Apply to base rules and :active states

## CSSMerger Conflict Resolution

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

## CSSMerger Naming Configuration

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

## CSSMerger Validation Configuration

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

## CSSMerger Complete Configuration Examples 🎯

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

## Advanced CSSMerger Usage 🔧

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

## CSSMerger Result Dictionary Structure

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

## CSSMerger API Reference

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