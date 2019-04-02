# для pytest работает
import sys
from pathlib import Path

p = Path(__file__).parent / '..'
sys.path.insert(0, p.absolute())
