# Pharmacy Database Project Proposal

# Database Description

I will create a pharmacy management database. It will keep track of medications, patients, prescriptions, and suppliers.
It will allow you to search the inventory of the database to find the inventory, patient, supplier, etc.

# Entity Types and Descriptions

## Medication

Medications will be described by:
- Medication name
- Dosage
- Quantity in stock

For example:
- Amoxicillin - 500 mg - 90 capsules
- Ibuprofen - 600 mg - 60 tablets

## Patient

Patients will be described by:
- First name
- Last name
- Date of birth

For example
- John Smith - 01/01/1991
- Jane Doe - 01/01/1991

## Prescription

Prescriptions will be described by:
- Drug Name
- Prescription/RX number
- Written Date
- Quantity prescribed

For example:
- {Drug name} - #1001 - 09/01/2026 - 30 capsules
- {Drug name} - #1002 - 09/02/2026 - 60 tablets

## Supplier

Suppliers will be described by:
- Company name
- Phone number
- Address

For example:
- ABC Drugs — 555-123-4567 — 123 Main Street
- Mckesson — 555-987-6543 — 456 Oak Avenue

# Questions/Use-Cases

1. I want to be able to look up which medications have been prescribed to a particular patient.

2. I want to be able to check how much of a particular medication the pharmacy currently has in stock.

3. I want to be able to look up which supplier provides a particular medication.

4. I want to be able to manage inventory.
