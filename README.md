# Python Voltage Monitor

This project simulates a **PLC voltage monitoring system** with extensible current processing strategies.  
It provides a modular architecture where strategies can be easily plugged into the `PLCVoltageReader` for flexible testing and ulation.


## 📌 Features

- **Type Validation**  
  Ensure that inputs conform to expected types before processing.  

- **Strategy Pattern for Current Processing**  
  Implement different strategies to manipulate or simulate voltage/current values.

- **Testing with Pytest**  
  Comprehensive test coverage with both fast and slow tests.


## 🏗️ Core Interfaces & Strategies

```python
class ICurrentProcessingStrategy(Protocol):
    """Interface: Defines current processing strategy"""
    def process(self, currents: Tuple[float, ...]) -> Tuple[float, ...]:
        ...
```

### 🔹 CurrentJumpStrategy
Random jump strategy that adds a random offset to the current values at fixed intervals.

```python
# Example
strategy = CurrentJumpStrategy(lower_bound=-5.0, upper_bound=5.0, interval_sec=1.0)
```

### 🔹 CurrentSmoothChangeStrategy
Smooth wave-like change strategy, generating values that gradually increase and then decrease.

```python
# Example
strategy = CurrentSmoothChangeStrategy(step=1.0, count=20, direction=Direction.UP)
```


## ⚡ PLC Voltage Reader

```python
class PLCVoltageReader(IValidatingReader):
    """Simulates real PLC voltage reading with type validation and strategy processing"""
```

The `PLCVoltageReader` can be configured with a processing strategy:

```python
reader = PLCVoltageReader(allow_types=(float,), strategy=CurrentSmoothChangeStrategy())
voltages = reader.read(220.0)
```


## ✅ Testing

This project uses [pytest](https://docs.pytest.org/) for unit testing.

### Run all tests
```bash
pytest -v
```

### Run only tests with specific keywords
```bash
pytest -k "jump"
```

### Mark slow tests
Some tests may be slow (e.g., using `time.sleep`).  
They are marked with `@pytest.mark.slow`.

```python
import pytest

@pytest.mark.slow
def test_delayed_behavior():
    ...
```

### Run all tests except slow ones
```bash
pytest -m "not slow"
```

### Run only slow tests
```bash
pytest -m slow
```

### Example `pytest.ini`
Make sure you have a `pytest.ini` file to register the `slow` marker:

```ini
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
```

## 📜 License

This project is licensed under the **Apache License 2.0**.  
You may not use this file except in compliance with the License.  
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and limitations under the License.
