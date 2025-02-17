# Customs Declaration Processing Module for Frappe

A configurable customs declaration processing system built for Frappe that supports import/export workflows, automated tax assessment, and cargo clearance.

## Features

- **Configurable Customs Processing**: Import customs rules, tariff codes, and procedures via JSON/CSV
- **Complete Document Workflow**:
  - Single Administrative Document (SAD)
  - Cargo Manifests
  - Waybills
  - Tax Assessment
  - Cargo Release Orders
- **Automated Calculations**: 
  - Duty assessment
  - VAT calculation
  - Excise tax computation
- **Role-Based Access Control**:
  - Customs Officers
  - Brokers
  - Shipping Agents
  - Importers

## Installation

```bash
bench get-app customs https://github.com/your-username/customs
bench --site your-site.local install-app customs
```

## Configuration

1. Set up customs offices and user roles
2. Import tariff codes and duty rates
3. Configure workflow states and transitions
4. Set up document numbering series

## Usage

### Creating a New Declaration

1. Create a new Single Administrative Document
2. Link to Manifest/Waybill
3. Enter goods classification (HS Codes)
4. Submit for assessment

### Processing Workflow

1. **Declaration Submission**
   - Broker submits SAD
   - System validates required fields

2. **Tax Assessment**
   - Officer reviews declaration
   - System calculates applicable duties
   - Assessment notice generated

3. **Payment Processing**
   - Duties payment recorded
   - Receipt generated

4. **Cargo Release**
   - Release order generated
   - Goods cleared for delivery

## Documentation

For detailed documentation, visit:
- [User Guide](docs/user-guide.md)
- [Technical Documentation](docs/technical.md)
- [API Reference](docs/api.md)

## License

MIT License. See [license.txt](license.txt) for more information.

## Support

- GitHub Issues: [Report a bug](https://github.com/your-username/customs/issues)
- Email Support: rubailly@gmail.com

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Credits

Developed by [Logiic Ltd](https://www.logiic.com/)
