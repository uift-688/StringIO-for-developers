# StringIO-for-developers
More extended io.StringIO. with write, read, etc. as triggers.

===

# Internal processes available:
- Control of return values of internal functions (errors were identified / return)
- Control of function arguments to base class basic processing (super.args)
- Replacement mode for the original argument to the base class function (super.default.None)
- Dynamic code execution (exec.code)

---

# Custom Control Syntax
   ((<control name>, <control value (tuple type for super.args)>), more can be added)

# Newly added structures
- class.Writes - List of values written so far
