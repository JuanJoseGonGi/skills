# Python Type Safety Details

This file explains detailed guidelines for type safety in Python.

## 📋 Table of Contents

- [Absolute Prohibition of the Any Type](#absolute-prohibition-of-the-any-type)
- [Correct Type Hinting Methods](#correct-type-hinting-methods)
- [Python Best Practices](#python-best-practices)
- [Utilizing TypedDict](#utilizing-typeddict)
- [Utilizing Protocol](#utilizing-protocol)
- [Utilizing dataclass](#utilizing-dataclass)
- [Using Type Checkers](#using-type-checkers)

## 🚫 Absolute Prohibition of the Any Type

### ❌ Patterns that Must Never Be Used

#### Pattern 1: Direct Use of the Any Type

```python
# ❌ Bad Example
from typing import Any

def process_data(data: Any) -> Any:
    return data.get('value')  # Type safety is lost

result: Any = fetch_data()  # Type checking is disabled
```

**Problems**:
- Python's type checking is completely disabled.
- Becomes a source of runtime errors.
- IDE autocompletion does not work.
- Makes refactoring difficult.

#### Pattern 2: Use of bare `except`

```python
# ❌ Bad Example
try:
    result = risky_operation()
except:  # Catches all exceptions (equivalent to Any type)
    pass
```

**Problems**:
- Catches unintended exceptions.
- Debugging is difficult.
- Catches system exceptions like KeyboardInterrupt.

**Correct Method**:
```python
# ✅ Good Example
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except KeyError as e:
    logger.error(f"Missing key: {e}")
```

#### Pattern 3: Use of eval/exec

```python
# ❌ Absolutely Forbidden
user_input = request.get('code')
eval(user_input)  # Security risk, zero type safety
exec(user_input)  # Equally dangerous
```

**Problems**:
- Severe security risk.
- Impossible to type check.
- Impossible to debug.

## ✅ Correct Type Hinting Methods

### 1. Explicit Type Hints (Mandatory)

```python
# ✅ Type hints for all functions
from typing import Optional, List, Dict

def get_user_by_id(user_id: str) -> Optional[User]:
    """Retrieves a user by ID"""
    # Implementation
    pass

def get_all_users() -> List[User]:
    """Retrieves all users"""
    # Implementation
    return []

def get_user_settings(user_id: str) -> Dict[str, str]:
    """Retrieves user settings"""
    # Implementation
    return {}
```

### 2. Use of Union Types

```python
from typing import Union

# ✅ When allowing multiple types
def process_value(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value)
    return value

# Use the | operator in Python 3.10+
def process_value_modern(value: int | str) -> str:
    if isinstance(value, int):
        return str(value)
    return value
```

### 3. Explicit Use of Optional Types

```python
from typing import Optional

# ✅ When None is a possibility
def find_user(user_id: str) -> Optional[User]:
    user = db.query(User).filter_by(id=user_id).first()
    return user  # User | None

# Always perform a None check at usage
user = find_user('123')
if user is not None:
    print(user.name)  # Type-safe
```

### 4. Use of Generic Types

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, model: type[T]) -> None:
        self.model = model

    def find_by_id(self, id: str) -> Optional[T]:
        # Implementation
        pass

    def find_all(self) -> List[T]:
        # Implementation
        return []

# Usage example
user_repo = Repository[User](User)
user = user_repo.find_by_id('123')  # Optional[User]
users = user_repo.find_all()  # List[User]
```

## 📚 Python Best Practices

### 1. Thorough Type Hinting

```python
# ✅ Type hints in all function signatures
def calculate_total(
    items: List[Dict[str, float]],
    tax_rate: float = 0.1
) -> float:
    """Calculates total amount (including tax)"""
    subtotal = sum(item['price'] for item in items)
    return subtotal * (1 + tax_rate)

# ✅ Type hints for class attributes
class User:
    id: str
    name: str
    email: str
    age: int
    is_active: bool

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        age: int,
        is_active: bool = True
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.age = age
        self.is_active = is_active
```

### 2. Use of Type Guards

```python
from typing import TypeGuard

def is_user_dict(data: object) -> TypeGuard[Dict[str, str]]:
    """Checks if a dictionary is of User type"""
    return (
        isinstance(data, dict) and
        'id' in data and isinstance(data['id'], str) and
        'name' in data and isinstance(data['name'], str) and
        'email' in data and isinstance(data['email'], str)
    )

# Usage example
def process_user_data(data: object) -> None:
    if is_user_dict(data):
        print(f"User: {data['name']}")  # Type-safe
    else:
        raise ValueError("Invalid user data")
```

### 3. Utilization of Type Aliases

```python
from typing import Dict, List, Tuple

# ✅ Define type aliases for complex types
UserId = str
UserData = Dict[str, str | int | bool]
UserList = List[UserData]
Coordinate = Tuple[float, float]

def get_user_location(user_id: UserId) -> Coordinate:
    # Implementation
    return (35.6895, 139.6917)

def get_users() -> UserList:
    # Implementation
    return []
```

### 4. Constraints on Type Variables

```python
from typing import TypeVar

# ✅ Constraint to specific types
T = TypeVar('T', str, int, float)

def first_element(items: List[T]) -> T:
    return items[0]

# ✅ Specification of upper bounds
class Animal:
    pass

class Dog(Animal):
    pass

T_Animal = TypeVar('T_Animal', bound=Animal)

def feed_animal(animal: T_Animal) -> T_Animal:
    # Accepts only Animal or its subclasses
    return animal
```

## 📦 Utilizing TypedDict

### Basic Usage

```python
from typing import TypedDict

# ✅ Use TypedDict for dictionary-based data structures
class UserDict(TypedDict):
    id: str
    name: str
    email: str
    age: int

class UserDictOptional(TypedDict, total=False):
    # total=False makes all properties optional
    phone: str
    address: str

# Usage example
def create_user(user_data: UserDict) -> User:
    return User(
        id=user_data['id'],
        name=user_data['name'],
        email=user_data['email'],
        age=user_data['age']
    )

user_data: UserDict = {
    'id': '123',
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
}

user = create_user(user_data)
```

### Partial Optionality

```python
from typing import TypedDict, NotRequired

# For Python 3.11+
class UserProfile(TypedDict):
    id: str
    name: str
    email: str
    bio: NotRequired[str]  # Only this property is optional
    avatar_url: NotRequired[str]

# For versions before Python 3.10
class UserProfileBase(TypedDict):
    id: str
    name: str
    email: str

class UserProfileOptional(TypedDict, total=False):
    bio: str
    avatar_url: str

# Combine via inheritance
class UserProfile310(UserProfileBase, UserProfileOptional):
    pass
```

### Nested TypedDict

```python
class AddressDict(TypedDict):
    street: str
    city: str
    postal_code: str

class UserWithAddress(TypedDict):
    id: str
    name: str
    address: AddressDict  # Nested structure

# Usage example
user: UserWithAddress = {
    'id': '123',
    'name': 'John',
    'address': {
        'street': '123 Main St',
        'city': 'Tokyo',
        'postal_code': '100-0001'
    }
}
```

## 🔌 Utilizing Protocol (Structural Subtyping)

### Basic Protocol

```python
from typing import Protocol

# ✅ Use Protocol when duck typing is needed
class Drawable(Protocol):
    """An object that can be drawn"""
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

# Both can be handled as Drawable (no explicit inheritance needed)
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK
render(Square())  # OK
```

### Runtime-Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        ...

class FileWrapper:
    def close(self) -> None:
        print("Closing file")

# Type checking at runtime
obj = FileWrapper()
if isinstance(obj, Closable):
    obj.close()  # OK
```

### Complex Protocol

```python
from typing import Protocol, Iterator

class SupportsIter(Protocol):
    """An object that can be iterated over"""
    def __iter__(self) -> Iterator[int]:
        ...

    def __len__(self) -> int:
        ...

class CustomRange:
    def __init__(self, max_value: int) -> None:
        self.max = max_value

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.max))

    def __len__(self) -> int:
        return self.max

def process_iterable(items: SupportsIter) -> int:
    return sum(items)

custom_range = CustomRange(10)
result = process_iterable(custom_range)  # OK
```

## 🎁 Utilizing dataclass

### Basic dataclass

```python
from dataclasses import dataclass, field
from typing import List

# ✅ Use @dataclass for data classes
@dataclass
class User:
    id: str
    name: str
    email: str
    age: int
    is_active: bool = True  # Default value

# __init__, __repr__, __eq__, etc., are automatically generated
user = User(
    id='123',
    name='John Doe',
    email='john@example.com',
    age=30
)

print(user)  # User(id='123', name='John Doe', ...)
```

### Immutable dataclass

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

point = Point(1.0, 2.0)
# point.x = 3.0  # Error: Cannot modify because frozen=True
```

### Default Values and factory

```python
from typing import List
from dataclasses import dataclass, field

@dataclass
class Team:
    name: str
    members: List[str] = field(default_factory=list)  # ✅ Mutable default value
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

# ❌ Bad Example (Absolutely forbidden)
# members: List[str] = []  # Mutable default arguments are dangerous
```

### Inheritance and post_init

```python
@dataclass
class Person:
    name: str
    age: int

@dataclass
class Employee(Person):
    employee_id: str
    department: str

    def __post_init__(self) -> None:
        """Post-initialization processing"""
        if self.age < 18:
            raise ValueError("Employee must be at least 18 years old")

employee = Employee(
    name='John',
    age=25,
    employee_id='E001',
    department='Engineering'
)
```

## 🔧 Using Type Checkers

### mypy

#### Basic Usage

```bash
# Check all Python files
mypy src/

# Check only a specific file
mypy src/main.py

# Check in strict mode
mypy --strict src/

# Generate HTML report
mypy --html-report ./mypy-report src/
```

#### example mypy.ini Configuration

```ini
[mypy]
# Basic settings
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# Strict type checking
disallow_any_unimported = True
disallow_any_expr = False  # Set to True for complete strictness
disallow_any_decorated = True
disallow_any_explicit = True
disallow_any_generics = True
disallow_subclassing_any = True

# Error settings
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

# Import settings
ignore_missing_imports = False
follow_imports = normal

# Others
strict_equality = True
strict_optional = True

# Third-party libraries
[mypy-pytest.*]
ignore_missing_imports = True

[mypy-requests.*]
ignore_missing_imports = True
```

### pyright

#### Basic Usage

```bash
# Check all Python files
pyright

# Check only a specific file
pyright src/main.py

# Specify configuration file
pyright --project pyrightconfig.json
```

#### example pyrightconfig.json Configuration

```json
{
  "include": ["src"],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    "**/.*"
  ],
  "ignore": ["tests"],

  "typeCheckingMode": "strict",

  "reportMissingImports": true,
  "reportMissingTypeStubs": false,

  "pythonVersion": "3.11",
  "pythonPlatform": "Linux",

  "executionEnvironments": [
    {
      "root": "src",
      "pythonVersion": "3.11",
      "extraPaths": ["lib"]
    }
  ]
}
```

### mypy vs pyright Usage Comparison

| Feature | mypy | pyright |
|------|------|---------|
| Speed | Slow | Fast |
| Accuracy | High | Very high |
| VS Code Integration | Via Pylance | Native support |
| Customization | Extensive | Simple |
| Recommended Use | CI/CD | Editor integration |

**Recommended Setup**:
- **During Development**: pyright (VS Code + Pylance)
- **In CI/CD**: mypy (for stricter checks)

### CI/CD Integration for Type Checking

```yaml
# .github/workflows/type-check.yml
name: Type Check

on: [push, pull_request]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install mypy
          pip install types-requests  # Type stubs

      - name: Run mypy
        run: mypy src/

      - name: Run pyright
        run: |
          npm install -g pyright
          pyright
```

## 🔗 Related Files

- **[SKILL.md](../SKILL.md)** - Back to Overview
- **[TYPESCRIPT.md](./TYPESCRIPT.md)** - TypeScript Type Safety
- **[ANTI-PATTERNS.md](./ANTI-PATTERNS.md)** - Patterns to Avoid
- **[REFERENCE.md](./REFERENCE.md)** - Checklists and Tool Settings
