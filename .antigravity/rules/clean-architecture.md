# Clean Architecture Compliance Rules

- **Delivery Layer (FastAPI/main.py)**: It is strictly prohibited to instantiate, coordinate, or execute business/application logic directly inside HTTP route functions. HTTP endpoints must only validate input data (via Pydantic schemas), invoke a pure Use Case/Application Service, and translate its output into HTTP response payloads.
- **Application/Domain Layer (Use Cases)**: All workflow coordination (e.g., fetching a product barcode name from a Gateway and persisting it via a Repository) must be encapsulated in pure Use Case classes (e.g., `RegisterDonationUseCase`, `ListDonationsUseCase`, etc.).
- **Dependency Injection**: Use Case classes must receive their repository and gateway dependencies (either abstractions or interfaces) via their constructor (`__init__`). They should not instantiate concrete repository or gateway classes directly inside their methods.
