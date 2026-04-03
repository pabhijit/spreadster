from pathlib import Path
from spreadster.providers.sample_provider import SampleProvider

def get_provider(sample: bool = True):
    if sample:
        sample_path = Path(__file__).resolve().parents[3] / "examples" / "sample_input.json"
        return SampleProvider(str(sample_path))
    raise NotImplementedError("Plug in your real provider here.")
