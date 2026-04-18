"""cases-faker: realistic synthetic helpdesk/support ticket data."""

from cases_faker.generator import CaseGenerator, GeneratorConfig
from cases_faker.schemas import get_schema, list_schemas

__version__ = "0.1.0"
__all__ = ["CaseGenerator", "GeneratorConfig", "get_schema", "list_schemas"]
