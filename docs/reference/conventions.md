# Public reference convention

Every supported Python operation, CLI command, and reusable data format has a
reference entry using the fields below. A field is marked **inapplicable** when
the concept does not apply; it is never silently omitted.

| Field | Required content |
| --- | --- |
| Purpose | The user-visible capability and its intended use. |
| Availability | Supported release, import path, command path, or compatibility status. |
| Inputs | Parameters, flags, files, and accepted representations. |
| Types | Python, CLI, column, or value types. |
| Shapes | Array dimensions or **inapplicable**. |
| Dtypes | Array/column dtypes or **inapplicable**. |
| Defaults | Runtime and parser defaults, including when a required input prevents a parser default from applying. |
| Choices | Enumerated values or **inapplicable**. |
| Constraints | Relationships and validation rules beyond basic types. |
| Outputs | Return values, files, schemas, and shapes. |
| Ordering | Stable ordering and input/output alignment, or **inapplicable**. |
| Side effects | File writes, mutation, network access, caching, or **none**. |
| Failures | Failure conditions and exception classes or CLI exit behavior; message text is not guaranteed. |

Generated parser facts and human-authored semantics are visibly distinguished.
The documentation build refreshes generated syntax from the selected code
checkout and fails if the built reference lacks a required field.
